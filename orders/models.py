from django.db import models
from products.models import Product, HarvestBatch, DeliveryWindow

# Create your models here.
class Customer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=50)
    whatsapp_number = models.CharField(max_length=50, blank=True, null=True)
    address = models.CharField(max_length=255)
    landmark = models.CharField(max_length=160, blank=True, null=True)

    class Meta:
        db_table = 'customers'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Order(models.Model):
    STATUS = [
        ("placed", "Placed"),
        ("confirmed", "Confirmed"),
        ("packed", "Packed"),
        ("out_for_delivery", "Out for delivery"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("cod", "Cash on Delivery"),
        ("failed", "Failed"),
        ("refunded", "Refunded"),
    ]
    PAYMENT_METHOD = [
        ("ecocash", "EcoCash"),
        ("zipit", "ZIPIT"),
        ("bank", "Bank Transfer"),
        ("cash", "Cash"),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    window = models.ForeignKey(DeliveryWindow, on_delete=models.PROTECT)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=50, choices=STATUS, default="placed")
    payment_status = models.CharField(max_length=50, choices=PAYMENT_STATUS, default="pending")
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD, default="cod")
    payment_ref = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
    
    def __str__(self):
        return f"Order #{self.id} for {self.customer.first_name} {self.customer.last_name}"
    
    def update_total_price(self):
        """Recalculate total_price from items."""
        self.total_price = sum(item.quantity * item.unit_price for item in self.items.all())
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    batch = models.ForeignKey(HarvestBatch, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'order_items'
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
