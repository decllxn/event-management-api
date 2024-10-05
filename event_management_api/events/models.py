from django.db import models
from users.models import User

class EventCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    is_canceled = models.BooleanField(default=False)
    category = models.ForeignKey(EventCategory, on_delete=models.SET_NULL, null=True, related_name='events', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def average_rating(self):
        feedbacks = self.feedbacks.all()
        if feedbacks.exists():
            return round(feedbacks.aggregate(models.Avg('rating'))['rating__avg'], 2)
        return None
    
class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} registered for {self.event.name}"