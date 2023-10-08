from django.urls import path
from AppShop import views
app_name = 'AppShop'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('product/<int:pk>/', views.ProductDetails.as_view(), name='details'),
]