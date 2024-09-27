from rest_framework import generics
from .models import Registration, Event
from .serializers import EventParticipantSerializer, EventSerializer, RegistrationSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from . import models

# Event creation view
class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Allowing Users to view a list of events
class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]


class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

class EventCancelView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(is_cancelled=True)

# Event RSVP (Registration) View
class EventRegisterView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        event_id = self.kwargs['pk']
        event = Event.objects.get(pk=event_id)
        serializer.save(event=event, user=self.request.user)

class IsCreator(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
    

# Event Update
# Only creator can update the event
class EventUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsCreator]


# Event Deletion
# Only the creator can delete the event
class EventDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsCreator]


class EventParticipantListView(generics.ListAPIView):
    serializer_class = EventParticipantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['pk']
        return Registration.objects.filter(event_id=event_id)
    

# Allow Users to search events based on name or location
class EventSearchView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        return Event.objects.filter(
            models.Q(name__icontains=query | models.Q(location__icontains=query))
        )
    