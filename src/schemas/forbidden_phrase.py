from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ForbiddenPhrase(BaseModel):
    phrase: str
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ForbiddenPhraseCreate(BaseModel):
    phrase: str

