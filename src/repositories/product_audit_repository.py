"""
Data Access Layer - Product Arena Repository
"""
from sqlalchemy.orm import Session
from typing import List
from src.models.product_audit import ProductAudit


class ProductAuditRepository:
    """Repository for database operations on ProductAudit model"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_product_id(self, product_id: int) -> List[ProductAudit]:
        """Get all audit logs for a product"""
        return self.db.query(ProductAudit).filter(
            ProductAudit.product_id == product_id
        ).order_by(ProductAudit.changed_at.desc()).all()
    
    def create(self, audit: ProductAudit) -> ProductAudit:
        """Create new audit log entry"""
        self.db.add(audit)
        self.db.commit()
        self.db.refresh(audit)
        return audit

