from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Feedback, FeedbackNotification
from .serializers import FeedbackSerializer, FeedbackNotificationSerializer
from events.models import Event

class SubmitFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            feedback = serializer.save(user=request.user, event=event)
            # Notify the event organizer
            FeedbackNotification.objects.create(event=event, organizer=event.organizer, feedback=feedback)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FeedbackListView(generics.ListAPIView):
    serializer_class = FeedbackSerializer

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return Feedback.objects.filter(event_id=event_id)

class EditFeedbackView(generics.UpdateAPIView):
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)

class DeleteFeedbackView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Feedback.objects.filter(user=self.request.user)

class FeedbackNotificationListView(generics.ListAPIView):
    serializer_class = FeedbackNotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FeedbackNotification.objects.filter(organizer=self.request.user, is_read=False)