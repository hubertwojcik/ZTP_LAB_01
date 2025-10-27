"""
Environment setup for Behave tests.
"""
import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def before_all(context):
    """Set up test environment before all scenarios."""
    from src.config import get_settings
    
    context.config = get_settings()
    context.base_url = os.environ.get('BASE_URL', 'http://localhost:8000')


def before_scenario(context, scenario):
    """Set up for each scenario."""
    pass


def after_scenario(context, scenario):
    """Clean up after each scenario."""
    pass


def after_all(context):
    """Clean up after all scenarios."""
    pass

