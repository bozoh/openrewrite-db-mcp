"""
OpenRewrite Recipe Extractor Library

This package provides functionality to extract OpenRewrite recipes
from HTML documentation and generate structured JSON databases.
"""

from .recipe_extractor import RecipeExtractor
from .recipe_repository import RecipeRepository
from .mcp_service import RecipeMcpService

__version__ = "1.0.0"
__all__ = ["RecipeExtractor", "RecipeRepository", "RecipeMcpService"]
