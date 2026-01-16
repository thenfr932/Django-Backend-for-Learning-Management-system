import uuid
from django.db import models
from django.conf import settings

# ==========================
# PAYMENTS & COUPONS
# ==========================

class Coupon(models.Model):
    DISCOUNT_TYPE = [
        ("percent", "Percentage"),
        ("fixed", "Fixed"),
    ]

    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.code


class Payment(models.Model):
    PROVIDER_CHOICES = [
        ("stripe", "Stripe"),
        ("razorpay", "Razorpay"),
        ("paypal", "PayPal"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
        ("expired", "Expired"),
        ("partially_refunded", "Partially Refunded"),
        
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey("courses.Course", on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    provider_payment_id = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment({self.provider_payment_id})"