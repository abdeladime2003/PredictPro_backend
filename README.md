
# Backend - PredictPro

## Description

Le backend de **PredictPro** est construit avec **Django** et **Django Rest Framework (DRF)** pour fournir des API robustes et efficaces. Ce backend gère les fonctionnalités principales telles que :
- La prédiction des résultats de match
- La prédiction des prix des transferts
- La génération d'images à partir de descriptions textuelles

Le projet utilise une base de données  PostgreSQL  pour stocker les données liées aux utilisateurs, aux prédictions et aux générateurs d'images.



## Fonctionnalités

### Prédiction des résultats de match
- L'API prend en entrée les équipes pour prédire les résultats.
- Modèle basé sur des statistiques historiques et des performances des équipes.

### Prédiction des prix des transferts
- Prédiction des prix des joueurs en fonction de différents paramètres comme les performances récentes, l'âge, et la popularité.

### Génération d'images
- API permettant la génération d'images en fonction d'une description textuelle fournie par l'utilisateur.

### Gestion des utilisateurs
- Inscription et gestion des utilisateurs via des API sécurisées.
- Utilisation de JWT pour l'authentification.

## Installation

### Prérequis
- **Python 3.x** : Pour exécuter l'application Django.
- **Virtualenv** : Pour isoler l'environnement Python.
- **PostgreSQL**  : Base de données pour le stockage des données.

### Étapes d'installation

1. Clone le repository backend

```bash
git clone https://github.com/ton-utilisateur/PredictPro_backend.git
cd PredictProb_backend
```

2. Crée un environnement virtuel et active-le

```bash
python -m venv myenv
source myenv/bin/activate  # Sur Windows : myenv\Scriptsctivate
```

3. Installe les dépendances

```bash
pip install -r requirements.txt
```

4. Configure les variables d'environnement
- Crée un fichier `.env` à la racine du projet avec les variables nécessaires (comme la base de données, les clés API, etc.).

5. Applique les migrations de la base de données

```bash
python manage.py migrate
```

6. Démarre le serveur de développement

```bash
python manage.py runserver
```

Cela démarrera le backend sur [http://localhost:8000](http://localhost:8000).



## API Endpoints

### Prédiction des résultats de match
- **Méthode** : POST
- **Paramètres** :
  - `team1`: Nom de l'équipe 1
  - `team2`: Nom de l'équipe 2
- **Réponse** : Prédiction du score du match.

### Prédiction des prix des transferts
- **Méthode** : POST
- **Paramètres** :
  - `player_name`: Nom du joueur
  - `Statistics`: Statistics du joueur
- **Réponse** : Estimation du prix du transfert.

### Génération d'images

- **Méthode** : POST
- **Paramètres** :
  - `description`: Description de l'image (par exemple "joueur de football stylisé")
- **Réponse** : Image générée selon la description.

### Inscription et Authentification

- **Méthode** : POST
- **Paramètres** :
  - `username`: Nom d'utilisateur
  - `email`: Adresse email
  - `password`: Mot de passe
- **Réponse** : Confirmation d'inscription.

## Contribuer

1. Fork ce repository.
2. Crée une branche (`git checkout -b feature/nouvelle-fonctionnalité`).
3. Fais tes modifications.
4. Soumets une pull request.

## Licence

Ce projet est sous licence [MIT](https://opensource.org/licenses/MIT).
