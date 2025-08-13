from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer, Order, OrderItem
from products.models import Product, DeliveryWindow, DeliveryZone, HarvestBatch
from .forms import PublicOrderForm, OrderItemFormSet

# Create your views here.
'''def public_order_view(request, window_id):
    window = get_object_or_404(DeliveryWindow, id=window_id, batch__is_published=True)

    # Inline formset for order items
    OrderItemFormSetClass = inlineformset_factory(
        Order, OrderItem, fields=('product', 'batch', 'quantity'), extra=1
    )

    if request.method == 'POST':
        customer_form = PublicOrderForm(request.POST)
        if customer_form.is_valid():
            customer, created = Customer.objects.get_or_create(
                first_name=customer_form.cleaned_data['first_name'],
                last_name=customer_form.cleaned_data['last_name'],
                phone_number=customer_form.cleaned_data['phone_number'],
                defaults={
                    'whatsapp_number': customer_form.cleaned_data['whatsapp_number'],
                    'address': customer_form.cleaned_data['address'],
                    'landmark': customer_form.cleaned_data['landmark'],
                }
            )
            order = Order.objects.create(
                customer=customer,
                window=window,
                payment_method=customer_form.cleaned_data['payment_method']
            )
            
            formset = OrderItemFormSetClass(request.POST, instance=order)
            if formset.is_valid():
                formset.save()
                order.update_total_price()
                return redirect('order_success', order_id=order.id)
    else:
        customer_form = PublicOrderForm()
        formset = OrderItemFormSetClass()

    context = {
        'window': window,
        'customer_form': customer_form,
        'formset': formset
    }
    return render(request, 'orders/public_order_form.html', context)'''
def public_order_view(request, window_id):
    window = get_object_or_404(DeliveryWindow, id=window_id, batch__is_published=True)

    if request.method == 'POST':
        customer_form = PublicOrderForm(request.POST)
        if customer_form.is_valid():
            customer, created = Customer.objects.get_or_create(
                first_name=customer_form.cleaned_data['first_name'],
                last_name=customer_form.cleaned_data['last_name'],
                phone_number=customer_form.cleaned_data['phone_number'],
                defaults={
                    'whatsapp_number': customer_form.cleaned_data['whatsapp_number'],
                    'address': customer_form.cleaned_data['address'],
                    'landmark': customer_form.cleaned_data['landmark'],
                }
            )
            order = Order.objects.create(
                customer=customer,
                window=window,
                payment_method=customer_form.cleaned_data['payment_method']
            )

            formset = OrderItemFormSet(request.POST, instance=order)
            if formset.is_valid():
                items = formset.save(commit=False)
                for item in items:
                    item.batch = window.batch # Auto-assign the batch from the window
                    item.unit_price = window.batch.price_override or item.product.base_price
                    item.save()
                order.update_total_price()
                return redirect('order_success', order_id=order.id)
    else:
        customer_form = PublicOrderForm()
        formset = OrderItemFormSet()

    context = {
        'window': window,
        'customer_form': customer_form,
        'formset': formset
    }
    return render(request, 'orders/public_order_form.html', context)


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    whatsapp_text = f"Hi, I just placed order #{order.id} for {order.window.zone.name} delivery on {order.window.delivery_date}. Total: ${order.total_price}"
    context = {
        'order': order,
        'whatsapp_text': whatsapp_text,
    }
    return render(request, 'orders/order_success.html', context)
