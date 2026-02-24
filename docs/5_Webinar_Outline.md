# 5. Webinar Outline: Building an AI Blog Writer Agent

## **Title**: Build Your First AI Agent with LangGraph & Python

**Duration**: 45-60 Minutes
**Audience**: Developers interested in AI, Python beginners to intermediate.

---

### **1. Introduction (5 mins)**
*   **Hook**: "Imagine having an AI assistant that not only writes for you but researches the web, cites sources, and creates custom images—all automatically."
*   **What we'll build**: A Blog Writer Agent using LangChain and LangGraph.
*   **Key Concepts**:
    *   Agents vs. Chatbots (Autonomy & Tools).
    *   The Power of Graphs (Stateful Workflows).

### **2. The Architecture (10 mins)**
*   **Visual Diagram**: Show the flow:
    `[Start] -> [Research] -> [Write] -> [Prompt] -> [Image] -> [End]`
*   **Why Graph?**: Explain why linear scripts fail for complex tasks (need for loops, conditions, state management).
*   **Tech Stack**:
    *   **Python**: The language of AI.
    *   **LangChain**: The framework for LLM apps.
    *   **LangGraph**: The orchestration layer.
    *   **Tavily**: Search engine for AI.
    *   **OpenAI (GPT-4o & DALL-E 3)**: The intelligence.

### **3. Live Coding / Walkthrough (25 mins)**
*   **Step 1: Setup**:
    *   `pip install langchain langgraph ...`
    *   Explain `.env` and API keys (OpenAI, Tavily).
*   **Step 2: Defining State**:
    *   Show `BlogState` class. Explain `TypedDict`.
    *   "This is the memory our agent passes around."
*   **Step 3: Building Tools**:
    *   Show `src/tools/search.py` (Tavily wrapper).
    *   Show `src/tools/image.py` (DALL-E wrapper).
*   **Step 4: Creating Nodes**:
    *   Walk through `research_node`: Input `topic` -> Output `research_content`.
    *   Walk through `write_node`: The Prompt Template -> LLM Chain.
    *   *Highlight*: The instruction to "include sources" in the prompt.
*   **Step 5: Wiring the Graph**:
    *   Show `create_blog_graph` in `src/agents/graph.py`.
    *   Explain `add_node` and `add_edge`.
    *   "It's like connecting LEGO blocks."
*   **Step 6: Running the Agent**:
    *   Run `python main.py "Future of Remote Work"`.
    *   Show the logs (Researching... Writing... Generating Image...).
    *   Open the final `blog_post.md` and `blog_image.png`.

### **4. Advanced Features & Improvements (10 mins)**
*   **Error Handling**: Show how `try/except` blocks in nodes prevent the whole agent from crashing.
*   **Human-in-the-loop**: Mention how LangGraph allows pausing for human approval (e.g., before publishing).
*   **Switching Models**: How easy it is to swap GPT-4o for Claude 3 or a local Llama 3 model using LangChain.

### **5. Q&A (10 mins)**
*   Common questions: Costs, Rate limits, Local LLMs.

---

### **Resources for Attendees**
*   **GitHub Repo**: [Link to this project]
*   **LangChain Docs**: https://python.langchain.com/
*   **LangGraph Docs**: https://langchain-ai.github.io/langgraph/
