import shap
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import io
import base64

def get_prediction_explanation(model, preprocessor, input_data):
    """
    Generates SHAP values for a single prediction.
    input_data: pd.DataFrame with raw features
    """
    # Process data
    X_processed = preprocessor.transform(input_data)
    
    # Get feature names from preprocessor
    feature_names = preprocessor.get_feature_names_out()
    
    # Create explainer
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_processed)
    
    # For classification, shap_values might be a list (one for each class)
    if isinstance(shap_values, list):
        shap_values = shap_values[1] # Probability of default
    
    # Format results
    explanation = []
    for i, feature in enumerate(feature_names):
        explanation.append({
            "feature": feature,
            "impact": float(shap_values[0][i])
        })
    
    # Sort by absolute impact
    explanation = sorted(explanation, key=lambda x: abs(x['impact']), reverse=True)
    
    return explanation

def plot_feature_importance(model, preprocessor):
    """
    Generates a global feature importance plot.
    """
    feature_names = preprocessor.get_feature_names_out()
    importances = model.feature_importances_
    
    feat_importances = pd.Series(importances, index=feature_names)
    feat_importances.nlargest(10).plot(kind='barh')
    plt.title('Top 10 Global Risk Factors')
    plt.tight_layout()
    
    # Convert plot to base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()
    
    return img_str
