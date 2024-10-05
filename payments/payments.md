# Payments App Documentation

## Overview

The `payments` app manages all payment-related functionalities for events in the Event Management system. It supports integration with payment gateways such as Stripe and PayPal. Additionally, it handles discount codes, refunds, and cancellations, making the payment process smooth and user-friendly.

### Key Features:
1. **Payment Gateway Integration**: Support for Stripe and PayPal for paid event bookings.
2. **Discount Codes**: Event organizers can create and apply discount codes.
3. **Refunds & Cancellations**: Allows users to request refunds for canceled tickets or events.

---

## Models

### 1. `Payment`
Represents a payment made by a user for an event.

- **Fields**:
  - `user`: The user who made the payment.
  - `event`: The event for which the payment was made.
  - `amount`: The total amount paid.
  - `payment_method`: Method of payment (`stripe`, `paypal`).
  - `payment_status`: Status of the payment (`completed`, `failed`).
  - `created_at`: Timestamp of when the payment was made.

### 2. `DiscountCode`
Represents a discount code that can be applied to reduce the cost of event tickets.

- **Fields**:
  - `code`: The discount code string.
  - `discount_percent`: The percentage discount.
  - `is_valid`: Boolean field indicating if the code is valid.
  - `used_count`: Number of times the code has been used.

### 3. `Refund`
Represents a refund request for a payment.

- **Fields**:
  - `payment`: Reference to the `Payment` model.
  - `amount`: Amount of the refund.
  - `refund_status`: Status of the refund (`requested`, `completed`).
  - `created_at`: Timestamp of when the refund request was created.

---

## Serializers

We created serializers to handle the serialization of data related to payments, discount codes, and refunds.

### 1. `PaymentSerializer`

Used to serialize payment data for API responses.

```python
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'event', 'amount', 'payment_method', 'payment_status', 'created_at']