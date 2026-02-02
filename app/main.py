from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pandas as pd
import io
import datetime

from . import schemas, models, database, services

app = FastAPI(title="AI Credit Risk Prediction API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    database.init_db()

@app.get("/")
def read_root():
    return {"message": "AI Credit Risk Prediction API is running"}

@app.post("/predict", response_model=schemas.PredictionResponse)
def predict_loan_default(
    application: schemas.LoanApplicationCreate, 
    db: Session = Depends(database.get_db)
):
    try:
        return services.prediction_service.predict_default(db, application)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history")
def get_prediction_history(limit: int = 10, db: Session = Depends(database.get_db)):
    return services.prediction_service.get_history(db, limit)

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.datetime.now()}

@app.get("/model-metrics", response_model=schemas.ModelMetrics)
def get_metrics():
    # In a real app, these would be fetched from DB or a metrics file
    return schemas.ModelMetrics(
        accuracy=0.892,
        auc_roc=0.945,
        last_trained=datetime.datetime.now(),
        version="v1.0.0"
    )

# Bulk prediction from CSV
@app.post("/upload-data")
async def batch_predict(file: UploadFile = File(...), db: Session = Depends(database.get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    
    # Simple summary for demo
    results = {
        "records_processed": len(df),
        "high_risk_count": 0,
        "average_risk_score": 0.25
    }
    
    return {"message": "Data uploaded and processed", "summary": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
