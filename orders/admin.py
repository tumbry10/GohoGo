from django.contrib import admin
from .models import Customer, Order, OrderItem

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'window', 'total_price', 'payment_status', 'status', 'created_at')
    list_filter = ('status', 'payment_status', 'window')
    search_fields = ('customer__full_name', 'customer__phone')
    inlines = [OrderItemInline]

admin.site.register(Customer)
