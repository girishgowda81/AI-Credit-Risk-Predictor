from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class BorrowerBase(BaseModel):
    full_name: str
    age: int
    gender: str
    income: float
    employment_duration: int
    housing_status: str

class LoanApplicationBase(BaseModel):
    loan_amount: float
    loan_purpose: str
    tenure: int
    interest_rate: float
    credit_score: int
    previous_defaults: int
    debt_to_income_ratio: float

class LoanApplicationCreate(LoanApplicationBase):
    borrower: BorrowerBase

class PredictionExplanation(BaseModel):
    feature: str
    impact: float

class PredictionResponse(BaseModel):
    application_id: int
    probability: float
    risk_level: str
    prediction: bool
    explanation: List[PredictionExplanation]
    recommendation: str

class ModelMetrics(BaseModel):
    accuracy: float
    auc_roc: float
    last_trained: datetime
    version: str
