from rest_framework import serializers
from .models import Payment, DiscountCode, Refund

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'event', 'amount', 'payment_method', 'payment_status', 'created_at']

class DiscountCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountCode
        fields = ['code', 'discount_percent', 'is_valid', 'used_count']

class RefundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Refund
        fields = ['id', 'payment', 'amount', 'refund_status', 'created_at']
