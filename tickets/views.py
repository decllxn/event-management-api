from rest_framework import generics, status
from rest_framework.response import Response
from .models import Ticket, TicketType
from .serializers import TicketSerializer, TicketTypeSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from events.models import Event

class TicketTypeListView(generics.ListAPIView):
    serializer_class = TicketTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event = get_object_or_404(Event, pk=self.kwargs['event_id'])
        return TicketType.objects.filter(event=event)

class TicketCreateView(generics.CreateAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        ticket_type = get_object_or_404(TicketType, pk=self.kwargs['ticket_type_id'])
        if ticket_type.available_quantity > 0:
            serializer.save(user=self.request.user, ticket_type=ticket_type, event=ticket_type.event)
            ticket_type.available_quantity -= 1
            ticket_type.save()
        else:
            return Response({"detail": "No tickets available"}, status=status.HTTP_400_BAD_REQUEST)

class MyTicketsView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

class TicketCancelView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Ticket, pk=self.kwargs['pk'], user=self.request.user)

    def perform_destroy(self, instance):
        ticket_type = instance.ticket_type
        ticket_type.available_quantity += 1
        ticket_type.save()
        instance.delete()