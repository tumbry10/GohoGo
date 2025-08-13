from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    unit_label = models.CharField(max_length=50, default='dozen')
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
    
    def __str__(self):
        return self.name

class HarvestBatch(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    label = models.CharField(max_length=255)
    harvest_date = models.DateField()
    total_quantity = models.PositiveIntegerField()
    quantity_available = models.PositiveIntegerField()
    price_override = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'harvest_batches'
    
    def __str__(self):
        return f'{self.label} ({self.product.name}) harvested on {self.harvest_date}'

class DeliveryZone(models.Model):
    name = models.CharField(max_length=255)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    whatsapp_group_name = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'delivery_zones'
    
    def __str__(self):
        return self.name
    
class DeliveryWindow(models.Model):
    batch = models.ForeignKey(HarvestBatch, on_delete=models.CASCADE)
    zone = models.ForeignKey(DeliveryZone, on_delete=models.PROTECT)
    delivery_date = models.DateField()
    cutoff_at = models.DateTimeField()
    max_orders = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'delivery_windows'
    
    def __str__(self):
        return f'{self.batch.label} for {self.zone.name} on {self.delivery_date}'

