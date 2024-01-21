from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("account/", include("accounts.urls")),
    path("store/", include("store.urls")),
    path("cart/", include("cart.urls")),
    path("order/", include("orders.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
