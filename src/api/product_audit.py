from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.database import get_db
from src.repositories.product_audit_repository import ProductAuditRepository
from src.schemas.product_audit import ProductAudit

router = APIRouter()


def get_audit_repo(db: Session = Depends(get_db)) -> ProductAuditRepository:
    return ProductAuditRepository(db)


@router.get("/products/{product_id}/history", response_model=List[ProductAudit], status_code=status.HTTP_200_OK)
def get_product_history(product_id: int, repo: ProductAuditRepository = Depends(get_audit_repo)):
    """Get product change history - shows all changes made to a product"""
    history = repo.find_by_product_id(product_id)
    return history if history else []


