"""
Data Access Layer - Forbidden Phrase Repository
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from src.models.forbidden_phrase import ForbiddenPhrase


class ForbiddenPhraseRepository:
    """Repository for database operations on ForbiddenPhrase model"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_all_phrases(self) -> List[ForbiddenPhrase]:
        """Get all forbidden phrases as list of ForbiddenPhrase objects"""
        return self.db.query(ForbiddenPhrase).all()
    
    def create(self, phrase: str) -> ForbiddenPhrase:
        """Add new forbidden phrase"""
        try:
            new_phrase = ForbiddenPhrase(phrase=phrase)
            self.db.add(new_phrase)
            self.db.commit()
            self.db.refresh(new_phrase)
            return new_phrase
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError(f"Forbidden phrase already exists or database error: {str(e)}")
        except Exception as e:
            self.db.rollback()
            raise ValueError(f"Error creating forbidden phrase: {str(e)}")
    
    def find_by_phrase(self, phrase: str) -> Optional[ForbiddenPhrase]:
        """Find phrase by text"""
        return self.db.query(ForbiddenPhrase).filter(ForbiddenPhrase.phrase == phrase).first()

