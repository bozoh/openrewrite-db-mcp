from typing import List, Dict, Optional, Any
from lib.recipe_repository import RecipeRepository


class RecipeMcpService:
    """
    Service layer for MCP operations on RecipeRepository.
    Handles input validation and error handling for MCP tool calls.
    """

    def __init__(self, recipe_repository: RecipeRepository):
        """
        Initialize the service with a RecipeRepository instance.

        Args:
            recipe_repository: The repository to delegate operations to
        """
        self._repository = recipe_repository

    def get_recipe_by_id(self, recipe_id: str) -> Dict[str, Any]:
        """
        Get a single recipe by its ID.

        Args:
            recipe_id: The recipe ID to search for

        Returns:
            Recipe dictionary if found, empty dict if not found or invalid input
        """
        if not recipe_id or not isinstance(recipe_id, str) or recipe_id.strip() == "":
            return {}

        try:
            return self._repository.get_recipe_by_id(recipe_id.strip())
        except Exception:
            return {}

    def get_recipes_by_name(self, name_query: str) -> List[Dict[str, Any]]:
        """
        Get recipes by partial name match (case-insensitive).

        Args:
            name_query: The partial name to search for

        Returns:
            List of recipe dictionaries with names containing the query
        """
        if not name_query or not isinstance(name_query, str) or name_query.strip() == "":
            return []

        try:
            return self._repository.get_recipes_by_name(name_query.strip())
        except Exception:
            return []

    def get_recipes_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """
        Get recipes that contain a specific tag.

        Args:
            tag: The tag to search for

        Returns:
            List of recipe dictionaries containing the tag
        """
        if not tag or not isinstance(tag, str) or tag.strip() == "":
            return []

        try:
            return self._repository.get_recipes_by_tag(tag.strip())
        except Exception:
            return []

    def get_recipes_by_category(self, category: str, subcategory: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get recipes by category and optional subcategory.

        Args:
            category: The category name to filter by
            subcategory: Optional subcategory name to further filter

        Returns:
            List of recipe dictionaries matching the criteria
        """
        if not category or not isinstance(category, str) or category.strip() == "":
            return []

        try:
            return self._repository.get_recipes_by_category(category.strip(), subcategory.strip() if subcategory and isinstance(subcategory, str) and subcategory.strip() else None)
        except Exception:
            return []

    def get_recipes_by_dependency(self, dependency: str) -> List[Dict[str, Any]]:
        """
        Get recipes by dependency (partial match, case-insensitive).

        Args:
            dependency: The dependency string to search for

        Returns:
            List of recipe dictionaries with matching dependencies
        """
        if not dependency or not isinstance(dependency, str) or dependency.strip() == "":
            return []

        try:
            return self._repository.get_recipes_by_dependency(dependency.strip())
        except Exception:
            return []

    def get_all_categories(self) -> List[str]:
        """
        Get all unique categories from the recipes.

        Returns:
            List of unique category names, sorted alphabetically
        """
        try:
            return self._repository.get_all_categories()
        except Exception:
            return []

    def get_subcategories_by_category(self, category: str) -> List[str]:
        """
        Get all subcategories for a specific category.

        Args:
            category: The category name to filter by

        Returns:
            List of unique subcategory names for the given category
        """
        if not category or not isinstance(category, str) or category.strip() == "":
            return []

        try:
            return self._repository.get_subcategories_by_category(category.strip())
        except Exception:
            return []

    def get_categories_with_subcategories(self) -> List[Dict[str, Any]]:
        """
        Get all categories with their respective subcategories.

        Returns:
            List of dicts with 'category' and 'sub-categories' keys
        """
        try:
            return self._repository.get_categories_with_subcategories()
        except Exception:
            return []
