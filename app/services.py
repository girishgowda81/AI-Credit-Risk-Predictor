import pandas as pd
import joblib
import os
from sqlalchemy.orm import Session
from . import models, schemas
from ml.explainability import get_prediction_explanation

class PredictionService:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.load_artifacts()

    def load_artifacts(self):
        model_path = 'models/risk_model_v1.pkl'
        preprocessor_path = 'models/preprocessor.pkl'
        
        if os.path.exists(model_path) and os.path.exists(preprocessor_path):
            self.model = joblib.load(model_path)
            self.preprocessor = joblib.load(preprocessor_path)
            print("Model and preprocessor loaded successfully")
        else:
            print("Warning: Model artifacts not found. Please train the model first.")

    def get_risk_level(self, prob):
        if prob < 0.3:
            return "Low"
        elif prob < 0.7:
            return "Medium"
        else:
            return "High"

    def predict_default(self, db: Session, application_data: schemas.LoanApplicationCreate):
        # 1. Create borrower and application in DB
        db_borrower = models.Borrower(
            full_name=application_data.borrower.full_name,
            age=application_data.borrower.age,
            gender=application_data.borrower.gender,
            income=application_data.borrower.income,
            employment_status="Employed", # Simple default
            employment_duration=application_data.borrower.employment_duration,
            housing_status=application_data.borrower.housing_status
        )
        db.add(db_borrower)
        db.commit()
        db.refresh(db_borrower)

        db_app = models.LoanApplication(
            borrower_id=db_borrower.id,
            loan_amount=application_data.loan_amount,
            loan_purpose=application_data.loan_purpose,
            tenure=application_data.tenure,
            interest_rate=application_data.interest_rate,
            credit_score=application_data.credit_score,
            previous_defaults=application_data.previous_defaults,
            debt_to_income_ratio=application_data.debt_to_income_ratio
        )
        db.add(db_app)
        db.commit()
        db.refresh(db_app)

        # 2. Prepare data for prediction
        input_dict = {
            'age': [application_data.borrower.age],
            'gender': [application_data.borrower.gender],
            'income': [application_data.borrower.income],
            'employment_duration': [application_data.borrower.employment_duration],
            'housing_status': [application_data.borrower.housing_status],
            'loan_amount': [application_data.loan_amount],
            'tenure': [application_data.tenure],
            'credit_score': [application_data.credit_score],
            'previous_defaults': [application_data.previous_defaults],
            'debt_to_income_ratio': [application_data.debt_to_income_ratio]
        }
        input_df = pd.DataFrame(input_dict)

        # 3. Prediction
        if self.model is None or self.preprocessor is None:
            self.load_artifacts()
            if self.model is None:
                raise Exception("Model not loaded")

        processed_input = self.preprocessor.transform(input_df)
        prob = float(self.model.predict_proba(processed_input)[:, 1][0])
        prediction = bool(prob > 0.5)
        risk_level = self.get_risk_level(prob)

        # 4. Explanation
        explanation_list = get_prediction_explanation(self.model, self.preprocessor, input_df)
        
        # 5. Save prediction in DB
        db_prediction = models.PredictionHistory(
            application_id=db_app.id,
            probability=prob,
            risk_level=risk_level,
            prediction=prediction,
            feature_importance=str(explanation_list),
            model_version="v1"
        )
        db.add(db_prediction)
        db.commit()

        # 6. Recommendation
        recommendation = "Approved" if prob < 0.4 else "Review Required" if prob < 0.7 else "Reject"

        return schemas.PredictionResponse(
            application_id=db_app.id,
            probability=prob,
            risk_level=risk_level,
            prediction=prediction,
            explanation=[schemas.PredictionExplanation(**e) for e in explanation_list[:5]],
            recommendation=recommendation
        )

    def get_history(self, db: Session, limit: int = 20):
        predictions = db.query(models.PredictionHistory).order_by(models.PredictionHistory.created_at.desc()).limit(limit).all()
        history = []
        for p in predictions:
            history.append({
                "id": p.id,
                "application_id": p.application_id,
                "probability": p.probability,
                "risk_level": p.risk_level,
                "prediction": p.prediction,
                "created_at": p.created_at.isoformat()
            })
        return history

prediction_service = PredictionService()
