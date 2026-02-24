# 4. Project Walkthrough

This document explains the structure of the Blog Writer Agent project and the purpose of each file.

## Project Structure
```text
blog_writer_agent/
├── src/
│   ├── agents/         # Graph, Nodes, State
│   │   ├── __init__.py
│   │   ├── graph.py    # The LangGraph workflow definition
│   │   ├── nodes.py    # The logic for each step (Research, Write, etc.)
│   │   └── state.py    # The BlogState schema
│   ├── config/         # Settings
│   │   ├── __init__.py
│   │   └── settings.py # Pydantic settings for API keys & config
│   ├── tools/          # Search, Image tools
│   │   ├── __init__.py
│   │   ├── image.py    # DALL-E 3 Wrapper
│   │   └── search.py   # Tavily Search Wrapper
│   ├── utils/          # Logger, File helpers
│   │   ├── __init__.py
│   │   ├── files.py    # Functions to save text/images
│   │   └── logger.py   # Standard logging setup
│   ├── __init__.py
│   └── main.py         # App entry point (initializes graph & runs it)
├── main.py             # Root launcher (runs src/main.py)
├── requirements.txt    # Dependencies
└── .env                # Environment variables (API Keys)
```

## Detailed File Explanations

### `src/config/settings.py`
**Purpose**: Centralized configuration management.
**Key Code**:
```python
class Settings(BaseSettings):
    openai_api_key: str = Field(..., description="OpenAI API Key")
    tavily_api_key: str = Field(..., description="Tavily API Key")
    # ... other fields ...
```
**Why?** Using `pydantic-settings` ensures that required environment variables are present and typed correctly. It prevents runtime errors due to missing keys.

### `src/tools/search.py`
**Purpose**: Encapsulates the logic for searching the web.
**Key Code**:
```python
def get_search_tool():
    # ... setup API key ...
    return TavilySearchResults(max_results=5)
```
**Why?** By wrapping the tool instantiation, we can easily swap out the underlying search engine (e.g., switch from DuckDuckGo to Tavily) without changing the rest of the application code.

### `src/agents/nodes.py`
**Purpose**: Contains the core business logic for each step of the workflow.
**Key Code**:
```python
def write_node(state: BlogState) -> BlogState:
    # ... logic to write blog post ...
    prompt = ChatPromptTemplate.from_messages(...)
    chain = prompt | get_llm() | StrOutputParser()
    return {"blog_content": chain.invoke(...)}
```
**Why?** Separating logic into "nodes" makes the code modular. Each node is a pure function that takes a state and returns a state update. This is easy to test and reason about.

### `src/agents/graph.py`
**Purpose**: Defines the orchestration logic.
**Key Code**:
```python
def create_blog_graph():
    workflow = StateGraph(BlogState)
    # ... add nodes and edges ...
    return workflow.compile()
```
**Why?** This file acts as the "director" of the agent. It decides the order of operations and how data flows between steps.

### `src/main.py` (Inside `src/`)
**Purpose**: The main application logic.
**Key Code**:
```python
def main():
    # ... parse arguments ...
    app = create_blog_graph()
    final_state = app.invoke({"topic": topic})
    # ... save results ...
```
**Why?** This file ties everything together. It handles user input (CLI arguments), initializes the graph, runs it, and saves the output to files.

### `main.py` (Root)
**Purpose**: A simple entry point for running the application from the root directory.
**Key Code**:
```python
from src.main import main
if __name__ == "__main__":
    main()
```
**Why?** This allows users to run `python main.py` directly without worrying about Python path issues or internal package structure.

---
**Next**: [5. Webinar Outline](./5_Webinar_Outline.md)
