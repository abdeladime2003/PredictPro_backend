# prediction/urls.py
from django.urls import path
from .views import PricePredictionView

urlpatterns = [
    path('predict-price/', PricePredictionView.as_view(), name='predict-price'),
]
# prediction/views.py
from rest_framework import generics
from .models import Prediction
from .serializers import PredictionSerializer

class UserPredictionsView(generics.ListAPIView):
    serializer_class = PredictionSerializer

    def get_queryset(self):
        return Prediction.objects.filter(user=self.request.user)
