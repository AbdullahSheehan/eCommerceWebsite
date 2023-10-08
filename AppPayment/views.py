from django.shortcuts import render, HttpResponseRedirect
from .forms import BillingForm
from AppOrder.models import Order
from AppPayment.models import BillingAddress
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
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
    return render(req, 'AppPayment/checkout.html', context={'form':form, 'items':order_items, 'total':order_total})