# prediction/urls.py
from django.urls import path
from .views import PricePredictionView

urlpatterns = [
    path('predict-price/', PricePredictionView.as_view(), name='predict-price'),
]
