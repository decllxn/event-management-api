from django.urls import path
from .views import PaymentView, ApplyDiscountView, RefundRequestView

urlpatterns = [
    path('pay/<int:event_id>/', PaymentView.as_view(), name='event-payment'),
    path('apply-discount/', ApplyDiscountView.as_view(), name='apply-discount'),
    path('refund/<int:payment_id>/', RefundRequestView.as_view(), name='request-refund'),
]
