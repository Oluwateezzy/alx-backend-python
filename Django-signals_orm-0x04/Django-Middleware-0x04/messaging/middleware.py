from collections import defaultdict
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

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Store request counts and timestamps per IP
        self.request_counts = defaultdict(list)
        # Rate limit configuration
        self.limit = 5  # 5 messages
        self.window = 60  # 60 seconds (1 minute)

    def __call__(self, request):
        # Only process POST requests to chat endpoints
        if request.method == 'POST' and request.path.startswith('/chat/'):
            ip_address = self.get_client_ip(request)
            current_time = time.time()
            
            # Clean up old timestamps
            self.request_counts[ip_address] = [
                t for t in self.request_counts[ip_address] 
                if current_time - t < self.window
            ]
            
            # Check if limit exceeded
            if len(self.request_counts[ip_address]) >= self.limit:
                return HttpResponseForbidden(
                    "Rate limit exceeded: 5 messages per minute allowed. Please wait."
                )
            
            # Record this request
            self.request_counts[ip_address].append(current_time)
        
        return self.get_response(request)
    
    def get_client_ip(self, request):
        """Get the client's IP address from request headers"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define protected paths and required roles
        self.protected_paths = {
            '/admin/actions/': ['admin'],
            '/moderate/': ['admin', 'moderator'],
            '/api/restricted/': ['admin']
        }

    def __call__(self, request):
        current_path = request.path
        
        # Check if current path requires special permissions
        for path, required_roles in self.protected_paths.items():
            if current_path.startswith(path):
                # Check if user is authenticated
                if not request.user.is_authenticated:
                    return HttpResponseForbidden("Authentication required")
                
                # Check if user has any of the required roles
                user_role = self.get_user_role(request.user)
                if user_role not in required_roles:
                    return HttpResponseForbidden("Insufficient permissions")
                
                break
        
        return self.get_response(request)
    
    def get_user_role(self, user):
        """
        Get the user's role from their profile or groups
        You may need to customize this based on your user role implementation
        """
        if user.is_superuser:
            return 'admin'
        
        # Example: Check groups (common implementation)
        if user.groups.filter(name='Moderators').exists():
            return 'moderator'
        
        # Default role for regular users
        return 'user'