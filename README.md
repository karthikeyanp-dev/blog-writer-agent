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

### Run the Agent (CLI)

Run the agent to generate new blog posts:

```bash
python main.py
```

Follow the prompts to enter a blog topic. The agent will generate a blog post (saved to `blog_post.md`) and an image (saved to `blog_image.png`).

### Web Interface (Backend & Frontend)

You can view the generated documentation and blog posts using the provided web interface.

#### 1. Start the Backend API

The backend serves markdown files from the `docs/` directory and handles blog post generation.

```bash
# Make sure your virtual environment is activated
uvicorn api:app --reload
```
or
```bash
python -m uvicorn api:app --reload
```

The API will run at `http://127.0.0.1:8000`.
- API Docs: `http://127.0.0.1:8000/docs`
- List Posts: `http://127.0.0.1:8000/posts`
- Generate Post: `POST http://127.0.0.1:8000/generate`

#### 2. Open the Frontend

Simply open the `frontend/index.html` file in your web browser. You can do this by double-clicking the file or dragging it into your browser window.

The frontend allows you to:
- View existing blog posts.
- **Create new blog posts** by entering a topic. The agent will research, write, and generate an image.
- **Download** the generated markdown file.

#### Adding New Posts

To add a new post to be served by the system, simply create a new `.md` file in the `docs/` directory. The API will automatically pick it up.
Alternatively, use the "New Post" button in the frontend to generate one.
