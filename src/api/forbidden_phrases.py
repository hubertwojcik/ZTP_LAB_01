from src.repositories.forbidden_phrase_repository import ForbiddenPhraseRepository
from src.database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.schemas.forbidden_phrase import ForbiddenPhrase, ForbiddenPhraseCreate


router = APIRouter()

def get_forbidden_phrase_repository(db: Session = Depends(get_db)) -> ForbiddenPhraseRepository:
    return ForbiddenPhraseRepository(db)


@router.get("/", response_model=List[ForbiddenPhrase], status_code=status.HTTP_200_OK)
def get_forbidden_phrases(repository: ForbiddenPhraseRepository = Depends(get_forbidden_phrase_repository)):
    """Get all forbidden phrases"""
    forbidden_phrases = repository.find_all_phrases()
    return forbidden_phrases if forbidden_phrases else []

@router.post("/", response_model=ForbiddenPhrase, status_code=status.HTTP_201_CREATED)
def create_forbidden_phrase(forbidden_phrase: ForbiddenPhraseCreate, repository: ForbiddenPhraseRepository = Depends(get_forbidden_phrase_repository)):
    """Create a new forbidden phrase"""
    try:
        # Check if phrase already exists
        existing_phrase = repository.find_by_phrase(forbidden_phrase.phrase)
        if existing_phrase:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Forbidden phrase already exists")
        
        # Create new phrase
        created_phrase = repository.create(forbidden_phrase.phrase)
        return created_phrase
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal server error: {str(e)}")