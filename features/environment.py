"""
Environment setup for Behave tests.
"""
import os
import sys
import requests
from pathlib import Path


project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    from src.database import SessionLocal, engine, Base
    from src.models.product import Product
    from src.models.product_category import ProductCategory
    from src.models.forbidden_phrase import ForbiddenPhrase
    from src.models.product_audit import ProductAudit
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

def before_all(context):
    """Set up test environment before all scenarios."""
    context.base_url = os.environ.get('BASE_URL', 'http://localhost:8000')
    context.session = requests.Session()
        
    try:
        response = context.session.get(f"{context.base_url}/health", timeout=5)
        if response.status_code != 200:
            print(f"Warning: API health check returned {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Warning: Could not connect to API at {context.base_url}: {e}")


def before_scenario(context, scenario):
    """Set up for each scenario."""    
    if DB_AVAILABLE:
        try:
            db = SessionLocal()
            try:                
                db.query(ProductAudit).delete()
                db.query(Product).delete()
                db.query(ProductCategory).delete()
                db.query(ForbiddenPhrase).delete()
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Warning: Could not clean database before scenario: {e}")
            finally:
                db.close()
        except Exception as e:
            print(f"Warning: Could not connect to database for cleanup: {e}")
    
    context.response = None
    context.product = None
    context.product_id = None
    context.category = None
    context.category_id = None
    context.forbidden_phrase = None
    context.forbidden_phrase_id = None
    context.created_products = []
    context.created_categories = []
    context.created_forbidden_phrases = []


def after_scenario(context, scenario):
    """Clean up after each scenario."""    
    pass


def after_all(context):
    """Clean up after all scenarios."""
    if hasattr(context, 'session'):
        context.session.close()

