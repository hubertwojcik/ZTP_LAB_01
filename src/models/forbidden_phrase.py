"""
Model for forbidden phrases in product names
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from src.database import Base


class ForbiddenPhrase(Base):
    __tablename__ = "forbidden_phrases"
    
    id = Column(Integer, primary_key=True, index=True)
    phrase = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

