from typing import TypedDict, Annotated, List, Optional
import operator

class BlogState(TypedDict):
    """
    State of the blog generation process.
    """
    topic: str
    research_content: Optional[str]
    blog_content: Optional[str]
    image_prompt: Optional[str]
    image_url: Optional[str]
    error: Optional[str]
