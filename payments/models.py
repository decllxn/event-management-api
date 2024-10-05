from django.db import models
from users.models import User
from events.models import Event

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=100, choices=(('stripe', 'Stripe'), ('paypal', 'PayPal')))
    payment_status = models.CharField(max_length=50, choices=(('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.user.email} - {self.event.name} - {self.amount}"

class DiscountCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=50, choices=(('percentage', 'Percentage'), ('fixed', 'Fixed')))
    value = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateTimeField()
    usage_limit = models.IntegerField(null=True, blank=True)
    used_count = models.IntegerField(default=0)

    def is_valid(self):
        return self.usage_limit is None or self.used_count < self.usage_limit

    def apply_discount(self, amount):
        if self.discount_type == 'percentage':
            return amount - (amount * (self.value / 100))
        else:
            return amount - self.value

class Refund(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    refund_status = models.CharField(max_length=50, choices=(('requested', 'Requested'), ('processed', 'Processed')))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refund {self.id} - {self.payment.user.email} - {self.payment.event.name} - {self.amount}"
