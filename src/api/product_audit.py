from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.models.product_audit import ProductAudit as ProductAuditModel
from src.repositories.product_audit_repository import ProductAuditRepository

router = APIRouter()


def get_audit_repo(db: Session = Depends(get_db)) -> ProductAuditRepository:
    return ProductAuditRepository(db)


@router.get("/products/{product_id}/history", status_code=status.HTTP_200_OK)
def get_product_history(product_id: int, repo: ProductAuditRepository = Depends(get_audit_repo)):
    """Get product change history - shows all changes made to a product"""
    history = repo.find_by_product_id(product_id)
    
    if not history:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No history found for this product"
        )
    
    return [
        {
            "id": record.id,
            "product_id": record.product_id,
            "field_name": record.field_name,
            "old_value": record.old_value,
            "new_value": record.new_value,
            "change_type": record.change_type,
            "changed_at": record.changed_at
        }
        for record in history
    ]


