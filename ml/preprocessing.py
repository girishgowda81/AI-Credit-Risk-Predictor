import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
import os

def get_preprocessing_pipeline():
    numeric_features = ['age', 'income', 'employment_duration', 'loan_amount', 'tenure', 'credit_score', 'previous_defaults', 'debt_to_income_ratio']
    categorical_features = ['gender', 'housing_status']
    
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])
    
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    return preprocessor

def save_pipeline(pipeline, path='models/preprocessor.pkl'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(pipeline, path)
    print(f"Preprocessor saved to {path}")

def load_pipeline(path='models/preprocessor.pkl'):
    return joblib.load(path)
