import os
import glob
import time
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sys
import uuid

# Add src to path if needed, though usually not needed if running from root
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.agents.graph import create_blog_graph
from src.utils.files import save_image_from_url
from src.config.settings import settings

# Determine environment
IS_VERCEL = os.environ.get("VERCEL") == "1"
# On Vercel, we can only write to /tmp. 
# NOTE: Files in /tmp are ephemeral and will be lost.
DOCS_DIR = "/tmp/docs" if IS_VERCEL else "docs"
STATIC_DIR = "/tmp/static" if IS_VERCEL else "static"
IMAGES_DIR = os.path.join(STATIC_DIR, "images")

# Ensure directories exist
os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

app = FastAPI(
    title="Markdown Blog API", 
    description="API to serve markdown files as blog posts.",
    root_path="/api" if IS_VERCEL else ""
)

# Mount static directory for images
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# CORS Configuration
origins = [
    "*",  # Allow all origins for development convenience. Restrict in production.
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BlogPost(BaseModel):
    filename: str
    last_modified: str
    content: str | None = None  # Content is optional in list view

class GenerateRequest(BaseModel):
    topic: str

@app.post("/generate", response_model=BlogPost)
def generate_post(request: GenerateRequest):
    """Generate a new blog post based on a topic."""
    topic = request.topic
    if not topic:
        raise HTTPException(status_code=400, detail="Topic is required")
    
    try:
        # Create and invoke the graph
        workflow = create_blog_graph()
        initial_state = {"topic": topic}
        final_state = workflow.invoke(initial_state)
        
        blog_content = final_state.get("blog_content")
        image_url = final_state.get("image_url")
        
        if not blog_content:
            raise HTTPException(status_code=500, detail="Failed to generate blog content")
            
        # Ensure title
        if not blog_content.lstrip().startswith(f"# {topic}"):
            blog_content = f"# {topic}\n\n{blog_content}"
            
        # Handle image
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        sanitized_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '_', '-')).rstrip()
        sanitized_topic = sanitized_topic.replace(' ', '_')
        
        image_filename = f"{sanitized_topic}_{timestamp}.png"
        local_image_path = os.path.join(IMAGES_DIR, image_filename)
        
        if image_url:
            # Save image locally
            try:
                save_success = save_image_from_url(image_url, local_image_path)
                if save_success:
                    # Use relative URL for frontend
                    relative_image_url = f"/static/images/{image_filename}"
                    # Insert image into markdown
                    image_markdown = f"![Blog Image]({relative_image_url})\n\n"
                    # Insert after title
                    lines = blog_content.split('\n')
                    title_index = -1
                    for i, line in enumerate(lines):
                        if line.strip().startswith('# '):
                            title_index = i
                            break
                    
                    if title_index != -1:
                        lines.insert(title_index + 1, image_markdown)
                        blog_content = '\n'.join(lines)
                    else:
                        blog_content = image_markdown + blog_content
            except Exception as img_error:
                print(f"Error saving image: {img_error}")
                # Continue without image if it fails
        
        # Save the generated markdown to docs folder so it persists
        md_filename = f"{sanitized_topic}.md"
        md_path = os.path.join(DOCS_DIR, md_filename)
        
        # Ensure unique filename
        if os.path.exists(md_path):
            md_filename = f"{sanitized_topic}_{timestamp}.md"
            md_path = os.path.join(DOCS_DIR, md_filename)
            
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(blog_content)
            
        # Return the result
        mod_time = os.path.getmtime(md_path)
        last_modified = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            "filename": md_filename,
            "last_modified": last_modified,
            "content": blog_content
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/posts", response_model=list[BlogPost])
async def list_posts():
    """List all available markdown posts with metadata."""
    if not os.path.exists(DOCS_DIR):
        return []
        
    posts = []
    # Find all .md files in the docs directory
    files = glob.glob(os.path.join(DOCS_DIR, "*.md"))
    
    # Also check the original repo docs directory if we are on Vercel
    if IS_VERCEL:
        original_docs = "docs"
        if os.path.exists(original_docs):
            files.extend(glob.glob(os.path.join(original_docs, "*.md")))

    for file_path in files:
        filename = os.path.basename(file_path)
        # Get last modified time
        mod_time = os.path.getmtime(file_path)
        last_modified = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        
        posts.append({
            "filename": filename,
            "last_modified": last_modified,
            "content": None # Don't send full content in list to save bandwidth
        })
    
    # Sort by filename or date if needed (currently unsorted/glob order)
    return sorted(posts, key=lambda x: x['filename'])

@app.get("/posts/{filename}", response_model=BlogPost)
async def get_post(filename: str):
    """Get the content of a specific markdown post."""
    # Security check: ensure filename doesn't contain path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")
        
    file_path = os.path.join(DOCS_DIR, filename)
    
    if not os.path.exists(file_path):
        # Check original docs if on Vercel
        if IS_VERCEL:
            file_path = os.path.join("docs", filename)
            if not os.path.exists(file_path):
                 raise HTTPException(status_code=404, detail="Post not found")
        else:
            raise HTTPException(status_code=404, detail="Post not found")
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        mod_time = os.path.getmtime(file_path)
        last_modified = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            "filename": filename,
            "last_modified": last_modified,
            "content": content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Run the API server
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
