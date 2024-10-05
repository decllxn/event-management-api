from rest_framework import serializers
from .models import Ticket, TicketType

class TicketTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketType
        field = ['id', 'name', 'price', 'available_quantity']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = [
            'id',
            'event',
            'ticket_type',
            'is_reserved',
            'qr_code',
            'pdf_ticket'
        ]