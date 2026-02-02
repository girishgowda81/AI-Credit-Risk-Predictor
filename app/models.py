from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Borrower(Base):
    __tablename__ = "borrowers"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    income = Column(Float)
    employment_status = Column(String)  # Employed, Self-Employed, Unemployed, etc.
    employment_duration = Column(Integer)  # in months
    housing_status = Column(String)  # Own, Rent, Free
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    applications = relationship("LoanApplication", back_populates="borrower")

class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    borrower_id = Column(Integer, ForeignKey("borrowers.id"))
    loan_amount = Column(Float)
    loan_purpose = Column(String)
    tenure = Column(Integer)  # in months
    interest_rate = Column(Float)
    credit_score = Column(Integer)
    previous_defaults = Column(Integer, default=0)
    debt_to_income_ratio = Column(Float)
    status = Column(String, default="pending")  # approved, rejected, pending
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    borrower = relationship("Borrower", back_populates="applications")
    prediction = relationship("PredictionHistory", back_populates="application", uselist=False)

class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("loan_applications.id"))
    probability = Column(Float)
    risk_level = Column(String)  # Low, Medium, High
    prediction = Column(Boolean)  # True = Default, False = No Default
    feature_importance = Column(Text)  # JSON string of SHAP values or importance
    model_version = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    application = relationship("LoanApplication", back_populates="prediction")
