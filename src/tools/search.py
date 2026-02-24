import os
from langchain_community.tools.tavily_search import TavilySearchResults
from ..config.settings import settings
from ..utils.logger import logger

def get_search_tool():
    """
    Returns the TavilySearchResults tool which includes snippets and links.
    """
    try:
        if "TAVILY_API_KEY" not in os.environ and settings.tavily_api_key:
            os.environ["TAVILY_API_KEY"] = settings.tavily_api_key
            
        # Using TavilySearchResults to get metadata (titles, links)
        search = TavilySearchResults(max_results=5)
        logger.info("Search tool initialized.")
        return search
    except Exception as e:
        logger.error(f"Error initializing search tool: {e}")
        raise e

def perform_search(query: str) -> str:
    """
    Performs a search query and returns the structured results.
    """
    tool = get_search_tool()
    logger.info(f"Performing search for: {query}")
    try:
        # invoke returns a string representation of list of results [snippet: ..., title: ..., link: ...]
        result = tool.invoke(query)
        logger.info("Search completed.")
        return result
    except Exception as e:
        logger.error(f"Search failed: {e}")
        return f"Search failed: {e}"
