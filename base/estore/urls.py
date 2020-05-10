from django.urls import path
from .views import (
    StoreView,
    ProductView,
    cart,
    cart_add,
    cart_update,
    cart_remove,
    checkout,
    payment,
    profile,
    saved_cards,
    saved_address,
    order_history,
)

app_name = 'estore'

urlpatterns = [
    path('', StoreView.as_view(), name='store'),
    path('product/<slug>/', ProductView.as_view(), name='product'),
    path('cart_add/<slug>', cart_add, name='cart_add'),
    path('cart_update/<slug>', cart_update, name='cart_update'),
    path('cart_remove/<slug>', cart_remove, name='cart_remove'),
    path('cart/', cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('payment/', payment, name='payment'),
    path('profile/', profile, name='profile'),
    path('saved_cards/', saved_cards, name='saved_cards'),
    path('saved_address/', saved_address, name='saved_address'),
    path('order_history/', order_history, name='order_history'),
]
