from django.db import models
from events.models import Event
from users.models import User

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, related_name='feedbacks', on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.IntegerField(default=0)
    anonymous = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Feedback from {'Anonymous' if self.anonymous else self.user.username} for {self.event.name}"
    
    @property
    def display_user(self):
        return 'Anonymous' if self.anonymous else self.user.username
    

class FeedbackNotification(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for feedback on {self.event.name}"