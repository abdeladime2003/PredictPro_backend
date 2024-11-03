from django.urls import path
from .views import UserListCreateView, UserRetrieveUpdateDestroyView, LoginView, LogoutView

urlpatterns = [
    path('', UserListCreateView.as_view(), name='user-list-create'),  # Pour lister et créer des utilisateurs
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='user-retrieve-update-destroy'),  # Pour récupérer, mettre à jour ou supprimer un utilisateur
    path('login/', LoginView.as_view(), name='login'),  # Pour se connecter
    path('logout/', LogoutView.as_view(), name='logout'),  # Pour se déconnecter
    
]