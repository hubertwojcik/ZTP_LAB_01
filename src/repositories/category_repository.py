"""
Data Access Layer - Category Repository
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.product_category import ProductCategory


class CategoryRepository:
    """Repository for database operations on ProductCategory model"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, category_id: int) -> Optional[ProductCategory]:
        """Find category by ID"""
        return self.db.query(ProductCategory).filter(ProductCategory.id == category_id).first()
    
    def find_all(self) -> List[ProductCategory]:
        """Find all categories"""
        return self.db.query(ProductCategory).all()

