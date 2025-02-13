"""
API routers module.
"""

from .files import router as files_router
from .scores import router as scores_router

__all__ = ["files_router", "scores_router"]
