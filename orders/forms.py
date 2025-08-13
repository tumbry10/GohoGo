from django import forms
from django.forms import inlineformset_factory
from .models import Customer, OrderItem, Order


PAYMENT_METHOD_CHOICES = [
    ('ecocash', 'EcoCash'),
    ('zipit', 'ZIPIT'),
    ('bank', 'Bank Transfer'),
    ('cash', 'Cash on Delivery'),
]

class PublicOrderForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices=PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'phone_number', 'whatsapp_number', 'address', 'landmark']

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

OrderItemFormSet = inlineformset_factory(
    Order,
    OrderItem,
    form=OrderItemForm,
    extra=1,  # default rows
    can_delete=True
)