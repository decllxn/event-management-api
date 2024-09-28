from django.urls import path
from .views import *

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications-list'),
    path('create/', NotificationCreateView.as_view(), name='notifications-create'),
    path('<int:pk>/read/',MarkNotificationReadView.as_view(), name='mark-notification-read'),
]