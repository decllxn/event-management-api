from rest_framework import serializers
from .models import Event, EventCategory, Registration

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ('id', 'name', 'description')

class EventSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=EventCategory.objects.all())

    class Meta:
        model = Event
        fields = '__all__'

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'
    
# Participants who have RSVP'd to a particular event
class EventParticipantSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Registration
        fields = ['user', 'created_at']