from django.urls import path
from AppOrder import views
app_name = 'AppOrder'
urlpatterns = [
    path('add/<pk>', views.add_to_cart, name='add'),
    path('cart/', views.cart_view, name='cart'),
    path('remove/<pk>', views.remove_from_cart, name='remove'),
    path('increase/<pk>', views.increase_quantity, name='increase'),
    path('decrease/<pk>', views.decrease_quantity, name='decrease'),
]