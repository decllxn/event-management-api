from rest_framework import serializers
from .models import Feedback, FeedbackNotification

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']


class FeedbackNotificationSerializer(serializers.ModelSerializer):
    feedback = FeedbackSerializer()

    class Meta:
        model = FeedbackNotification
        fields = '__all__'