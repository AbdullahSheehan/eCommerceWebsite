from django.urls import path
from AppLogin import views
app_name = 'AppLogin'
urlpatterns = [
    path('signup/',views.sign_up, name='signup'),
    path('login/',views.login_user, name='login'),
    path('logout/',views.logout_user, name='logout'),
    path('profile/',views.profile_user, name='profile'),
]