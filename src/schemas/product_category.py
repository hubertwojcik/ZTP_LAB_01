from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    min_price: float
    max_price: float


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategory(ProductCategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

