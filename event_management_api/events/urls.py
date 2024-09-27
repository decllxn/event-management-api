from django.urls import path
from .views import (
    EventCancelView,
    EventCategoryListView,
    EventCreateView,
    EventDeleteView,
    EventDetailView,
    EventFilterByCategoryView,
    EventListView,
    EventParticipantListView,
    EventParticipantManageView,
    EventRegisterView,
    EventSearchView,
    EventUpdateView,
    PastEventListView,
    UpcomingEventListView,
    UserCreatedEventsListView,
)

urlpatterns = [
    path('create/', EventCreateView.as_view(), name='event-create'),
    path('list/', EventListView.as_view(), name='event-list'),
    path('detail/<int:pk>/', EventDetailView.as_view(), name = 'event-details'),
    path('update/<int:pk>/', EventUpdateView.as_view(), name='event-update'),
    path('delete/<int:pk>/', EventDeleteView.as_view(), name='event-delete'),

    path('register/<int:pk>/', EventRegisterView.as_view(), name='register-event'),
    path('<int:pk>/participants/', EventParticipantListView.as_view(), name='event-participants'),
    path('search/', EventSearchView.as_view(), name='event-search'),
    path('cancel/<int:pk>/', EventCancelView.as_view(), name = 'cancel-event'),
    path('categories/', EventCategoryListView.as_view(), name='event-categories'),
    path('category/<int:category_id>/', EventFilterByCategoryView.as_view(), name='event-filter-category'),
    path('past-events/', PastEventListView.as_view(), name='past-events'),
    path('upcoming-events/', UpcomingEventListView.as_view(), name='upcoming-events'),
    path('my-events/', UserCreatedEventsListView.as_view(), name='user-created-events'),
    path('manage-participants/<int:pk>/', EventParticipantManageView.as_view(), name='manage-participants'),
]