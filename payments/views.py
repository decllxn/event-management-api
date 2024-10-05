from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Payment, DiscountCode, Refund
from .serializers import PaymentSerializer, DiscountCodeSerializer, RefundSerializer
from events.models import Event
import stripe
import paypalrestsdk
from django.conf import settings

class PaymentView(APIView):
    def post(self, request, event_id):
        event = Event.objects.get(id=event_id)
        user = request.user
        amount = request.data.get('amount')
        payment_method = request.data.get('payment_method')

        if payment_method == 'stripe':
            try:
                # Process Stripe Payment
                stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
                stripe_charge = stripe.Charge.create(
                    amount=int(amount * 100),  # Stripe expects amount in cents
                    currency='usd',
                    source=request.data.get('source'),  # Token from Stripe.js
                    description=f"Payment for {event.name} tickets"
                )
                payment_status = 'completed' if stripe_charge['status'] == 'succeeded' else 'failed'

            except stripe.error.StripeError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        elif payment_method == 'paypal':
            try:
                # Process PayPal Payment
                paypalrestsdk.configure({
                    "mode": "sandbox",  # Use "live" for production
                    "client_id": settings.PAYPAL_CLIENT_ID,
                    "client_secret": settings.PAYPAL_SECRET,
                })

                payment = paypalrestsdk.Payment({
                    "intent": "sale",
                    "payer": {
                        "payment_method": "paypal"
                    },
                    "transactions": [{
                        "amount": {
                            "total": str(amount),
                            "currency": "USD"
                        },
                        "description": f"Payment for {event.name} tickets"
                    }],
                    "redirect_urls": {
                        "return_url": "http://localhost:8000/payment/success/",
                        "cancel_url": "http://localhost:8000/payment/cancel/"
                    }
                })

                if payment.create():
                    payment_status = 'completed'
                else:
                    payment_status = 'failed'
                    return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"error": "Invalid payment method"}, status=status.HTTP_400_BAD_REQUEST)

        if payment_status == 'completed':
            payment = Payment.objects.create(user=user, event=event, amount=amount, payment_method=payment_method, payment_status=payment_status)
            
            # Serialize the payment data
            serializer = PaymentSerializer(payment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST)


class ApplyDiscountView(APIView):
    def post(self, request):
        code = request.data.get('code')
        discount_code = DiscountCode.objects.filter(code=code).first()

        if not discount_code or not discount_code.is_valid():
            return Response({"error": "Invalid or expired discount code"}, status=status.HTTP_400_BAD_REQUEST)

        amount = request.data.get('amount')
        discounted_amount = discount_code.apply_discount(amount)
        discount_code.used_count += 1
        discount_code.save()

        # Serialize the discount code data
        discount_serializer = DiscountCodeSerializer(discount_code)
        return Response({
            "discounted_amount": discounted_amount,
            "discount_code": discount_serializer.data
        }, status=status.HTTP_200_OK)


class RefundRequestView(APIView):
    def post(self, request, payment_id):
        payment = Payment.objects.get(id=payment_id)
        refund_amount = payment.amount  # Full refund for now
        refund_status = 'requested'

        refund = Refund.objects.create(payment=payment, amount=refund_amount, refund_status=refund_status)

        # Serialize the refund data
        refund_serializer = RefundSerializer(refund)
        return Response(refund_serializer.data, status=status.HTTP_201_CREATED)