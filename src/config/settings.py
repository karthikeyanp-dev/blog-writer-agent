from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os

class Settings(BaseSettings):
    """
    Application settings and configuration.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    openai_api_key: str = Field(..., description="OpenAI API Key")
    tavily_api_key: str = Field(..., description="Tavily API Key")
    
    # Model Configuration
    model_name: str = Field("gpt-5-nano", description="Main LLM model name")
    image_model_name: str = Field("dall-e-3", description="Image generation model name")
    temperature: float = Field(0.7, description="LLM temperature")
    
    # Output Configuration
    output_dir: str = Field(".", description="Directory to save outputs")
    blog_filename: str = Field("blog_post.md", description="Blog post filename")
    image_filename: str = Field("blog_image.png", description="Image filename")

    def get_output_path(self, filename: str) -> str:
        return os.path.join(self.output_dir, filename)

settings = Settings()
