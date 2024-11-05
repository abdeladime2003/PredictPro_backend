from django.db import models
from users.models import User
class Prediction_Match(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Lien avec l'utilisateur
    home_team = models.CharField(max_length=100 , default='home_team')
    away_team = models.CharField(max_length=100 , default='away_team')
    predicted_home_goals = models.IntegerField()
    predicted_away_goals = models.IntegerField()
    result = models.CharField(max_length=20, default='Draw')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} - {self.predicted_home_goals} - {self.predicted_away_goals} - {self.result} - {self.created_at}"