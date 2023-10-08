from django.shortcuts import render

# Import Views
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
# Import models
from .models import Product, Category

# Create your views here.
class Home(ListView):
    model = Product
    template_name = 'AppShop/home.html'

class ProductDetails(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'AppShop/product_details.html'