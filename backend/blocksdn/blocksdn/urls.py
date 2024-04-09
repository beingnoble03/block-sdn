from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("controller/", include("blocksdn_app.urls")),
    path("admin/", admin.site.urls),
]