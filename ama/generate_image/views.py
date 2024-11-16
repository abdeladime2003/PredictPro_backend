import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
import logging
from .models import GeneratedImage  # Importez le modèle

# Création d'un logger
logger = logging.getLogger(__name__)

class ImageGeneratorAPIView(APIView):
    def post(self, request):
        logger.info("Received request for image generation.")
        
        # Récupérer le prompt depuis la requête
        prompt = request.data.get("prompt")
        logger.info(f"Prompt received: {prompt}")
        
        # Token d'authentification (à remplacer par un réel token si nécessaire)
        authorization_token = "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"
        user = request.user if request.user.is_authenticated else None
        logger.info(f"User authenticated: {user is not None}")
        
        # Vérifier si le token et le prompt sont valides
        if authorization_token and prompt and len(prompt) >= 5:
            # URL de l'API Hugging Face
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
            
            # Corps de la requête
            json_payload = {
                "inputs": prompt,
                "parameters": {
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5
                }
            }
            
            logger.info(f"Sending request to API with prompt: {prompt}")
            
            try:
                # Faire la requête à l'API Hugging Face
                response = requests.post(API_URL,
                                         headers={"Authorization": f"Bearer {authorization_token}"},
                                         json=json_payload)
                
                logger.info(f"API response status code: {response.status_code}")
                
                # Si la réponse est correcte (status 200)
                if response.status_code == 200:
                    try:
                        # Ouvrir l'image depuis la réponse API
                        logger.info("Processing image from API response.")
                        image = Image.open(BytesIO(response.content))
                        buffered = BytesIO()
                        image.save(buffered, format="PNG")
                        
                        # Convertir l'image en base64
                        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                        
                        # Sauvegarder l'image et le prompt dans la base de données
                        logger.info(f"Saving image with prompt: {prompt}")
                        GeneratedImage.objects.create(prompt=prompt, image_data=img_str, user=user)

                        logger.info("Image generated and saved successfully.")
                        
                        # Retourner l'image générée en base64
                        return JsonResponse({"image": img_str}, status=status.HTTP_200_OK)
                    
                    except UnidentifiedImageError:
                        logger.error("API response is not a valid image.")
                        return Response({"error": "API response is not a valid image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                else:
                    # Si l'API renvoie une erreur
                    logger.error(f"Failed to fetch image. Status code: {response.status_code}")
                    logger.error(f"Error details: {response.content}")
                    return Response({
                        "error": "Failed to fetch image",
                        "status_code": response.status_code,
                        "details": response.json() if response.headers.get("Content-Type") == "application/json" else response.content
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            except Exception as e:
                # Gérer toute autre exception inattendue
                logger.exception("An unexpected error occurred during API request.")
                return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        else:
            # Si le prompt ou le token d'authentification sont invalides
            logger.warning("Invalid prompt or authorization token.")
            return Response({"error": "Invalid prompt or authorization token"}, status=status.HTTP_400_BAD_REQUEST)
