from django.urls import path
from AppPayment import views
app_name = 'AppPayment'
urlpatterns = [
    path('checkout/', views.checkout_form, name='checkout')
]