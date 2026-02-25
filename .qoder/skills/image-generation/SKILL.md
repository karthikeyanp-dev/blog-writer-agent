---
name: image-generation
description: Configure DALL-E image generation and prompt engineering for blog images. Use when modifying image generation, changing image models, or adjusting prompt_node behavior.
---

# Image Generation

## Implementation

Image tool: `src/tools/image.py`
Prompt node: `src/agents/nodes.py` (prompt_node)
Image node: `src/agents/nodes.py` (image_node)

## Current Flow

1. `prompt_node`: LLM generates image prompt from blog content
2. `image_node`: DALL-E generates image from prompt
3. `main.py`: Downloads and saves image, inserts markdown into blog

## DALL-E Configuration

In `src/tools/image.py`:

```python
dalle = DallEAPIWrapper(model=settings.image_model_name)
```

Default model: `dall-e-3`
Alternative: `dall-e-2`

## Image Prompt Generation

Current prompt template in `prompt_node()`:

```python
("user", "Create a detailed and creative image prompt for a blog post about '{topic}'...")
```

Constraints:
- Keep under 1000 characters (DALL-E limit)
- Uses first 500 chars of blog as context

## Changing Image Style

Modify system prompt in `prompt_node()` to specify:
- Art style (photorealistic, illustration, 3D render)
- Mood (professional, vibrant, minimalist)
- Composition (wide banner, square, portrait)

## Image Placement

In `src/main.py`, image is inserted:
- After the H1 title (`# Title`)
- As markdown: `![Blog Image](blog_image.png)`
- Full width (no size constraints)

## Saving Images

`save_image_from_url()` in `src/utils/files.py`:
- Downloads from DALL-E URL
- Saves as PNG
- Filename from `settings.image_filename`
