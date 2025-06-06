from rest_framework.permissions import BasePermission

class IsOwnerOrParticipant(BasePermission):
    """
    Custom permission to only allow owners or participants to access their messages/conversations
    """
    def has_object_permission(self, request, view, obj):
        # For messages
        if hasattr(obj, 'sender'):
            return obj.sender == request.user or request.user in obj.conversation.participants.all()
        
        # For conversations
        if hasattr(obj, 'participants'):
            return request.user in obj.participants.all()
        
        return False