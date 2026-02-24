import os
from langchain_community.utilities.dalle_image_generator import DallEAPIWrapper
from ..config.settings import settings
from ..utils.logger import logger

def get_dalle_tool():
    """
    Returns the DallEAPIWrapper tool.
    """
    try:
        # Ensure OPENAI_API_KEY is set in environment for DALL-E wrapper
        if "OPENAI_API_KEY" not in os.environ and settings.openai_api_key:
            os.environ["OPENAI_API_KEY"] = settings.openai_api_key
            
        dalle = DallEAPIWrapper(model=settings.image_model_name)
        logger.info("DALL-E tool initialized.")
        return dalle
    except Exception as e:
        logger.error(f"Error initializing DALL-E tool: {e}")
        raise e

def generate_image_url(prompt: str) -> str:
    """
    Generates an image from a prompt and returns the URL.
    """
    tool = get_dalle_tool()
    logger.info(f"Generating image for prompt: {prompt}")
    try:
        url = tool.run(prompt)
        logger.info("Image generation completed.")
        return url
    except Exception as e:
        logger.error(f"Image generation failed: {e}")
        return ""
