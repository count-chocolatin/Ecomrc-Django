from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from django.utils import timezone
from .models import Item, OrderItem, Order

class HomeView(ListView):
    model = Item
    template_name = "home.html"

class ItemDetailView(DetailView):
         model = Item
         template_name = "product.html"


def checkout(request):
         return render(request, 'checkout.html')

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, create = OrderItem.objects.get_or_create(
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
            messages.info(request, "this item quantity was update.")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "this item was added to you cart.")
            order.items.add(order_item)
            return redirect("core:product", slug=slug)    
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,
                                    ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "this item quantity was updated")
    return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
        )
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user= request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "this item was removed from your cart")
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, "this item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "you do not have an active order")
        return redirect("core:product", slug=slug) 
    