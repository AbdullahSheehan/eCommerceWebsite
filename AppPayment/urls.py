from django.urls import path
from AppPayment import views
app_name = 'AppPayment'
urlpatterns = [
    path('checkout/', views.checkout_form, name='checkout'),
    path('', views.payment, name='payment'),
    path('status/', views.complete, name='complete'),
    path('purchase/<val_id>/<tran_id>/', views.purchase, name='purchased'),
    path('orders/', views.orderall, name='orders')
]