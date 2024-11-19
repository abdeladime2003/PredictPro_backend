
# Backend_ML - PredictPro  

## Description  

Le backend de **PredictPro** est conçu avec **Django** et **Django Rest Framework (DRF)** pour offrir une architecture modulaire et performante.  
Il fournit des fonctionnalités innovantes pour :  
- Prédire les résultats de match.  
- Estimer les prix des transferts de joueurs.  
- Générer des images à partir de descriptions textuelles.  

Chaque API est associée à des modèles de machine learning dédiés, organisés par fonction pour une gestion claire et efficace. Ces modèles sont optimisés et intégrés dans le backend pour répondre aux besoins spécifiques de chaque fonctionnalité.  

Le projet utilise une base de données **PostgreSQL** pour gérer les données liées aux utilisateurs, aux prédictions et aux générateurs d'images.  

---

## Fonctionnalités  

### 1. Prédiction des résultats de match  
- **Description** : Prévoir les scores des matchs en fonction des performances historiques et des données des équipes.  
- **Modèles ML** : Basés sur des statistiques historiques et des algorithmes de régression.  

### 2. Prédiction des prix des transferts  
- **Description** : Estimer la valeur des joueurs selon divers paramètres comme les performances récentes, l'âge, et la popularité.  
- **Modèles ML** : Réseaux neuronaux et algorithmes supervisés.  

### 3. Génération d'images  
- **Description** : Générer des images personnalisées à partir d'une description textuelle fournie par l'utilisateur.  
- **Modèles ML** : Modèles de génération d'images (GANs).  

### 4. Gestion des utilisateurs  
- **Description** :  
  - Inscription, connexion et gestion sécurisée des utilisateurs.  
  - Utilisation de **JWT** pour l'authentification et l'autorisation.  

---

## Installation  

### Prérequis  
- **Python 3.x** : Pour exécuter l'application Django.  
- **Virtualenv** : Pour isoler l'environnement Python.  
- **PostgreSQL** : Base de données pour le stockage des données.  

### Étapes d'installation  

1. **Clonez le repository**  

   ```bash
   git clone https://github.com/ton-utilisateur/PredictPro_backend.git
   cd PredictPro_backend
   ```  

2. **Créez un environnement virtuel et activez-le**  

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # Sur Windows : myenv\Scripts\activate
   ```  

3. **Installez les dépendances**  

   ```bash
   pip install -r requirements.txt
   ```  

4. **Configurez les variables d'environnement**  
   - Créez un fichier `.env` à la racine du projet avec les informations nécessaires (base de données, clés API, etc.).  

5. **Appliquez les migrations**  

   ```bash
   python manage.py migrate
   ```  

6. **Lancez le serveur de développement**  

   ```bash
   python manage.py runserver
   ```  

   Accédez à l'application à [http://localhost:8000](http://localhost:8000).  

---

## API Endpoints  

### Prédiction des résultats de match  
- **Méthode** : POST  
- **Paramètres** :  
  - `team1` : Nom de l'équipe 1.  
  - `team2` : Nom de l'équipe 2.  
- **Réponse** : Prédiction du score.  

### Prédiction des prix des transferts  
- **Méthode** : POST  
- **Paramètres** :  
  - `player_name` : Nom du joueur.  
  - `statistics` : Statistiques du joueur.  
- **Réponse** : Estimation du prix.  

### Génération d'images  
- **Méthode** : POST  
- **Paramètres** :  
  - `description` : Description textuelle de l'image (par ex. : "un joueur de football stylisé").  
- **Réponse** : Image générée.  

### Inscription et authentification  
- **Méthode** : POST  
- **Paramètres** :  
  - `username` : Nom d'utilisateur.  
  - `email` : Adresse email.  
  - `password` : Mot de passe.  

- **Réponse** : Confirmation d'inscription.

## Contribuer

1. Fork ce repository.
2. Crée une branche (`git checkout -b feature/nouvelle-fonctionnalité`).
3. Fais tes modifications.
4. Soumets une pull request.

## Licence

Ce projet est sous licence [MIT](https://opensource.org/licenses/MIT).
