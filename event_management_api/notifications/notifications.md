# Notifications App Documentation

## Overview

The Notifications app provides users with in-app notifications for events and system-related updates. Notifications can be user-specific and are delivered in real-time. The app also supports creating, listing, marking as read, and deleting notifications. Future enhancements may include email and push notifications.

---

## Features

1. **Event Notifications**: Users are notified of event-related updates (e.g., event registrations, cancellations).
2. **User-Specific Notifications**: Each user has a personalized notification feed.
3. **In-App Notifications**: Notifications are delivered directly within the application.
4. **Create Notifications**: Notifications can be created programmatically (e.g., when an event is created, or system events occur).
5. **List Notifications**: Users can view all their notifications.
6. **Mark as Read**: Users can mark individual notifications as read.
7. **Unread Count**: An unread notifications count can be displayed to users.
8. **Notification Preferences (Upcoming)**: Users can manage their notification preferences (e.g., enable/disable event notifications).
9. **Email Notifications (Upcoming)**: Optional email notifications can be sent for critical updates.
10. **Push Notifications (Upcoming)**: Support for push notifications via external services.

---

## Model

The `Notification` model is used to store notifications in the database.

```python
from django.db import models
from django.contrib.auth import get_user_model
from events.models import Event

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('event', 'Event'),
        ('system', 'System'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True, related_name='notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.notification_type} - {self.is_read}"
