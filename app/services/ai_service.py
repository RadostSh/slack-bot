import json
import google.generativeai as genai
from app.config import Config
from app.models.incident import IncidentResponse


def get_incident_response_schema() -> dict:
    """
    Define JSON schema for structured output from Gemini API.
    
    Returns:
        JSON schema dictionary for IncidentResponse structure
    """
    return {
        "type": "object",
        "properties": {
            "customerMessage": {
                "type": "string",
                "description": "Customer-facing message for status page (professional, clear, reassuring)"
            },
            "internalMessage": {
                "type": "string",
                "description": "Internal message for support team (concise, technical, actionable)"
            }
        },
        "required": ["customerMessage", "internalMessage"]
    }


class AIService:
    """Service for interacting with Gemini API."""
    
    def __init__(self):
        """Initialize Gemini client."""
        api_key = Config.GEMINI_API_KEY
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")
        genai.configure(api_key=api_key)
        system_instruction = "You are a professional incident communicator. Always respond with valid JSON containing customerMessage and internalMessage fields."
        self.model = genai.GenerativeModel(
            Config.GEMINI_MODEL,
            system_instruction=system_instruction
        )
    
    def generate_incident_messages(self, incident_text: str) -> IncidentResponse:
        """
        Generate customer and internal messages from incident text.
        
        Args:
            incident_text: Raw incident description
            
        Returns:
            IncidentResponse dataclass with customerMessage and internalMessage
            
        Raises:
            Exception: If Gemini API call fails
        """
        prompt = f"""Based on the following incident description, generate TWO distinct messages:

1. A customer-facing message for a status page (professional, clear, reassuring, appropriate for public communication)
2. An internal message for the support team (concise, technical, actionable)

Incident Description:
{incident_text}

Ensure both messages are distinct and appropriate for their respective audiences."""

        try:
            # Get JSON schema for structured output
            response_schema = get_incident_response_schema()
            
            # Configure generation parameters with structured output
            generation_config = genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=500,
                response_mime_type="application/json",
                response_schema=response_schema
            )
            
            # Generate content with structured output
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            # Parse structured JSON response
            content = response.text.strip()
            parsed = json.loads(content)
            
            customer_message = parsed.get("customerMessage", "")
            internal_message = parsed.get("internalMessage", "")
            
            if not customer_message or not internal_message:
                raise ValueError("Missing required fields in AI response")
            
            return IncidentResponse(
                customerMessage=customer_message,
                internalMessage=internal_message
            )
                
        except json.JSONDecodeError as e:
            raise Exception(f"Failed to parse structured JSON response: {str(e)}")
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")


def get_ai_service() -> AIService:
    """Get or create AI service instance."""
    return AIService()

