from django.contrib import admin
from .models import Prediction_Match
class PredictionMatchAdmin(admin.ModelAdmin):
    list_display = ('user' , 'home_team' , 'away_team' , 'predicted_home_goals' , 'predicted_away_goals' , 'result' , 'created_at')
    search_fields = ('user' , 'home_team' , 'away_team' , 'predicted_home_goals' , 'predicted_away_goals' , 'result' , 'created_at')
admin.site.register(Prediction_Match , PredictionMatchAdmin)

