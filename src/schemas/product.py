from pydantic import BaseModel, Field, validator, field_validator
from typing import Optional
from datetime import datetime
import re


class ProductBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=20, description="Product name (3-20 chars, alphanumeric only)")
    price: float = Field(..., gt=0, description="Product price (must be greater than 0)")
    quantity: int = Field(..., ge=0, description="Available quantity (must be >= 0)")
    category_id: int = Field(..., gt=0, description="Product category ID (must be greater than 0)")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not v:
            raise ValueError('Product name cannot be empty')
        if not re.match('^[a-zA-Z0-9]+$', v):
            raise ValueError('Product name must contain only letters and digits (no spaces or special characters)')
        return v
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('Product price must be greater than 0')
        return v
    
    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v):
        if v < 0:
            raise ValueError('Product quantity cannot be negative')
        return v


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=20, description="Product name (3-20 chars, alphanumeric only)")
    price: Optional[float] = Field(None, gt=0, description="Product price (must be greater than 0)")
    quantity: Optional[int] = Field(None, ge=0, description="Available quantity (must be >= 0)")
    category_id: Optional[int] = Field(None, gt=0, description="Product category ID (must be greater than 0)")
    
    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if v is not None:
            if not v:
                raise ValueError('Product name cannot be empty')
            if not re.match('^[a-zA-Z0-9]+$', v):
                raise ValueError('Product name must contain only letters and digits (no spaces or special characters)')
        return v
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Product price must be greater than 0')
        return v
    
    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v):
        if v is not None and v < 0:
            raise ValueError('Product quantity cannot be negative')
        return v


class Product(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


