from django.contrib import admin
from .models import Product, HarvestBatch, DeliveryZone, DeliveryWindow

# Register your models here.
admin.site.register(Product)
admin.site.register(HarvestBatch)
admin.site.register(DeliveryZone)
admin.site.register(DeliveryWindow)