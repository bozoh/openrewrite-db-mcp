import json
import os
from typing import List, Dict, Optional, Any, Iterator
import ijson
from jsonpath_ng import parse as jsonpath_parse


class RecipeRepository:
    """
    Repository for querying OpenRewrite recipes stored in JSON format using JSONPath.
    """

    def __init__(self, json_file_path: str):
        """
        Initialize the repository with a path to the JSON file containing the recipes.

        Args:
            json_file_path: Path to the JSON file containing the recipes
        """
        if not json_file_path or not isinstance(json_file_path, str):
            raise ValueError("json_file_path must be a non-empty string")

        self.json_file_path = json_file_path

    def _stream_recipes(self) -> Iterator[Dict[str, Any]]:
        """
        Stream recipes from the JSON file one by one.

        Yields:
            Recipe dictionaries from the JSON file
        """
        try:
            if not os.path.exists(self.json_file_path):
                return

            with open(self.json_file_path, 'rb') as f:
                for item in ijson.items(f, 'item'):
                    if isinstance(item, dict):
                        yield item
        except (ijson.IncompleteJSONError, IOError, Exception):
            return

    def get_all_categories(self) -> List[str]:
        """
        Get all unique categories from the recipes.

        Returns:
            List of unique category names, sorted alphabetically
        """
        categories = set()
        for recipe in self._stream_recipes():
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

        for recipe in self._stream_recipes():
            category_val = recipe.get('category')
            category = category_val.lower() if isinstance(category_val, str) else None
            subcategory_val = recipe.get('sub-category')
            subcategory = subcategory_val.lower() if isinstance(subcategory_val, str) else None

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

        for recipe in self._stream_recipes():
            category_val = recipe.get('category')
            if isinstance(category_val, str) and category_val.lower() == category_lower:
                subcategory_val = recipe.get('sub-category')
                if isinstance(subcategory_val, str):
                    subcategories.add(subcategory_val.lower())

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
        for recipe in self._stream_recipes():
            category_val = recipe.get('category')
            if isinstance(category_val, str) and category_val.lower() == category_lower:
                if subcategory_lower is None:
                    results.append(recipe)
                else:
                    subcategory_val = recipe.get('sub-category')
                    if isinstance(subcategory_val, str) and subcategory_val.lower() == subcategory_lower:
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

        for recipe in self._stream_recipes():
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

        for recipe in self._stream_recipes():
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

        for recipe in self._stream_recipes():
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

        for recipe in self._stream_recipes():
            dep = recipe.get('dependency', '')
            if isinstance(dep, str) and dependency_lower in dep.lower():
                results.append(recipe)

        return results
