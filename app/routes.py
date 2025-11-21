import logging
from flask import Blueprint, request, jsonify
from app.models.incident import IncidentRequest
from app.services.ai_service import get_ai_service
from app.services.db_service import get_db_service

logger = logging.getLogger(__name__)

incident_bp = Blueprint('incident', __name__)


@incident_bp.route('/incident-handler', methods=['POST'])
def incident_handler():
    """
    Handle incident text and generate customer/internal messages.
    
    Expected request body:
    {
        "incidentText": "Description of the incident"
    }
    
    Returns:
    {
        "customerMessage": "Message for customers",
        "internalMessage": "Message for internal team"
    }
    """
    try:
        # Parse and validate request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body must be JSON'}), 400
        
        incident_request = IncidentRequest(incidentText=data.get('incidentText', ''))
        is_valid, error_message = incident_request.validate()
        
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        incident_text = incident_request.incidentText
        
        # Generate messages using AI
        try:
            ai_service = get_ai_service()
            response = ai_service.generate_incident_messages(incident_text)
        except Exception as e:
            logger.error(f"AI service error: {str(e)}")
            return jsonify({'error': f'Failed to generate messages: {str(e)}'}), 500
        
        # Save to database
        try:
            db_service = get_db_service()
            object_id = db_service.save_incident_message(incident_text, response.customerMessage, response.internalMessage)
            logger.info(f"Saved incident message with ID: {object_id}")
        except Exception as e:
            logger.error(f"Database service error: {str(e)}")
            # Continue even if database save fails - return messages anyway
            logger.warning("Returning messages despite database save failure")
        
        # Return response
        return jsonify({
            'customerMessage': response.customerMessage,
            'internalMessage': response.internalMessage
        }), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in incident_handler: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

