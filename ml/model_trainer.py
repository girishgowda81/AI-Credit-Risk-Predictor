import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
import os
from .preprocessing import get_preprocessing_pipeline, save_pipeline

def train_model(data_path='data/synthetic_loan_data.csv'):
    # Load data
    df = pd.read_csv(data_path)
    
    X = df.drop(['borrower_id', 'default'], axis=1)
    y = df['default']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Preprocessing
    preprocessor = get_preprocessing_pipeline()
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    save_pipeline(preprocessor)
    
    # Train XGBoost
    model = XGBClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=5,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    
    model.fit(X_train_processed, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_processed)
    y_prob = model.predict_proba(X_test_processed)[:, 1]
    
    print("Model Evaluation:")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/risk_model_v1.pkl')
    print("Model saved to models/risk_model_v1.pkl")
    
    return model, preprocessor

if __name__ == "__main__":
    train_model()
