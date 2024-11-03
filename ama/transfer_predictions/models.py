# prediction/models.py
from django.db import models
from users.models import User

class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Lien avec l'utilisateur
    predicted_price = models.FloatField()  # Prix prédit
    features = models.JSONField()  # Stocker les caractéristiques utilisées pour la prédiction
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création de la prédiction

    def __str__(self):
        return f"{self.user.email} - {self.predicted_price} - {self.created_at}"
