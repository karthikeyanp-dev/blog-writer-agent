import argparse
import sys
from .agents.graph import create_blog_graph
from .config.settings import settings
from .utils.logger import logger
from .utils.files import save_text, save_image_from_url

def main():
    parser = argparse.ArgumentParser(description="AI Blog Writer Agent")
    parser.add_argument("topic", nargs="?", help="Topic for the blog post")
    args = parser.parse_args()

    topic = args.topic
    if not topic:
        topic = input("Enter the blog topic: ")

    logger.info(f"Starting blog generation for topic: {topic}")

    # Create and run the graph
    app = create_blog_graph()
    initial_state = {"topic": topic}
    
    try:
        final_state = app.invoke(initial_state)
        
        # Save blog post
        blog_content = final_state.get("blog_content")
        image_url = final_state.get("image_url")
        
        if blog_content:
            blog_path = settings.get_output_path(settings.blog_filename)
            
            # Ensure the blog content starts with the title if not already present
            if not blog_content.lstrip().startswith(f"# {topic}"):
                blog_content = f"# {topic}\n\n{blog_content}"

            # Insert image after title if available
            if image_url:
                lines = blog_content.split('\n')
                title_index = -1
                for i, line in enumerate(lines):
                    if line.strip().startswith('# '):
                        title_index = i
                        break
                
                if title_index != -1:
                    # Insert full width image markdown
                    image_markdown = f"\n![Blog Image]({settings.image_filename})\n"
                    lines.insert(title_index + 1, image_markdown)
                    blog_content = '\n'.join(lines)
                else:
                    # If no title found (shouldn't happen due to check above), prepend image
                    blog_content = f"![Blog Image]({settings.image_filename})\n\n{blog_content}"

            save_text(blog_content, blog_path)
            logger.info(f"Blog post saved to {blog_path}")
        else:
            logger.error("Failed to generate blog content.")

        # Save image
        if image_url:
            image_path = settings.get_output_path(settings.image_filename)
            save_image_from_url(image_url, image_path)
            logger.info(f"Image saved to {image_path}")
        else:
            logger.warning("No image generated or image URL not found.")

        logger.info("Process completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
