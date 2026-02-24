# Blog Writer Agent

This is a Python agent that uses LangChain to write blog posts and generate images for them using OpenAI's GPT-4 and DALL-E 3 models.

## Prerequisites

- Python 3.8+
- An OpenAI API Key

## Setup

1.  **Clone the repository** (if you haven't already).
2.  **Navigate to the project directory**:
    ```bash
    cd blog_writer_agent
    ```
3.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```
4.  **Activate the virtual environment**:
    -   Windows: `venv\Scripts\activate`
    -   macOS/Linux: `source venv/bin/activate`
5.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
6.  **Set up your OpenAI API Key**:
    -   Copy the `.env.example` file to `.env`:
        ```bash
        cp .env.example .env
        ```
    -   Open `.env` and replace `your_openai_api_key_here` with your actual OpenAI API key.

## Usage

Run the agent:

```bash
python main.py
```

Follow the prompts to enter a blog topic. The agent will generate a blog post (saved to `blog_post.md`) and an image (saved to `blog_image.png`).
