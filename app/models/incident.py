from dataclasses import dataclass
from typing import Optional


@dataclass
class IncidentRequest:
    """Data model for incoming incident request."""
    incidentText: str
    
    def validate(self) -> tuple[bool, Optional[str]]:
        """
        Validate the incident request.
        Returns: (is_valid, error_message)
        """
        if not self.incidentText:
            return False, "incidentText cannot be empty"
        
        if not isinstance(self.incidentText, str):
            return False, "incidentText must be a string"
        
        if len(self.incidentText.strip()) == 0:
            return False, "incidentText cannot be only whitespace"
        
        if len(self.incidentText) > 10000:
            return False, "incidentText is too long (max 10000 characters)"
        
        return True, None


@dataclass
class IncidentResponse:
    """Data model for incident response."""
    customerMessage: str
    internalMessage: str

