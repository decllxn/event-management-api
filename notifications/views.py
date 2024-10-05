from rest_framework import generics, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    

# Mark Notification as Read
class MarkNotificationReadView(generics.UpdateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"status": "Notification marked as read"})

# Create Notification
class NotificationCreateView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
