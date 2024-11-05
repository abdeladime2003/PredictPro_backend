from rest_framework import serializers
from .models import Prediction_Match

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction_Match
        fields = '__all__'