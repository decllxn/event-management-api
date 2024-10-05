from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),

    # users app
    path('users/', include('users.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Events
    path('events/', include('events.urls')),

    # Notification
    path('notifications/', include('notifications.urls')),

    # Tickets
    path('tickets/', include('tickets.urls')),

    # Payments
    path('payments/', include('payments.urls')),

    # Feedback
    path('feedback/', include('feedback.urls')),
]