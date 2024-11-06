import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
import logging

# Création d'un logger
logger = logging.getLogger(__name__)

class ImageGeneratorAPIView(APIView):
    def post(self, request):
        logger.info("Received request for image generation.")
        prompt = request.data.get("prompt")
        authorization_token = "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"  # Remplacez par votre token réel

        if authorization_token and prompt and len(prompt) >= 5:
            API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
            
            json_payload = {
                "inputs": prompt,
                "parameters": {
                    "num_inference_steps": 50,
                    "guidance_scale": 7.5
                }
            }
            
            logger.info(f"Sending request to API with prompt: {prompt}")
            try:
                response = requests.post(API_URL,
                                         headers={"Authorization": f"Bearer {authorization_token}"},
                                         json=json_payload)

                if response.status_code == 200:
                    try:
                        image = Image.open(BytesIO(response.content))
                        buffered = BytesIO()
                        image.save(buffered, format="PNG")
                        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
                        logger.info("Image generated successfully.")
                        return JsonResponse({"image": img_str}, status=status.HTTP_200_OK)
                    except UnidentifiedImageError:
                        logger.error("API response is not a valid image.")
                        return Response({"error": "API response is not a valid image"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    logger.error(f"Failed to fetch image. Status code: {response.status_code}")
                    return Response({
                        "error": "Failed to fetch image",
                        "status_code": response.status_code,
                        "details": response.json() if response.headers.get("Content-Type") == "application/json" else response.content
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                logger.exception("An unexpected error occurred during API request.")
                return Response({"error": "An unexpected error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.warning("Invalid prompt or authorization token.")
            return Response({"error": "Invalid prompt or authorization token"}, status=status.HTTP_400_BAD_REQUEST)
