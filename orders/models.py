from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid
from store.models import ProductVariant

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', _('Pending')),
        ('confirmed', _('Confirmed')),
        ('shipped', _('Shipped')),
        ('delivered', _('Delivered')),
        ('cancelled', _('Cancelled')),
    )

    tracking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    iphone_number = models.CharField(max_length=20) # 'iPhone' from prompt "tell me what u want" -> likely just phone number
    address = models.TextField()
    city = models.CharField(max_length=100)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Simple payment tracking
    is_paid = models.BooleanField(default=False)
    payment_metadata = models.JSONField(default=dict, blank=True) # For Paymob response

    def __str__(self):
        return f"Order {self.tracking_id} - {self.full_name}"

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Snapshot of price at time of order
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.variant}"

    def get_cost(self):
        return self.price * self.quantity

class Invoice(models.Model):
    order = models.OneToOneField(Order, related_name='invoice', on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to='invoices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for {self.order.tracking_id}"
