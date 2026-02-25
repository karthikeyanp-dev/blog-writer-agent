---
name: langgraph-workflow
description: Build and modify LangGraph workflows for AI agent orchestration. Use when creating nodes, edges, state graphs, or modifying agent workflows in the blog writer agent.
---

# LangGraph Workflow Development

## Quick Reference

This project uses LangGraph for agent orchestration with the following pattern:

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

# 1. Define state
class MyState(TypedDict):
    field: str

# 2. Create nodes
def my_node(state: MyState) -> MyState:
    return {"field": "value"}

# 3. Build graph
def create_graph():
    workflow = StateGraph(MyState)
    workflow.add_node("node_name", my_node)
    workflow.set_entry_point("node_name")
    workflow.add_edge("node_name", END)
    return workflow.compile()
```

## Adding New Nodes

1. Define node function in `src/agents/nodes.py`:
   - Accept `state: BlogState` parameter
   - Return dictionary with state updates
   - Handle errors gracefully

2. Register in `src/agents/graph.py`:
   - Import the node function
   - Add `workflow.add_node("name", function)`
   - Connect with `workflow.add_edge("from", "to")`

## State Management

State is in `src/agents/state.py`:
- Add new fields to `BlogState` TypedDict
- Nodes return partial state updates (dict)
- Use `state.get("key", default)` for safe access
- Set `error` field to skip downstream nodes

## Error Handling Pattern

```python
def node_name(state: BlogState) -> BlogState:
    if state.get("error"):
        return {}  # Skip on error
    try:
        # Node logic
        return {"field": result}
    except Exception as e:
        logger.error(f"Node failed: {e}")
        return {"error": str(e)}
```

## Node Execution Order

Current flow: `research` → `write` → `prompt` → `image` → END

Modify edges in `create_blog_graph()` to change workflow.
