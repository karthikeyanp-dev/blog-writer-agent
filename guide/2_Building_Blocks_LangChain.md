# 2. Building Blocks: LangChain, Tools, and Models

This project uses **LangChain**, a powerful framework for building applications powered by LLMs. Here are the core building blocks used in the Blog Writer Agent.

## 1. LLMs (Large Language Models)
The "brain" of the agent. We use OpenAI's GPT-4o for high-quality reasoning and writing.

**Code Reference:** `src/agents/nodes.py`
```python
def get_llm():
    return ChatOpenAI(
        model=settings.model_name,  # e.g., "gpt-4o"
        temperature=settings.temperature, # Controls creativity (0.7)
        openai_api_key=settings.openai_api_key
    )
```
*   `ChatOpenAI`: A LangChain wrapper for the OpenAI Chat Completion API.
*   `temperature`: Higher values (0.7-1.0) make the output more creative; lower values (0.0-0.3) make it more deterministic.

## 2. Tools (The "Hands")
Tools allow the agent to interact with the outside world.

### A. Tavily Search (Research)
**Code Reference:** `src/tools/search.py`
```python
def get_search_tool():
    # ... logic to check API key ...
    return TavilySearchResults(max_results=5)
```
*   **Why Tavily?** Unlike DuckDuckGo, Tavily is built for AI agents. It returns *content snippets* optimized for LLM context windows, not just links.
*   **How it works**: The agent sends a query -> Tavily scrapes multiple sites -> Tavily summarizes the content -> Agent receives structured results.

### B. DALL-E 3 (Image Generation)
**Code Reference:** `src/tools/image.py`
```python
def get_dalle_tool():
    return DallEAPIWrapper(model=settings.image_model_name)
```
*   **Purpose**: Creates visuals for the blog post.
*   **LangChain Wrapper**: `DallEAPIWrapper` simplifies the API call to a single function: `tool.run(prompt)`.

## 3. Prompts (The "Instructions")
Prompts guide the LLM on *how* to behave. We use `ChatPromptTemplate` to structure these instructions.

**Code Reference:** `src/agents/nodes.py`
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert blog writer..."), # Persona
    ("user", "Topic: {topic}\n\nResearch:\n{research}...") # Dynamic Inputs
])
```
*   **System Message**: Sets the persona and constraints ("expert blog writer", "use Markdown").
*   **User Message**: Provides the specific task inputs (the topic and the research data found by the tool).

## 4. Chains (Linking it all together)
LangChain uses the pipe operator (`|`) to create a "chain" of operations.

**Code Reference:** `src/agents/nodes.py`
```python
chain = prompt | get_llm() | StrOutputParser()
```
1.  `prompt`: Formats the input variables into a full prompt string.
2.  `get_llm()`: Sends that prompt to GPT-4o and gets a response object.
3.  `StrOutputParser()`: Extracts just the text content from the response object (e.g., removing metadata).

---
**Next**: [3. Orchestration: LangGraph](./3_Orchestration_LangGraph.md)
