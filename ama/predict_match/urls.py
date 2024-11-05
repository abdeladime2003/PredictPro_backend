from django.urls import path
from .views import predict_view , get_predictions
urlpatterns = [
    path('predict/', predict_view, name='predict'),
    path('predictions/', get_predictions, name='predictions'),
]
