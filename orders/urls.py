from django.urls import path
from . import views

urlpatterns = [
    path('order/<int:window_id>/', views.public_order_view, name='public_order'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
]
