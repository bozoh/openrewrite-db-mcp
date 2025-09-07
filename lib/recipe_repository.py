import json
import os
from typing import List, Dict, Optional, Any
from jsonpath_ng import parse as jsonpath_parse


class RecipeRepository:
    """
    Repository for querying OpenRewrite recipes stored in JSON format using JSONPath.
    """

    def __init__(self, json_file_path: str):
        """
        Initialize the repository with the path to the JSON file.

        Args:
            json_file_path: Path to the JSON file containing the recipes
        """
        self.json_file_path = json_file_path
        self._data: Optional[List[Dict[str, Any]]] = None

    @property
    def data(self) -> List[Dict[str, Any]]:
        """Lazy load the data when first accessed."""
        if self._data is None:
            try:
                if not os.path.exists(self.json_file_path):
                    self._data = []
                else:
                    with open(self.json_file_path, 'r', encoding='utf-8') as f:
                        loaded_data = json.load(f)

                    if loaded_data is None:
                        self._data = []
                    elif isinstance(loaded_data, list):
                        # Filter out non-dict items
                        self._data = [item for item in loaded_data if isinstance(item, dict)]
                    else:
                        self._data = []
            except (json.JSONDecodeError, IOError, Exception):
                self._data = []
        return self._data

    def get_all_categories(self) -> List[str]:
        """
        Get all unique categories from the recipes.

        Returns:
            List of unique category names, sorted alphabetically
        """
        categories = set()
        for recipe in self.data:
            category = recipe.get('category')
            if category and isinstance(category, str):
                categories.add(category.lower())

        return sorted(list(categories))

    def get_categories_with_subcategories(self) -> List[Dict[str, Any]]:
        """
        Get all categories with their respective subcategories.

        Returns:
            List of dicts with 'category' and 'sub-categories' keys
        """
        category_map = {}

        for recipe in self.data:
            category = recipe.get('category', '').lower()
            subcategory = recipe.get('sub-category', '').lower() if recipe.get('sub-category') else None

            if category:
                if category not in category_map:
                    category_map[category] = set()

                if subcategory:
                    category_map[category].add(subcategory)

        result = []
        for category in sorted(category_map.keys()):
            subcategories = sorted(list(category_map[category]))
            result.append({
                'category': category,
                'sub-categories': subcategories
            })

        return result

    def get_subcategories_by_category(self, category: str) -> List[str]:
        """
        Get all subcategories for a specific category.

        Args:
            category: The category name to filter by

        Returns:
            List of unique subcategory names for the given category
        """
        if not category or not isinstance(category, str):
            return []

        category_lower = category.lower()
        subcategories = set()

        for recipe in self.data:
            if recipe.get('category', '').lower() == category_lower:
                subcategory = recipe.get('sub-category')
                if subcategory:
                    subcategories.add(subcategory.lower())

        return sorted(list(subcategories))

    def get_recipes_by_category(self, category: str, subcategory: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get recipes by category and optional subcategory.

        Args:
            category: The category name to filter by
            subcategory: Optional subcategory name to further filter

        Returns:
            List of recipe dictionaries matching the criteria
        """
        if not category or not isinstance(category, str):
            return []

        category_lower = category.lower()
        subcategory_lower = subcategory.lower() if subcategory and isinstance(subcategory, str) else None

        results = []
        for recipe in self.data:
            if recipe.get('category', '').lower() == category_lower:
                if subcategory_lower is None:
                    results.append(recipe)
                elif recipe.get('sub-category', '').lower() == subcategory_lower:
                    results.append(recipe)

        return results

    def get_recipes_by_tag(self, tag: str) -> List[Dict[str, Any]]:
        """
        Get recipes that contain a specific tag.

        Args:
            tag: The tag to search for

        Returns:
            List of recipe dictionaries containing the tag
        """
        if not tag or not isinstance(tag, str):
            return []

        tag_lower = tag.lower()
        results = []

        for recipe in self.data:
            tags = recipe.get('tags', [])
            if isinstance(tags, list):
                for recipe_tag in tags:
                    if isinstance(recipe_tag, str) and recipe_tag.lower() == tag_lower:
                        results.append(recipe)
                        break

        return results

    def get_recipes_by_name(self, name_query: str) -> List[Dict[str, Any]]:
        """
        Get recipes by partial name match (case-insensitive).

        Args:
            name_query: The partial name to search for

        Returns:
            List of recipe dictionaries with names containing the query
        """
        if not name_query or not isinstance(name_query, str):
            return []

        query_lower = name_query.lower()
        results = []

        for recipe in self.data:
            name = recipe.get('name', '')
            if isinstance(name, str) and query_lower in name.lower():
                results.append(recipe)

        return results

    def get_recipe_by_id(self, recipe_id: str) -> Dict[str, Any]:
        """
        Get a single recipe by its ID.

        Args:
            recipe_id: The recipe ID to search for

        Returns:
            Recipe dictionary if found, empty dict if not found
        """
        if not recipe_id or not isinstance(recipe_id, str):
            return {}

        for recipe in self.data:
            if recipe.get('id') == recipe_id:
                return recipe

        return {}

    def get_recipes_by_dependency(self, dependency: str) -> List[Dict[str, Any]]:
        """
        Get recipes by dependency (partial match, case-insensitive).

        Args:
            dependency: The dependency string to search for

        Returns:
            List of recipe dictionaries with matching dependencies
        """
        if not dependency or not isinstance(dependency, str):
            return []

        dependency_lower = dependency.lower()
        results = []

        for recipe in self.data:
            dep = recipe.get('dependency', '')
            if isinstance(dep, str) and dependency_lower in dep.lower():
                results.append(recipe)

        return results
