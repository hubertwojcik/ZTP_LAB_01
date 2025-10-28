from pydantic import BaseModel, Field, validator, field_validator
from typing import Optional
from datetime import datetime
import re


class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=20, description="Product name (3-20 chars, alphanumeric only)")
    price: float = Field(..., gt=0, description="Product price")
    quantity: int = Field(..., ge=0, description="Available quantity (>= 0)")
    category_id: int = Field(..., description="Product category ID")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not re.match('^[a-zA-Z0-9]+$', v):
            raise ValueError('Product name must contain only letters and digits')
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=20)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v is not None and not re.match('^[a-zA-Z0-9]+$', v):
            raise ValueError('Product name must contain only letters and digits')
        return v


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


