from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View, ListView, DetailView

from .models import Product, OrderItem, Order
from .forms import AddressForm


class StoreView(ListView):
    model = Product
    template_name = "store.html"
    context_object_name = "items"


class ProductView(DetailView):
    model = Product
    template_name = "product.html"


@login_required
def cart_remove(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.get_or_create(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
    return redirect("estore:cart")


@login_required
def cart_update(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.get_or_create(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
    return redirect("estore:cart")


@login_required
def cart_add(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
        else:
            order.items.add(order_item)
    else:
        order = Order.objects.create(user=request.user)
        order.items.add(order_item)

    return redirect("estore:cart")

def cart(request):
    if not request.user.is_authenticated:
        return render(request, "cart.html")

    try:
        order = Order.objects.get(user=request.user, ordered=False)
        return render(request, "cart.html", {'object': order})
    except ObjectDoesNotExist:
        return render(request, "cart.html")


def checkout(request):
    context = {}
    return render(request, "checkout.html", context)

@login_required
def profile(request):
    context = {
        'form': AddressForm
    }
    return render(request, "profile.html", context)

@login_required
def saved_cards(request):
    context = {}
    return render(request, "cards.html", context)

@login_required
def saved_address(request):
    context = {}
    return render(request, "address.html", context)

@login_required
def order_history(request):
    context = {}
    return render(request, "order_history.html", context)

@login_required
def payment(request):
    context = {}
    return render(request, "payment.html", context)