from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("homepage.urls")),
    path("trading/", include("trading.urls")),
    path("admin/", admin.site.urls),
]
