from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ProductCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Category name")
    description: Optional[str] = Field(None, max_length=500, description="Category description")
    min_price: float = Field(..., ge=0, description="Minimum price for products in this category")
    max_price: float = Field(..., gt=0, description="Maximum price for products in this category")
    
    @field_validator('max_price')
    @classmethod
    def validate_max_price(cls, v, info):
        if 'min_price' in info.data and v <= info.data['min_price']:
            raise ValueError('max_price must be greater than min_price')
        return v


class ProductCategoryCreate(ProductCategoryBase):
    pass


class ProductCategory(ProductCategoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

