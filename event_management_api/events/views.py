from rest_framework import generics, status
from .models import EventCategory, Registration, Event
from .serializers import EventCategorySerializer, EventParticipantSerializer, EventSerializer, RegistrationSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission
from . import models
from django.utils import timezone
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class EventCategoryListView(generics.ListAPIView):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [IsAuthenticated]

class EventFilterByCategoryView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Event.objects.filter(category_id=category_id)


# Event creation view
class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


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
        serializer.save(is_canceled=True)

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
        return obj.organizer == request.user
    

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
    

class PastEventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(date__lt=timezone.now())
    

class UpcomingEventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(date_gte=timezone.now())
    

class UserCreatedEventsListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Event.objects.filter(creator=self.request.user)
    

class EventParticipantManageView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsCreator]
    queryset = Event.objects.all()

    def get(self, request, pk):
        """View participants"""
        event = get_object_or_404(Event, pk=pk)
        participants = Registration.objects.filter(event=event)
        serializer = RegistrationSerializer(participants, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        """Add participant"""
        event = get_object_or_404(Event, pk=pk)
        user = request.data.get('user_id')
        Registration.objects.create(user_id=user, event=event)
        return Response({'message': 'User added'}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """Remove participant"""
        event = get_object_or_404(Event, pk=pk)
        user = request.data.get('user_id')
        rsvp = get_object_or_404(Registration, user_id=user, event=event)
        rsvp.delete()
        return Response({'message': 'User removed'}, status=status.HTTP_204_NO_CONTENT)  
