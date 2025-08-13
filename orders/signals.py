from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderItem

@receiver([post_save, post_delete], sender=OrderItem)
def update_order_total(sender, instance, **kwargs):
    """
    Recalculate order total whenever an OrderItem is saved or deleted.
    """
    order = instance.order
    order.total_price = sum(
        item.quantity * item.unit_price for item in order.items.all()
    )
    order.save(update_fields=["total_price"])
