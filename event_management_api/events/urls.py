from django.urls import path
from .views import (
    EventCancelView,
    EventCreateView,
    EventDeleteView,
    EventDetailView,
    EventListView,
    EventParticipantListView,
    EventRegisterView,
    EventSearchView,
    EventUpdateView,
)

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('list/', EventListView.as_view(), name='event-list'),
    path('detail/<int:pk>/', EventDetailView.as_view(), name = 'event-details'),
    path('update/<int:pk>/', EventUpdateView.as_view(), name='event-update'),
    path('delete/<int:pk>/', EventDeleteView.as_view(), name='event-delete'),

    path('register/<int:pk>', EventRegisterView.as_view(), name='register-event'),
    path('<int:pk>/participants/', EventParticipantListView.as_view(), name='event-participants'),
    path('search/', EventSearchView.as_view(), name='event-search'),
    path('cancel/<int:pk>/', EventCancelView.as_view(), name = 'cancel-event')
]