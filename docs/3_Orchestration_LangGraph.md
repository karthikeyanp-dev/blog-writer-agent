# 3. Orchestration: LangGraph

## What is LangGraph?
LangGraph is a library for building stateful, multi-actor applications with LLMs. Unlike simple linear chains, LangGraph allows us to define cycles, conditions, and persistence.

## 1. The State (`BlogState`)
Think of this as the "memory" or "context" passed between different steps of the agent.

**Code Reference:** `src/agents/state.py`
```python
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
```
*   `TypedDict`: A Python typing feature that defines the structure of the state dictionary.
*   **Why?** This ensures every node (research, write, etc.) knows exactly what data is available and what type it is (string, optional, etc.).

## 2. The Nodes (The "Actions")
Nodes are functions that modify the state. Each node takes the current state as input and returns *updates* to that state.

**Example: The Research Node** (`src/agents/nodes.py`)
```python
def research_node(state: BlogState) -> BlogState:
    topic = state.get("topic")
    # ... performs search ...
    return {"research_content": search_results}
```
*   **Input**: `state` (contains `topic`).
*   **Action**: Calls Tavily Search.
*   **Output**: Updates `research_content` in the state. The rest of the state (`topic`, etc.) remains unchanged.

## 3. The Graph (The "Workflow")
The graph defines the flow of execution: **Entry Point -> Node A -> Node B -> End**.

**Code Reference:** `src/agents/graph.py`
```python
def create_blog_graph():
    workflow = StateGraph(BlogState)

    # 1. Add Nodes
    workflow.add_node("research", research_node)
    workflow.add_node("write", write_node)
    # ... add other nodes ...

    # 2. Define Edges (The Flow)
    workflow.set_entry_point("research")
    workflow.add_edge("research", "write")
    workflow.add_edge("write", "prompt")
    # ... define other edges ...
    workflow.add_edge("image", END)

    return workflow.compile()
```
*   `StateGraph`: Initializes the graph with our `BlogState` schema.
*   `add_node`: Registers a function (node) with a name (string key).
*   `add_edge`: Defines a directed connection. When "research" finishes, go to "write".
*   `compile()`: Builds the executable application.

## 4. Execution Flow
When you run `app.invoke({"topic": "AI Agents"})`:
1.  **Entry Point**: Start at `research_node`.
2.  **Research**: Find info on "AI Agents". Update state with `research_content`.
3.  **Edge**: Move to `write_node`.
4.  **Write**: Use `topic` + `research_content` to generate `blog_content`.
5.  **Edge**: Move to `prompt_node`.
6.  **Prompt**: Use `blog_content` snippet to create `image_prompt`.
7.  **Edge**: Move to `image_node`.
8.  **Image**: Generate `image_url` using `image_prompt`.
9.  **End**: Graph execution completes.

---
**Next**: [4. Project Walkthrough](./4_Project_Walkthrough.md)
