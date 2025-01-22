from typing import Dict, Any, List
import torch
from diffusers import StableDiffusionPipeline
from ..config.settings import TOOL_CONFIG, MODEL_CONFIG

class ContentCreator:
    def __init__(self):
        self.config = TOOL_CONFIG["content_creation"]
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.image_model = self._initialize_image_model()
        
    def create_content(
        self,
        prompt: str,
        platform: str,
        content_type: str = "text",
        additional_context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Create content for social media
        """
        try:
            content = {
                "platform": platform,
                "type": content_type,
                "original_prompt": prompt
            }
            
            # Generate platform-specific content
            if content_type == "text":
                content.update(self._create_text_content(prompt, platform))
            elif content_type == "image":
                content.update(self._create_image_content(prompt))
            
            # Add metadata
            content["metadata"] = self._get_metadata(platform, content_type)
            
            return content
            
        except Exception as e:
            raise Exception(f"Error creating content: {str(e)}")
    
    def _initialize_image_model(self) -> StableDiffusionPipeline:
        """
        Initialize Stable Diffusion model
        """
        model_id = MODEL_CONFIG["image"]["model_name"]
        pipe = StableDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        ).to(self.device)
        return pipe
    
    def _create_text_content(
        self,
        prompt: str,
        platform: str
    ) -> Dict[str, str]:
        """
        Create platform-specific text content
        """
        # Apply platform-specific formatting
        if platform == "twitter":
            content = self._format_for_twitter(prompt)
        elif platform == "instagram":
            content = self._format_for_instagram(prompt)
        elif platform == "linkedin":
            content = self._format_for_linkedin(prompt)
        else:
            content = prompt
            
        return {"text": content}
    
    def _create_image_content(self, prompt: str) -> Dict[str, Any]:
        """
        Generate image using Stable Diffusion
        """
        image = self.image_model(
            prompt,
            num_inference_steps=30,
            guidance_scale=7.5
        ).images[0]
        
        return {
            "image": image,
            "prompt_used": prompt
        }
    
    def _format_for_twitter(self, text: str) -> str:
        """
        Format content for Twitter
        """
        # Truncate to Twitter's limit
        max_length = 280
        if len(text) > max_length:
            text = text[:max_length-3] + "..."
        return text
    
    def _format_for_instagram(self, text: str) -> str:
        """
        Format content for Instagram
        """
        # Add hashtags and format
        hashtags = self._generate_hashtags(text)
        return f"{text}\n\n{hashtags}"
    
    def _format_for_linkedin(self, text: str) -> str:
        """
        Format content for LinkedIn
        """
        # Add professional formatting
        return f"{text}\n\n#professional #networking"
    
    def _generate_hashtags(self, text: str) -> str:
        """
        Generate relevant hashtags from text
        """
        # Simple hashtag generation (replace with more sophisticated logic)
        words = text.lower().split()[:5]
        hashtags = [f"#{word}" for word in words if len(word) > 3]
        return " ".join(hashtags)
    
    def _get_metadata(self, platform: str, content_type: str) -> Dict[str, Any]:
        """
        Generate metadata for the content
        """
        return {
            "platform": platform,
            "content_type": content_type,
            "timestamp": self._get_timestamp(),
            "version": "1.0"
        }
    
    def _get_timestamp(self) -> float:
        """
        Get current timestamp
        """
        from datetime import datetime
        return datetime.now().timestamp() 