import requests
from app.config import Config


class DatabaseService:
    """Service for interacting with Parse Server/SashiDo."""
    
    def __init__(self):
        """Initialize Parse Server connection."""
        self.app_id = Config.PARSE_APPLICATION_ID
        self.rest_api_key = Config.PARSE_REST_API_KEY
        self.server_url = Config.PARSE_SERVER_URL
        
        if not all([self.app_id, self.rest_api_key, self.server_url]):
            raise ValueError("Parse Server configuration is incomplete")
        
        # Ensure server URL ends with /parse
        if not self.server_url.endswith('/parse'):
            if self.server_url.endswith('/'):
                self.server_url = self.server_url.rstrip('/') + '/parse'
            else:
                self.server_url = self.server_url + '/parse'
    
    def save_incident_message(self, incident_text: str, customer_message: str, internal_message: str) -> str:
        """
        Save incident message to Parse Server.
        
        Args:
            incident_text: Original incident description
            customer_message: Generated customer message
            internal_message: Generated internal message
            
        Returns:
            Object ID of the saved record
        """
        url = f"{self.server_url}/classes/{Config.SASHIDO_INCIDENT_CLASS}"
        
        headers = {
            "X-Parse-Application-Id": self.app_id,
            "X-Parse-REST-API-Key": self.rest_api_key,
            "Content-Type": "application/json"
        }
        
        data = {
            "incidentText": incident_text,
            "customerMessage": customer_message,
            "internalMessage": internal_message
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            response.raise_for_status()
            
            result = response.json()
            object_id = result.get("objectId")
            
            if not object_id:
                raise Exception("Parse Server did not return objectId")
            
            return object_id
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to save to Parse Server: {str(e)}")
        except Exception as e:
            raise Exception(f"Database error: {str(e)}")


def get_db_service() -> DatabaseService:
    """Get or create database service instance."""
    return DatabaseService()

