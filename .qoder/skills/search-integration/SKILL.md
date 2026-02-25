---
name: search-integration
description: Configure and modify web search functionality using Tavily API. Use when changing search providers, adjusting search parameters, or modifying research node behavior.
---

# Search Integration

## Implementation Location

Search tool: `src/tools/search.py`
Research node: `src/agents/nodes.py` (research_node)

## Current Setup

Uses TavilySearchResults from `langchain_community`:

```python
from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults(max_results=5)
result = search.invoke(query)  # Returns string with snippets + URLs
```

## Configuration

API key sources (in order of priority):
1. `TAVILY_API_KEY` environment variable
2. `settings.tavily_api_key` from `.env` file

## Modifying Search Parameters

In `get_search_tool()`:

- `max_results` - Number of results (default: 5)
- `search_depth` - "basic" or "advanced"
- `include_answer` - Include AI-generated summary

## Changing Search Provider

To switch to different search (e.g., DuckDuckGo):

1. Replace import in `search.py`:
   ```python
   from langchain_community.tools import DuckDuckGoSearchRun
   ```

2. Update `get_search_tool()` to return new tool

3. Adjust `perform_search()` if return format differs

## Enhancing Research Node

Current: Single search query
To add multiple queries:

```python
def research_node(state: BlogState) -> BlogState:
    topic = state.get("topic")
    queries = [
        f"latest information about {topic}",
        f"{topic} trends 2024",
        f"{topic} expert opinions"
    ]
    results = []
    for query in queries:
        results.append(perform_search(query))
    return {"research_content": "\n\n".join(results)}
```
