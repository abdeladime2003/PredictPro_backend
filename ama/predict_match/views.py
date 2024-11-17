from rest_framework.decorators import api_view
from rest_framework.response import Response
import joblib
import pandas as pd
from rest_framework.permissions import IsAuthenticated
from .models import Prediction_Match
# Charger les modèles sauvegardés
away_model= joblib.load(r'C:\Users\LENOVO\Desktop\backend\ama\predict_match\ml_model\away_model.joblib')
home_model = joblib.load(r'C:\Users\LENOVO\Desktop\backend\ama\predict_match\ml_model\home_model.joblib')



# Charger les données historiques
historical_matches = pd.read_csv(r'C:\Users\LENOVO\Desktop\backend\ama\predict_match\ml_model\df_clean.csv')
# Affichage des premières lignes
print(historical_matches.head())

# Vérification des colonnes disponibles
print(historical_matches.columns)

# Création de la colonne 'goal_difference' si elle n'existe pas
if 'goal_difference' not in historical_matches.columns:
    # Supposons que 'FTHG' (Full Time Home Goals) et 'FTAG' (Full Time Away Goals) existent
    historical_matches['goal_difference'] = historical_matches['FTHG'] - historical_matches['FTAG']

# Fonction de prédiction
def custom_round(value):
    return max(0, int(value)+1)

def predict_match(home_team, away_team):
    home_team_form = historical_matches[historical_matches['HomeTeam'] == home_team]['goal_difference'].mean()
    away_team_form = historical_matches[historical_matches['AwayTeam'] == away_team]['goal_difference'].mean()

    if pd.isna(home_team_form):
        home_team_form = 0
    if pd.isna(away_team_form):
        away_team_form = 0

    new_match = pd.DataFrame({
        'HomeTeam': [home_team],
        'AwayTeam': [away_team],
        'home_team_form': [home_team_form],
        'away_team_form': [away_team_form]
    })

    # Prédictions pour les buts
    home_goals = custom_round(home_model.predict(new_match)[0])
    away_goals = custom_round(away_model.predict(new_match)[0])

    return home_goals, away_goals

@api_view(['POST'])
def predict_view(request):
    permission_classes = [IsAuthenticated]  # Assure-toi que cette permission est active
    user = request.user  # Récupérer l'utilisateur authentifié
    data = request.data
    home_team = data.get('home_team')
    away_team = data.get('away_team')

    if home_team and away_team:
        home_goals, away_goals = predict_match(home_team, away_team)
        result = 'Home Win' if home_goals > away_goals else 'Away Win' if away_goals > home_goals else 'Draw'

        # Enregistrement de la prédiction dans la base de données
        prediction = Prediction_Match.objects.create(
            user=user,
            home_team=home_team,
            away_team=away_team,
            predicted_home_goals=home_goals,
            predicted_away_goals=away_goals,
            result=result
        )

        return Response({
            'home_team': home_team,
            'away_team': away_team,
            'home_goals': home_goals,
            'away_goals': away_goals,
            'result': result,
            'prediction_id': prediction.id  # Retourner l'ID de la prédiction enregistrée
        })
    else:
        return Response({'error': 'Invalid input'}, status=400)
## get all predictions
@api_view(['GET'])
def get_predictions(request):
    permission_classes = [IsAuthenticated]
    
    # Vérifie si l'utilisateur est authentifié
    user = request.user
    if not user.is_authenticated:
        return Response({'error': 'User not authenticated'}, status=401)

    # Récupérer les prédictions de l'utilisateur
    predictions = Prediction_Match.objects.filter(user=user)
    data = [
        {
            'home_team': pred.home_team,
            'away_team': pred.away_team,
            'home_goals': pred.predicted_home_goals,
            'away_goals': pred.predicted_away_goals,
            'result': pred.result,
            'prediction_id': pred.id  # Ajoute l'ID de la prédiction si nécessaire
        } for pred in predictions
    ]
    
    return Response(data)
