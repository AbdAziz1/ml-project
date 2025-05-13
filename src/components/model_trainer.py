import os
import sys 
from src.utils import save_object, evaluate_models
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    AdaBoostRegressor,
    GradientBoostingRegressor
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test data")
            X_train, y_train, X_test, y_test = (
                train_array[:,:-1], 
                train_array[:,-1], 
                test_array[:,:-1], 
                test_array[:,-1]
            )
            models = {
                'RandomForestRegressor': RandomForestRegressor(),
                'DecisionTreeRegressor': DecisionTreeRegressor(),
                'LinearRegression': LinearRegression(),
                'KNeighborsRegressor': KNeighborsRegressor(),
                'AdaBoostRegressor': AdaBoostRegressor(),
                'GradientBoostingRegressor': GradientBoostingRegressor(),
                'XGBRegressor': XGBRegressor(),
                'CatBoostRegressor': CatBoostRegressor(verbose=0)
            }
            parameters = {
                'RandomForestRegressor': {
                    'n_estimators': [10, 50, 100],
                    'max_features': ['sqrt', 'log2'],
                    'max_depth': [None, 10, 20, 30]
                },
                'DecisionTreeRegressor': {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error'],
                    'max_depth': [None, 10, 20, 30]
                },
                'LinearRegression': {},
                'KNeighborsRegressor': {
                    'n_neighbors': [3, 5, 7],
                    'weights': ['uniform', 'distance']
                },
                'AdaBoostRegressor': {
                    'n_estimators': [50, 100],
                    'learning_rate': [0.01, 0.1, 1.0]
                },
                'GradientBoostingRegressor': {
                    'n_estimators': [100],
                    'learning_rate': [0.01, 0.1],
                    'max_depth': [3, 5]
                },
                'XGBRegressor': {
                    'n_estimators': [100],
                    'learning_rate': [0.01, 0.1],
                    'max_depth': [3, 5]
                },
                'CatBoostRegressor': {
                    'iterations': [100],
                    'depth': [3, 5],
                    'learning_rate': [0.01, 0.1]
                }
            }

            model_report: dict = evaluate_models(X_train = X_train, y_train = y_train, X_test = X_test, y_test = y_test, models = models, parameters = parameters)

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found")
            
            logging.info(f"Best model found: {best_model_name} with score: {best_model_score}")

            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj = best_model
            )

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)

            return r2_square
            

        except Exception as e:
            raise CustomException(e, sys)