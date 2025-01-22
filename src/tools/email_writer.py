from typing import Dict, Any, Optional
from pathlib import Path
import json
from ..config.settings import TOOL_CONFIG

class EmailWriter:
    def __init__(self):
        self.config = TOOL_CONFIG["email"]
        self.templates_path = Path(self.config["templates_path"])
        self.templates = self._load_templates()
        
    def compose_email(
        self,
        context: Dict[str, Any],
        template_name: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Compose an email based on context and optional template
        """
        try:
            # Get base template if specified
            template = self._get_template(template_name) if template_name else ""
            
            # Extract relevant information from context
            subject = self._generate_subject(context)
            body = self._generate_body(context, template)
            
            return {
                "subject": subject,
                "body": body,
                "metadata": self._get_metadata(context)
            }
            
        except Exception as e:
            raise Exception(f"Error composing email: {str(e)}")
    
    def _load_templates(self) -> Dict[str, str]:
        """
        Load email templates from files
        """
        templates = {}
        if self.templates_path.exists():
            for template_file in self.templates_path.glob("*.txt"):
                templates[template_file.stem] = template_file.read_text()
        return templates
    
    def _get_template(self, template_name: str) -> str:
        """
        Get specific template by name
        """
        return self.templates.get(template_name, "")
    
    def _generate_subject(self, context: Dict[str, Any]) -> str:
        """
        Generate email subject based on context
        """
        intent = context.get("intent", "")
        topic = context.get("topic", "")
        return f"{intent.capitalize()}: {topic.capitalize()}"
    
    def _generate_body(self, context: Dict[str, Any], template: str) -> str:
        """
        Generate email body using context and template
        """
        # Start with greeting
        body_parts = [self._generate_greeting(context)]
        
        # Add main content
        content = template.format(**context) if template else context.get("content", "")
        body_parts.append(content)
        
        # Add signature
        body_parts.append(self._generate_signature(context))
        
        return "\n\n".join(body_parts)
    
    def _generate_greeting(self, context: Dict[str, Any]) -> str:
        """
        Generate appropriate greeting
        """
        recipient = context.get("recipient_name", "")
        return f"Dear {recipient}," if recipient else "Hello,"
    
    def _generate_signature(self, context: Dict[str, Any]) -> str:
        """
        Generate email signature
        """
        sender = context.get("sender_name", "AI Assistant")
        return f"Best regards,\n{sender}"
    
    def _get_metadata(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate metadata for the email
        """
        return {
            "type": "email",
            "priority": context.get("priority", "normal"),
            "category": context.get("category", "general"),
            "timestamp": self._get_timestamp()
        }
    
    def _get_timestamp(self) -> float:
        """
        Get current timestamp
        """
        from datetime import datetime
        return datetime.now().timestamp() 