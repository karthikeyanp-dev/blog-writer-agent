from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from ..config.settings import settings
from ..tools.search import perform_search
from ..tools.image import generate_image_url
from .state import BlogState
from ..utils.logger import logger

def get_llm():
    return ChatOpenAI(
        model=settings.model_name,
        temperature=settings.temperature,
        openai_api_key=settings.openai_api_key
    )

def research_node(state: BlogState) -> BlogState:
    """
    Researches the topic using DuckDuckGo.
    """
    topic = state.get("topic")
    logger.info(f"Researching topic: {topic}")
    
    try:
        # Simple search for now. Can be enhanced with multiple queries.
        search_results = perform_search(f"latest information about {topic}")
        return {"research_content": search_results}
    except Exception as e:
        logger.error(f"Research failed: {e}")
        return {"error": str(e)}

def write_node(state: BlogState) -> BlogState:
    """
    Writes the blog post based on the research.
    """
    if state.get("error"):
        logger.warning("Skipping write_node due to previous error.")
        return {}

    topic = state.get("topic")
    research_content = state.get("research_content", "")
    
    logger.info(f"Writing blog post for topic: {topic}")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert blog writer. Write a comprehensive and engaging blog post based on the provided research. Use Markdown formatting with headings."),
        ("user", "Topic: {topic}\n\nResearch:\n{research}\n\nWrite the blog post. IMPORTANT: You must include a 'Sources' section at the bottom of the post listing the URLs from the research.")
    ])
    
    chain = prompt | get_llm() | StrOutputParser()
    
    try:
        blog_content = chain.invoke({"topic": topic, "research": research_content})
        return {"blog_content": blog_content}
    except Exception as e:
        logger.error(f"Writing failed: {e}")
        return {"error": str(e)}

def prompt_node(state: BlogState) -> BlogState:
    """
    Generates an image prompt based on the blog content.
    """
    if state.get("error"):
        logger.warning("Skipping prompt_node due to previous error.")
        return {}

    blog_content = state.get("blog_content", "")
    topic = state.get("topic")
    
    logger.info("Generating image prompt...")
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert at creating prompts for AI image generators like DALL-E 3."),
        ("user", "Create a detailed and creative image prompt for a blog post about '{topic}'. \n\nHere is a snippet of the blog content for context:\n{snippet}...\n\nThe prompt should describe a visual scene that captures the essence of the blog post. Keep it under 1000 characters.")
    ])
    
    chain = prompt | get_llm() | StrOutputParser()
    
    try:
        # Use first 500 chars as context
        snippet = blog_content[:500]
        image_prompt = chain.invoke({"topic": topic, "snippet": snippet})
        return {"image_prompt": image_prompt}
    except Exception as e:
        logger.error(f"Prompt generation failed: {e}")
        return {"error": str(e)}

def image_node(state: BlogState) -> BlogState:
    """
    Generates the image using the prompt.
    """
    if state.get("error"):
        logger.warning("Skipping image_node due to previous error.")
        return {}

    image_prompt = state.get("image_prompt")
    
    if not image_prompt:
        logger.warning("No image prompt found. Skipping image generation.")
        return {"error": "No image prompt found"}

    logger.info("Generating image...")
    
    try:
        image_url = generate_image_url(image_prompt)
        return {"image_url": image_url}
    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        return {"error": str(e)}
