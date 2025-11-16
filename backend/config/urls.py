from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(
        route="admin/", 
        view=admin.site.urls,
        name="admin"
    ),
    path(
        route="files/",
        view=include("s3storage.urls"),
        name="s3_storage"
    )
]
