import django_filters
from django_filters import rest_framework as filters
from .models import Message
from django.utils import timezone
from datetime import timedelta

class MessageFilter(filters.FilterSet):
    conversation = filters.CharFilter(field_name='conversation__id')
    sender = filters.CharFilter(field_name='sender__id')
    read = filters.BooleanFilter()
    
    # Date range filters
    start_date = filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    end_date = filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    
    # Last N hours filter
    last_hours = filters.NumberFilter(method='filter_last_hours')
    
    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'read', 'start_date', 'end_date']
    
    def filter_last_hours(self, queryset, name, value):
        try:
            hours = int(value)
            if hours > 0:
                cutoff = timezone.now() - timedelta(hours=hours)
                return queryset.filter(sent_at__gte=cutoff)
        except (ValueError, TypeError):
            pass
        return queryset