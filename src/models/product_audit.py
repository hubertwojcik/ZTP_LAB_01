"""
Model for tracking product change history (audit log)
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from src.database import Base


class ProductAudit(Base):
    __tablename__ = "product_audits"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    field_name = Column(String, nullable=False, description="Name of the field that changed")
    old_value = Column(String, nullable=True, description="Previous value")
    new_value = Column(String, nullable=True, description="New value")
    change_type = Column(String, nullable=False, description="Type: create, update, delete")
    changed_at = Column(DateTime(timezone=True), server_default=func.now())

