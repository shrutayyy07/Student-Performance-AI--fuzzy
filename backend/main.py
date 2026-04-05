from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uvicorn
import os

from ai_models.nn_model import predict_performance
from fuzzy_logic.fuzzy_system import compute_fuzzy_score
from data.database import Base, engine, get_db
from data.models import PredictionRecord
from ai_models.train import train_and_save, MODEL_PATH

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hybrid Student Performance Prediction AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictionRequest(BaseModel):
    attendance: float
    assignment: float
    test: float

class PredictionResponse(BaseModel):
    attendance: float
    assignment: float
    test: float
    fuzzy_score: float
    prediction: str
    confidence: float

@app.post("/predict", response_model=PredictionResponse)
def predict(req: PredictionRequest, db: Session = Depends(get_db)):
    if req.attendance < 0 or req.attendance > 100 or \
       req.assignment < 0 or req.assignment > 100 or \
       req.test < 0 or req.test > 100:
        raise HTTPException(status_code=400, detail="Scores must be between 0 and 100")
        
    # 1. Fuzzy Logic Component
    fuzzy_score = compute_fuzzy_score(req.attendance, req.assignment, req.test)
    
    # Check if model exists, if not, train it
    if not os.path.exists(MODEL_PATH):
        print("Model not found. Training model automatically...")
        train_and_save()
        
    # 2. Neural Network Component (Hybrid Integration)
    prediction_class, confidence = predict_performance(
        req.attendance, req.assignment, req.test, fuzzy_score
    )
    
    # 3. Save to database
    record = PredictionRecord(
        attendance=req.attendance,
        assignment=req.assignment,
        test=req.test,
        fuzzy_score=fuzzy_score,
        prediction=prediction_class,
        confidence=confidence
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    
    return PredictionResponse(
        attendance=req.attendance,
        assignment=req.assignment,
        test=req.test,
        fuzzy_score=fuzzy_score,
        prediction=prediction_class,
        confidence=confidence
    )

@app.post("/train")
def train_model():
    try:
        train_and_save()
        return {"status": "success", "message": "Model trained and saved."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
