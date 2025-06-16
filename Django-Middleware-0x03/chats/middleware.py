import logging

from datetime import datetime, time
from django.http import HttpResponseForbidden

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

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Define restricted hours (9 PM to 6 AM)
        current_time = datetime.now().time()
        start_time = time(21, 0)  # 9 PM
        end_time = time(6, 0)     # 6 AM
        
        # Check if the current path is the messaging app
        # Update '/messages/' to match your actual messaging URL path
        if request.path.startswith('/messages/'):
            # Check if current time is within restricted hours
            if current_time >= start_time or current_time <= end_time:
                return HttpResponseForbidden(
                    "Messaging is unavailable between 9 PM and 6 AM"
                )
        
        return self.get_response(request)