import os
import sys
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.agents import AgentExecutor, create_openai_tools_agent
from PIL import Image
from io import BytesIO

# Load environment variables
load_dotenv()

def write_blog(topic):
    """Generates a blog post based on the given topic using real-time search."""
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    # Initialize the search tool
    search = DuckDuckGoSearchRun()
    tools = [search]
    
    # Get the prompt to use - you can modify this!
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert blog writer. First, research the given topic using the search tool to get the latest information. Then, write a comprehensive and engaging blog post based on your research. Ensure the blog post is well-structured with headings."),
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    # Construct the OpenAI Tools agent
    agent = create_openai_tools_agent(llm, tools, prompt)
    
    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    response = agent_executor.invoke({"input": f"Write a blog post about: {topic}"})
    return response["output"]

def generate_image_prompt(topic, blog_content):
    """Generates a detailed image prompt based on the blog topic and content."""
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert at creating prompts for AI image generators like DALL-E 3."),
        ("user", "Create a detailed and creative image prompt for a blog post about '{topic}'. \n\nHere is a snippet of the blog content for context:\n{snippet}...\n\nThe prompt should describe a visual scene that captures the essence of the blog post. Keep it under 1000 characters.")
    ])
    
    # Use the first 500 characters of the blog content for context
    snippet = blog_content[:500]
    
    chain = prompt | llm
    response = chain.invoke({"topic": topic, "snippet": snippet})
    return response.content

def generate_image(prompt_text):
    """Generates an image using DALL-E 3."""
    try:
        dalle = DallEAPIWrapper(model="dall-e-3")
        image_url = dalle.run(prompt_text)
        return image_url
    except Exception as e:
        print(f"Error generating image: {e}")
        return None

def save_image(image_url, filename="blog_image.png"):
    """Downloads and saves the image from the URL."""
    if not image_url:
        return
    
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image.save(filename)
            print(f"Image saved to {filename}")
        else:
            print("Failed to download image.")
    except Exception as e:
        print(f"Error saving image: {e}")

def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found. Please set it in the .env file.")
        return

    if len(sys.argv) > 1:
        topic = sys.argv[1]
    else:
        topic = input("Enter the blog topic: ")
    
    print(f"\nWriting blog post about '{topic}'...")
    blog_content = write_blog(topic)
    print("Blog post generated successfully.")
    
    print("\nGenerating image prompt...")
    image_prompt = generate_image_prompt(topic, blog_content)
    print(f"Image Prompt: {image_prompt}")
    
    print("\nGenerating image...")
    image_url = generate_image(image_prompt)
    
    # Save outputs
    with open("blog_post.md", "w", encoding="utf-8") as f:
        f.write(f"# {topic}\n\n")
        f.write(blog_content)
    print(f"Blog post saved to blog_post.md")
    
    if image_url:
        print(f"Image URL: {image_url}")
        save_image(image_url)
    
    print("\nDone!")

if __name__ == "__main__":
    main()
