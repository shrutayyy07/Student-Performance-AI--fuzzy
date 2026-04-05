from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from .database import Base

class PredictionRecord(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    attendance = Column(Float)
    assignment = Column(Float)
    test = Column(Float)
    fuzzy_score = Column(Float)
    prediction = Column(String)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
