from django.db import models
from users.models import User
from events.models import Event

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('event', 'Event'),
        ('system', 'System'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, blank=True, null=True, related_name='notifications')
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    message = models.TextField
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.notification_type} - {self.is_read}'

