from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),  # Interface d'administration Django
    path('', include('users.urls')),  # Inclure les URLs de l'application users
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # URL pour obtenir le token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # URL pour rafraîchir le token
    path('transfer-predictions/', include('transfer_predictions.urls')),  # Inclure les URLs de l'application transfer_predictions
    path('accounts/', include('allauth.urls')),  # Inclure les URLs de django-allauth
    path('predict-match/', include('predict_match.urls')),  # Inclure les URLs de l'application predict_match
    path('generate-image/', include('generate_image.urls')),  # Inclure les URLs de l'application generate_image

]
