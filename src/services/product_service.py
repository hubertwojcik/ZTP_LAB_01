"""
Business Logic Layer - Product Service
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from src.schemas.product import ProductCreate, ProductUpdate
from src.models.product import Product
from src.repositories.product_repository import ProductRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.forbidden_phrase_repository import ForbiddenPhraseRepository
from src.repositories.product_audit_repository import ProductAuditRepository
from src.models.product_audit import ProductAudit


class ProductService:
    """Service layer for product business logic"""
    
    def __init__(self, db: Session):
        self.db = db
        self.product_repo = ProductRepository(db)
        self.category_repo = CategoryRepository(db)
        self.forbidden_phrase_repo = ForbiddenPhraseRepository(db)
        self.audit_repo = ProductAuditRepository(db)
    
    def _validate_name_not_forbidden(self, name: str):
        """Check if product name contains forbidden phrases"""
        forbidden_phrases = self.forbidden_phrase_repo.find_all_phrases()
        for phrase_obj in forbidden_phrases:
            phrase_text = phrase_obj.phrase if hasattr(phrase_obj, 'phrase') else str(phrase_obj)
            if phrase_text.lower() in name.lower():
                raise ValueError(f'Product name contains forbidden phrase: "{phrase_text}"')
    
    def _validate_price_range(self, price: float, category_id: int):
        """Validate price is within category limits"""
        category = self.category_repo.find_by_id(category_id)
        if not category:
            raise ValueError(f"Category with ID {category_id} not found")
        
        if price < category.min_price or price > category.max_price:
            raise ValueError(
                f"Price must be between {category.min_price} and {category.max_price} for category '{category.name}'"
            )
    
    def _validate_name_unique(self, name: str, exclude_product_id: Optional[int] = None):
        """Check if product name is unique"""
        existing_product = self.product_repo.find_by_name(name)
        if existing_product and existing_product.id != exclude_product_id:
            raise ValueError(f"Product with name '{name}' already exists")
    
    def get_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Get all products"""
        return self.product_repo.find_all(skip=skip, limit=limit)
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self.product_repo.find_by_id(product_id)
    
    def create_product(self, product_data: ProductCreate) -> Product:
        """Create new product with validation"""
        self._validate_name_not_forbidden(product_data.name)
        
        self._validate_name_unique(product_data.name)
        
        self._validate_price_range(product_data.price, product_data.category_id)
        
        new_product = Product(**product_data.model_dump())
        created_product = self.product_repo.create(new_product)
        
        self._log_change(created_product.id, 'product', None, 'create', 'CREATE')
        
        return created_product
    
    def update_product(self, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
        """Update product with validation"""
        product = self.product_repo.find_by_id(product_id)
        if not product:
            return None
        
        update_dict = product_data.model_dump(exclude_unset=True)
        
        if 'name' in update_dict:
            self._validate_name_not_forbidden(update_dict['name'])
            self._validate_name_unique(update_dict['name'], exclude_product_id=product_id)
        
        if 'price' in update_dict:
            category_id = update_dict.get('category_id', product.category_id)
            self._validate_price_range(update_dict['price'], category_id)
        
        for field, value in update_dict.items():
            old_value = getattr(product, field)
            setattr(product, field, value)
            self._log_change(product.id, field, str(old_value), str(value), 'UPDATE')
        
        return self.product_repo.update(product)
    
    def delete_product(self, product_id: int) -> bool:
        """Delete product"""
        product = self.product_repo.find_by_id(product_id)
        if not product:
            return False
        
        self._log_change(product.id, 'product', None, None, 'DELETE')
        
        from src.database import SessionLocal
        db = SessionLocal()
        try:
            from src.models.product_audit import ProductAudit
            db.query(ProductAudit).filter(ProductAudit.product_id == product_id).delete()
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()
        
        self.product_repo.delete(product)
        
        return True
    
    def _log_change(self, product_id: int, field_name: str, old_value: str, new_value: str, change_type: str):
        """Log product change to audit trail"""
        audit = ProductAudit(
            product_id=product_id,
            field_name=field_name,
            old_value=old_value,
            new_value=new_value,
            change_type=change_type
        )
        self.audit_repo.create(audit)

