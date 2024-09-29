from django.urls import path
from .views import SubmitFeedbackView, FeedbackListView, EditFeedbackView, DeleteFeedbackView, FeedbackNotificationListView

urlpatterns = [
    path('submit/<int:event_id>/', SubmitFeedbackView.as_view(), name='submit-feedback'),
    path('event/<int:event_id>/feedbacks/', FeedbackListView.as_view(), name='event-feedbacks'),
    path('edit/<int:pk>/', EditFeedbackView.as_view(), name='edit-feedback'),
    path('delete/<int:pk>/', DeleteFeedbackView.as_view(), name='delete-feedback'),
    path('notifications/', FeedbackNotificationListView.as_view(), name='feedback-notifications'),
]