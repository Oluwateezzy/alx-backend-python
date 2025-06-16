import logging
from datetime import datetime

# Set up logging
logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Get the user (or 'Anonymous' if not authenticated)
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        
        # Log the request information
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        
        # Process the request and get the response
        response = self.get_response(request)
        
        return response