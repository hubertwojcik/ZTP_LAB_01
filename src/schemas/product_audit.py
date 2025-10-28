from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProductAudit(BaseModel):
    id: int
    product_id: int
    field_name: str
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    change_type: str
    changed_at: datetime
    
    class Config:
        from_attributes = True

