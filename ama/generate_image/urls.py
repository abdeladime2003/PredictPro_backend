from django.urls import path
from .views import ImageGeneratorAPIView

urlpatterns = [
    path("generate/", ImageGeneratorAPIView.as_view(), name="generate-image"),
]
