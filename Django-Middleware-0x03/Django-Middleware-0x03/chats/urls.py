from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(conversations_router.urls)),
    path('', include(router.urls)),
]