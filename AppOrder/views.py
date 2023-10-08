# Generals
from django.shortcuts import render, get_object_or_404, redirect
# Auth
from django.contrib.auth.decorators import login_required
# Model
from AppShop.models import Product
from .models import Order, Cart
# Messages
from django.contrib import messages
# Create your views here.
@login_required
def add_to_cart(req, pk):
    item = get_object_or_404(Product, pk=pk)
    print(f"item => {item}")
    order_item = Cart.objects.get_or_create(product=item, user=req.user, purchased=False) # Returns a tuple where second index is False if object existed before or its True
    print(f"order_item => {order_item}")
    order_qs = Order.objects.filter(user=req.user, ordered=False)
    print(f"order_qs => {order_qs}")
    if(order_qs.exists()):
        order = order_qs[0]
        print(f"order => {order}")
        if order.orderitems.filter(product=item).exists():
            order_item[0].quantity += 1
            order_item[0].save()
            messages.info(req, "This item quantity was updated")
            return redirect('AppShop:home')
        else:
            order.orderitems.add(order_item[0])
            messages.info(req, "This item was added to your cart")
            return redirect('AppShop:home')
    else:
        order = Order(user=req.user)
        order.save()
        order.orderitems.add(order_item[0])
        messages.info(req, 'This item was added to your cart')
        return redirect('AppShop:home')

@login_required
def cart_view(req):
    carts = Cart.objects.filter(user=req.user, purchased=False)
    orders = Order.objects.filter(user=req.user, ordered=False)
    if carts.exists() and orders.exists():
        order = orders[0]
        return render(req, 'AppOrder/cart.html', context={'carts':carts, 'order':order})
    else:
        messages.warning(req, "You have nothing in your cart")
        return redirect('AppShop:home')
    
@login_required
def remove_from_cart(req, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=req.user, ordered=False)
    if(order_qs.exists()):
        order = order_qs[0].orderitems
        if(order.filter(product=item).exists()):
            order_item = Cart.objects.filter(user=req.user, product=item, purchased=False)[0]
            order.remove(order_item)
            order_item.delete()
            messages.info(req, 'This item was removed from your cart!')
            return redirect('AppOrder:cart')
        else:
            messages.info(req, "This product is not in your cart!")
            return redirect('AppShop:home')
    else:
        messages.info(req, "You have no items to remove!")
        return redirect('AppShop:home')

@login_required
def increase_quantity(req, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=req.user, ordered=False)
    if(order_qs.exists()):
        order = order_qs[0].orderitems
        if(order.filter(product=item).exists()):
            order_item = Cart.objects.filter(product=item, user=req.user, purchased=False)[0]
            if(order_item.quantity >= 1):
                order_item.quantity += 1
                order_item.save()
                return redirect('AppOrder:cart')
        else:
            messages.info(req, f"{item.name} is not in your cart!")
            return redirect('AppOrder:cart')
    else:
        messages.info(req, "You don't have an active cart")
        return redirect('AppShop:home')
    
@login_required
def decrease_quantity(req, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=req.user, ordered=False)
    if(order_qs.exists()):
        order = order_qs[0].orderitems
        if(order.filter(product=item).exists()):
            order_item = Cart.objects.filter(product=item, user=req.user, purchased=False)[0]
            if(order_item.quantity > 1):
                order_item.quantity -= 1
                order_item.save()
                return redirect('AppOrder:cart')
            else:
                order.remove(order_item)
                order_item.delete()
                return redirect('AppOrder:cart')
        else:
            messages.info(req, f"{item.name} is not in your cart!")
            return redirect('AppOrder:cart')
    else:
        messages.info(req, "You don't have an active cart")
        return redirect('AppShop:home')
    