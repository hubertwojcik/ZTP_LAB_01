"""
Data Access Layer - Forbidden Phrase Repository
"""
from sqlalchemy.orm import Session
from typing import List
from src.models.forbidden_phrase import ForbiddenPhrase


class ForbiddenPhraseRepository:
    """Repository for database operations on ForbiddenPhrase model"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_all_phrases(self) -> List[str]:
        """Get all forbidden phrases as list of strings"""
        phrases = self.db.query(ForbiddenPhrase).all()
        return [phrase.phrase for phrase in phrases]
    
    def create(self, phrase: str) -> ForbiddenPhrase:
        """Add new forbidden phrase"""
        new_phrase = ForbiddenPhrase(phrase=phrase)
        self.db.add(new_phrase)
        self.db.commit()
        self.db.refresh(new_phrase)
        return new_phrase
    
    def find_by_phrase(self, phrase: str) -> ForbiddenPhrase:
        """Find phrase by text"""
        return self.db.query(ForbiddenPhrase).filter(ForbiddenPhrase.phrase == phrase).first()

