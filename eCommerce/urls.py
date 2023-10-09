from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('AppShop.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('AppLogin.urls')),
    path('shop/', include('AppOrder.urls')),
    path('payment/', include('AppPayment.urls')),
]

from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)