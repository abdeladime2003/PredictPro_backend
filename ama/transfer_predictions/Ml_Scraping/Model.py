import pandas as pd
import numpy as np
import xgboost as xgb
import optuna
from sklearn.model_selection import train_test_split, cross_val_score, RepeatedKFold
from sklearn.preprocessing import QuantileTransformer
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
import pickle

class XGBoostModelBuilder:
    def __init__(self, random_state=1937):
        self.random_state = random_state
        self.scaler = QuantileTransformer(output_distribution='normal')

    def prepare_data(self, df):
        """
        Prépare les données en nettoyant et transformant les variables.
        """
        # Convertir les valeurs de 'market_value' en numériques
        df['market_value'] = df['market_value'].apply(self.convert_market_value)
        
        # Supprimer les colonnes inutiles
        df = df.drop(['Unnamed: 0', 'Unnamed: 0.1', 'name'], axis=1, errors='ignore')
        
        # Imputation des valeurs manquantes
        df = self.impute_missing_values(df)

        # Suppression des outliers avec IQR
        numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
        df = self.remove_outliers_iqr(df, numerical_columns)
        
        return df

    def convert_market_value(self, value):
        """
        Convertit les valeurs de 'market_value' en nombres.
        """
        try:
            value = str(value).replace('€', '').strip()
            if 'M' in value:
                return float(value.replace('M', '')) * 1_000_000
            elif 'k' in value:
                return float(value.replace('k', '')) * 1_000
            return float(value)
        except:
            return np.nan

    def impute_missing_values(self, df):
        """
        Impute les valeurs manquantes des colonnes numériques.
        """
        imp = IterativeImputer(random_state=self.random_state)
        numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
        df[numerical_columns] = imp.fit_transform(df[numerical_columns])
        return df

    def remove_outliers_iqr(self, df, columns, k=1.5):
        """
        Supprime les valeurs aberrantes selon la méthode IQR.
        """
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df = df[~((df[col] < (Q1 - k * IQR)) | (df[col] > (Q3 + k * IQR)))]
        return df

    def create_advanced_features(self, X):
        """
        Crée des caractéristiques avancées à partir des colonnes existantes.
        """
        X = X.copy()
        skills_cols = ['ATT', 'SKI', 'MOV', 'POW', 'MEN', 'DEF', 'GK']
        
        # Moyenne, écart-type, max, min des compétences
        X['skills_mean'] = X[skills_cols].mean(axis=1)
        X['skills_std'] = X[skills_cols].std(axis=1)
        X['skills_max'] = X[skills_cols].max(axis=1)
        X['skills_min'] = X[skills_cols].min(axis=1)

        # Ratios et scores basés sur les compétences
        X['att_def_ratio'] = X['ATT'] / (X['DEF'] + 1)
        X['skill_efficiency'] = X['SKI'] * X['MOV'] / (X['age'] + 1)
        X['mental_physical_balance'] = X['MEN'] / (X['POW'] + 1)
        X['offensive_score'] = (X['ATT'] * 0.4 + X['SKI'] * 0.3 + X['MOV'] * 0.3)
        X['defensive_score'] = (X['DEF'] * 0.4 + X['POW'] * 0.3 + X['MEN'] * 0.3)
        X['overall_potential'] = X['skills_mean'] * (30 / (X['age'] + 1))

        # Interactions entre les compétences
        for col1 in skills_cols:
            for col2 in skills_cols:
                if col1 < col2:
                    X[f'{col1}_{col2}_interact'] = X[col1] * X[col2]

        # Caractéristiques supplémentaires
        X['age_squared'] = X['age'] ** 2
        X['experience_factor'] = np.log1p(X['age'] * X['skills_mean'])

        return X

    def optimize_hyperparameters(self, X, y, n_trials=100):
        """
        Optimise les hyperparamètres du modèle XGBoost via Optuna.
        """
        def objective(trial):
            params = {
                'max_depth': trial.suggest_int('max_depth', 3, 12),
                'learning_rate': trial.suggest_float('learning_rate', 0.001, 0.3, log=True),
                'n_estimators': trial.suggest_int('n_estimators', 100, 2000),
                'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
                'subsample': trial.suggest_float('subsample', 0.5, 1.0),
                'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
                'gamma': trial.suggest_float('gamma', 0, 10),
                'reg_alpha': trial.suggest_float('reg_alpha', 0, 10),
                'reg_lambda': trial.suggest_float('reg_lambda', 0, 10)
            }
            model = xgb.XGBRegressor(**params, random_state=self.random_state)
            cv = RepeatedKFold(n_splits=5, n_repeats=3, random_state=self.random_state)
            scores = cross_val_score(model, X, y, cv=cv, scoring='neg_mean_squared_error', n_jobs=-1)
            return -scores.mean()

        study = optuna.create_study(direction='minimize')
        study.optimize(objective, n_trials=n_trials)
        return study.best_params

    def evaluate_model(self, y_true, y_pred):
        """
        Évalue les performances du modèle avec plusieurs métriques.
        """
        metrics = {
            'MSE': mean_squared_error(y_true, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
            'MAE': mean_absolute_error(y_true, y_pred),
            'R2': r2_score(y_true, y_pred),
            'MAPE': np.mean(np.abs((y_true - y_pred) / y_true)) * 100,
            'MedianAPE': np.median(np.abs((y_true - y_pred) / y_true)) * 100
        }
        return metrics

    def train_and_evaluate(self, df):
        """
        Prépare les données, entraîne et évalue le modèle.
        """
        # Préparation des données
        df = self.prepare_data(df)
        X = df.drop('market_value', axis=1)
        y = df['market_value']

        # Création des caractéristiques avancées
        X = self.create_advanced_features(X)

        # Split des données en ensembles d'entraînement et de test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=self.random_state)

        # Mise à l'échelle des caractéristiques
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        # Optimisation des hyperparamètres
        best_params = self.optimize_hyperparameters(X_train_scaled, y_train)

        # Entraînement du modèle XGBoost avec les meilleurs hyperparamètres
        model = xgb.XGBRegressor(**best_params, random_state=self.random_state)
        model.fit(X_train_scaled, y_train)

        # Prédictions et évaluation
        y_pred = model.predict(X_test_scaled)
        metrics = self.evaluate_model(y_test, y_pred)

        return model, metrics

def main():
    # Charger le jeu de données
    df = pd.read_csv('/content/model_training_data.csv')

    # Initialiser le constructeur du modèle XGBoost
    model_builder = XGBoostModelBuilder(random_state=1937)

    # Entraîner et évaluer le modèle
    model, metrics = model_builder.train_and_evaluate(df)

    # Afficher les métriques d'évaluation
    print("Model Evaluation Metrics:")
    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")

    # Sauvegarder le modèle dans un fichier pickle
    with open('model.pkl', 'wb') as file:
        pickle.dump(model, file)

if __name__ == "__main__":
    main()
