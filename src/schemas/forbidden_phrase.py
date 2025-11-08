from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class ForbiddenPhrase(BaseModel):
    id: int
    phrase: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ForbiddenPhraseCreate(BaseModel):
    phrase: str = Field(..., min_length=1, max_length=100, description="The forbidden phrase (1-100 characters)")
    
    @field_validator('phrase')
    @classmethod
    def validate_phrase(cls, v):
        if not v or not v.strip():
            raise ValueError('Phrase cannot be empty or whitespace only')
        return v.strip()

