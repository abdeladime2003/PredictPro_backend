import joblib
import numpy as np
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from .models import Prediction
from rest_framework.permissions import IsAuthenticated

class PricePredictionView(views.APIView):
    permission_classes = [IsAuthenticated]  # Assurer que l'utilisateur est authentifié
    def get(self, request):
        # Code pour récupérer les prédictions (par exemple, toutes les prédictions d'un utilisateur)
        user_predictions = Prediction.objects.filter(user=request.user)
        predictions_data = [{'predicted_price': pred.predicted_price, 'features': pred.features} for pred in user_predictions]
        
        return Response(predictions_data, status=status.HTTP_200_OK)
    def post(self, request):
        # Charger le modèle
        model = joblib.load(r'C:\Users\LENOVO\Desktop\backend\ama\transfer_predictions\Ml_Scraping\model.pkl')

        # Récupérer les données d'entrée
        input_data = request.data.get('features')  # Assurez-vous que les features sont correctement envoyées
        
        # Vérification de l'existence de input_data
        if input_data is None:
            return Response({'error': 'Aucune donnée de caractéristiques fournie.'}, status=status.HTTP_400_BAD_REQUEST)

        # Liste des caractéristiques requises
        required_features = ['age', 'ATT', 'SKI', 'MOV', 'POW', 'MEN', 'DEF', 'GK', 'fee', 'loan']
        
        # Validation des données d'entrée
        missing_features = [feature for feature in required_features if feature not in input_data]
        if missing_features:
            return Response({'error': f'Les champs suivants sont requis: {", ".join(missing_features)}.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Convertir les données d'entrée en tableau numpy
        try:
            input_data_array = np.array([list(input_data.values())])
            
            # Effectuer la prédiction
            prediction = model.predict(input_data_array)
            
            # Enregistrer la prédiction dans la base de données
            user_prediction = Prediction(
                user=request.user,
                predicted_price=prediction[0],  # Ajouter un peu de bruit si nécessaire
                features=input_data
            )
            user_prediction.save()  # Sauvegarder l'objet Prediction

            return Response({'predicted_price': prediction[0]}, status=status.HTTP_200_OK)
        except Exception as e:
            print(f"Erreur lors de la prédiction: {e}")  # Pour le débogage
            return Response({'error': 'Erreur lors de la prédiction.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
