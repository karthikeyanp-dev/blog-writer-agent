---
name: blog-content-generation
description: Generate and refine blog post content using LLM prompts. Use when modifying blog writing logic, changing prompt templates, or adjusting content formatting in the write_node.
---

# Blog Content Generation

## Write Node Location

Blog writing logic is in `src/agents/nodes.py` in `write_node()` function.

## Current Prompt Template

```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert blog writer..."),
    ("user", "Topic: {topic}\n\nResearch:\n{research}\n\nWrite the blog post...")
])
```

## Key Requirements

1. **System prompt constraints**:
   - Must instruct: "Output ONLY the blog post content"
   - Must prohibit: conversational text, introductions, conclusions
   - Must require: direct start with blog title/content

2. **User prompt must include**:
   - `{topic}` - the blog subject
   - `{research}` - search results for context
   - Sources section requirement at bottom

## Modifying Content Style

Edit the system prompt string in `write_node()` to change:
- Tone (professional, casual, technical)
- Structure (sections, length, formatting)
- Audience (beginners, experts, general)

## Adding Content Sections

To add new sections (e.g., TL;DR, Key Takeaways):

1. Update system prompt with section requirements
2. LLM will follow instructions in the generated content
3. No code changes needed beyond prompt text

## Sources Section

The prompt requires URLs from research to be listed. This is automatic - the LLM extracts URLs from the `{research}` parameter which contains Tavily search results with links.
