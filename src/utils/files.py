import os
import requests
from io import BytesIO
from PIL import Image
from ..utils.logger import logger

def save_text(content: str, filepath: str) -> bool:
    """
    Saves text content to a file.
    """
    try:
        # ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Text content saved to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Error saving text to {filepath}: {e}")
        return False

def save_image_from_url(image_url: str, filepath: str) -> bool:
    """
    Downloads and saves an image from a URL.
    """
    if not image_url:
        logger.warning("No image URL provided to save.")
        return False
        
    try:
        # ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)

        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image.save(filepath)
            logger.info(f"Image saved to {filepath}")
            return True
        else:
            logger.error(f"Failed to download image. Status code: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error saving image to {filepath}: {e}")
        return False
