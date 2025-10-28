"""
Data Access Layer - Product Repository
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.product import Product


class ProductRepository:
    """Repository for database operations on Product model"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_id(self, product_id: int) -> Optional[Product]:
        """Find product by ID"""
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def find_by_name(self, name: str) -> Optional[Product]:
        """Find product by name"""
        return self.db.query(Product).filter(Product.name == name).first()
    
    def find_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Find all products with pagination"""
        return self.db.query(Product).offset(skip).limit(limit).all()
    
    def create(self, product: Product) -> Product:
        """Create new product"""
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def update(self, product: Product) -> Product:
        """Update existing product"""
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def delete(self, product: Product) -> None:
        """Delete product"""
        self.db.delete(product)
        self.db.commit()

