from langgraph.graph import StateGraph, END
from .state import BlogState
from .nodes import research_node, write_node, prompt_node, image_node

def create_blog_graph():
    """
    Creates the LangGraph for the blog generation workflow.
    """
    workflow = StateGraph(BlogState)

    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("write", write_node)
    workflow.add_node("prompt", prompt_node)
    workflow.add_node("image", image_node)

    # Define edges
    workflow.set_entry_point("research")
    workflow.add_edge("research", "write")
    workflow.add_edge("write", "prompt")
    workflow.add_edge("prompt", "image")
    workflow.add_edge("image", END)

    return workflow.compile()
