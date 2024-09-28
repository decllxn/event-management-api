from django.urls import path
from .views import TicketTypeListView, TicketCreateView, MyTicketsView, TicketCancelView

urlpatterns = [
    path('event/<int:event_id>/ticket-types/', TicketTypeListView.as_view(), name='ticket-type-list'),
    path('ticket-type/<int:ticket_type_id>/book/', TicketCreateView.as_view(), name='ticket-create'),
    path('my-tickets/', MyTicketsView.as_view(), name='my-tickets'),
    path('ticket/<int:pk>/cancel/', TicketCancelView.as_view(), name='ticket-cancel'),
]