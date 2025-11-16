from django.urls import path
from .views import FileAPIView

urlpatterns = [
    # http://localhost:8000/files/
    path(
        route="",
        view=FileAPIView.as_view(),
        name="files"
    )
]
