---
name: project-configuration
description: Manage environment variables, API keys, and application settings for the blog writer agent. Use when modifying config, adding new settings, or troubleshooting setup issues.
---

# Project Configuration

## Settings Location

Main config: `src/config/settings.py`
Environment file: `.env` (create from `.env.example`)

## Required Environment Variables

```bash
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
```

## Available Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `openai_api_key` | required | OpenAI API key |
| `tavily_api_key` | required | Tavily search API key |
| `model_name` | gpt-4o-mini | Main LLM model |
| `image_model_name` | dall-e-3 | Image generation model |
| `temperature` | 0.7 | LLM creativity (0-1) |
| `output_dir` | . | Output directory |
| `blog_filename` | blog_post.md | Blog output filename |
| `image_filename` | blog_image.png | Image output filename |

## Adding New Settings

1. Add field to `Settings` class in `settings.py`:
   ```python
   new_setting: str = Field("default", description="What it does")
   ```

2. Optionally add to `.env.example` for documentation

3. Access via `settings.new_setting`

## Changing Output Location

Set in `.env`:
```bash
output_dir=./output
blog_filename=my_blog.md
```

Or modify defaults in `settings.py`.

## Model Configuration

Available models for `model_name`:
- `gpt-4o-mini` (default, cost-effective)
- `gpt-4o` (higher quality)
- `gpt-3.5-turbo` (legacy)

Temperature guide:
- `0.1-0.3`: Factual, consistent
- `0.5-0.7`: Balanced (default)
- `0.8-1.0`: Creative, varied
