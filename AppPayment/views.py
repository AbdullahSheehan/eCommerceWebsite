from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from .forms import BillingForm
from AppOrder.models import Order, Cart
from AppPayment.models import BillingAddress
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Payment
import requests
from sslcommerz_lib import SSLCOMMERZ 
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@login_required
def checkout_form(req):
    saved_address = BillingAddress.objects.get_or_create(user=req.user)[0]
    form = BillingForm(instance=saved_address)
    if(req.method == 'POST'):
        form = BillingForm(req.POST, instance=saved_address)
        if (form.is_valid()):
            form.save()
            form = BillingForm(instance=saved_address)
            messages.success(req, "Billing Address has been updated!")
    order_qs = Order.objects.filter(user=req.user, ordered=False)[0]
    order_items = order_qs.orderitems.all()
    order_total = order_qs.get_totals()
    return render(req, 'AppPayment/checkout.html', context={'form':form, 'items':order_items, 'total':order_total, 'address':saved_address})

@login_required
def payment(req):
    saved_address = BillingAddress.objects.get_or_create(user=req.user)[0]
    if not saved_address.is_fully_filled():
        messages.info(req, 'Please complete the shipping address')
        return redirect('AppPayment:checkout')
    if not req.user.profile.is_fully_filled():
        messages.info(req, 'Please Complete your profile details first')
        return redirect('AppLogin:profile')
    settings = { 'store_id': 'examp6523129d9c69c', 'store_pass': 'examp6523129d9c69c@ssl', 'issandbox': True }
    sslcommez = SSLCOMMERZ(settings)
    post_body = {}
    # Success & Fail URL's
    status_url = req.build_absolute_uri(reverse('AppPayment:complete'))
    print(status_url)
    post_body['success_url'] = status_url
    post_body['fail_url'] = status_url
    post_body['cancel_url'] = status_url
    # Order Info
    post_body['tran_id'] = "IHKADSQ124809JASDF"
    order_qs = Order.objects.filter(user=req.user, ordered=False)
    order_items = order_qs[0].orderitems.all()
    order_count = order_qs[0].orderitems.count()
    order_total = order_qs[0].get_totals()
    post_body['total_amount'] = Decimal(order_total)
    post_body['currency'] = "BDT"
    post_body['shipping_method'] = "Courier"
    post_body['product_name'] = order_items
    post_body['num_of_item'] = order_count
    post_body['product_category'] = "Mixed"
    post_body['product_profile'] = "None"
    # Customer Info
    cur_user = req.user
    post_body['ship_name'] = cur_user.profile.fullname
    post_body['ship_add1'] = cur_user.profile.address_1
    post_body['ship_city'] = cur_user.profile.city
    post_body['ship_country'] = cur_user.profile.country
    post_body['ship_postcode'] = cur_user.profile.zipcode
    post_body['cus_email'] = cur_user.email
    post_body['cus_phone'] = cur_user.profile.phone
    post_body['cus_add1'] = cur_user.profile.address_1
    post_body['cus_city'] = cur_user.profile.city
    post_body['cus_country'] = cur_user.profile.country
    response = sslcommez.createSession(post_body)
    #print(response)
    return redirect(response['GatewayPageURL'])

@csrf_exempt
def complete(req):
    if req.method == 'POST' or req.method == 'post':
        payment_data = req.POST
        status = (payment_data['status'])
        if(status == 'VALID'):
            val_id = payment_data['val_id']
            bank_tran_id = payment_data['bank_tran_id']
            messages.success(req, 'Your Payment Completed Successfully! Redirecting you to homepage...')
            return HttpResponseRedirect(reverse('AppPayment:purchased', kwargs={'val_id':val_id, 'tran_id':bank_tran_id}))
        elif(status == 'FAILED'):
            messages.warning(req, 'Your Payment Failed! Please try again.(Redirecting you to homepage...)')
    return render(req, 'AppPayment/complete.html', context={})

@login_required
def purchase(req, val_id, tran_id):
    order_qs = Order.objects.filter(user=req.user, ordered=False)
    order = order_qs[0]
    order.ordered = True
    order.orderID = tran_id
    order.paymentID = val_id
    order.save()
    cart_items = Cart.objects.filter(user=req.user, purchased=False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse('AppShop:home'))
@login_required
def orderall(req):
    try:
        orders = Order.objects.filter(user=req.user, ordered=True)
        context = {'orders':orders}
    except:
        messages.warning(req, 'You do not have any order')
        return redirect('AppShop:home')
    return render(req, 'AppPayment/order.html', context=context)