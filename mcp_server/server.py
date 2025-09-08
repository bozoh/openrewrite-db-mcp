"""
MCP Server for OpenRewrite recipes database.
Provides tools for querying recipes by various criteria.
"""

import asyncio
from typing import Any, Dict, List
from mcp.server import FastMCP
from lib.recipe_repository import RecipeRepository
from lib.mcp_service import RecipeMcpService


def build_server() -> FastMCP:
    """
    Build and configure the MCP server with all recipe query tools.
    Uses the fixed path 'resource/db/recipes.json' for recipes data.

    Returns:
        Configured FastMCP Server instance
    """
    # Initialize repository and service with fixed path
    repository = RecipeRepository('resource/db/recipes.json')
    service = RecipeMcpService(repository)

    server = FastMCP("openrewrite-recipes")

    @server.tool()
    async def get_recipe_by_id(recipe_id: str) -> str:
        """
        Get a single OpenRewrite recipe by its ID (md5 string).

        Searches for a specific recipe in the OpenRewrite recipes database using the provided ID.

        Args:
            recipe_id: The recipe ID to search for (e.g., "ebe22a8d0299cd2871cb0bb4d5339906")

        Returns:
            JSON string containing the recipe data or empty object {} if not found.
            Response format: {"name": "Recipe Name", "id": "recipe.id", "category": "category", ...}
            or {} if recipe not found
        """
        result = service.get_recipe_by_id(recipe_id)
        return str(result)

    @server.tool()
    async def get_recipes_by_name(name_query: str) -> str:
        """
        Get OpenRewrite recipes by partial name match (case-insensitive).

        Searches for recipes in the OpenRewrite recipes database where the name contains
        the provided query string (case-insensitive partial match).

        Args:
            name_query: The partial name to search for (e.g., "spring", "jdbc")

        Returns:
            JSON string containing a list of matching recipes or empty list [] if none found.
            Response format: [{"name": "Recipe Name", "id": "recipe.id", "category": "category", ...}, ...]
            or [] if no recipes match the query
        """
        result = service.get_recipes_by_name(name_query)
        return str(result)

    @server.tool()
    async def get_recipes_by_tag(tag: str) -> str:
        """
        Get OpenRewrite recipes that contain a specific tag.

        Searches for recipes in the OpenRewrite recipes database that have the specified
        tag in their tags array (case-insensitive exact match).

        Args:
            tag: The tag to search for (e.g., "spring", "java", "database")

        Returns:
            JSON string containing a list of recipes with the specified tag or empty list [] if none found.
            Response format: [{"name": "Recipe Name", "id": "recipe.id", "tags": ["tag1", "tag2"], ...}, ...]
            or [] if no recipes contain the specified tag
        """
        result = service.get_recipes_by_tag(tag)
        return str(result)

    @server.tool()
    async def get_recipes_by_category(category: str, subcategory: str = None) -> str:
        """
        Get OpenRewrite recipes by category and optional subcategory.

        Searches for recipes in the OpenRewrite recipes database that belong to the specified
        category. Optionally filters further by subcategory if provided.

        Args:
            category: The category name to filter by (e.g., "spring", "java", "testing")
            subcategory: Optional subcategory name to further filter (e.g., "jdbc", "web", "junit")

        Returns:
            JSON string containing a list of recipes in the specified category/subcategory or empty list [] if none found.
            Response format: [{"name": "Recipe Name", "id": "recipe.id", "category": "category", "sub-category": "subcategory", ...}, ...]
            or [] if no recipes match the criteria
        """
        result = service.get_recipes_by_category(category, subcategory)
        return str(result)

    @server.tool()
    async def get_recipes_by_dependency(dependency: str) -> str:
        """
        Get OpenRewrite recipes by dependency package name (partial match, case-insensitive).

        Searches for recipes in the OpenRewrite recipes database that have dependencies
        containing the provided string (case-insensitive partial match).

        Args:
            dependency: The dependency string to search for (e.g., "springframework", "junit", "org.springframework")

        Returns:
            JSON string containing a list of recipes with matching dependencies or empty list [] if none found.
            Response format: [{"name": "Recipe Name", "id": "recipe.id", "dependency": "dependency.string", ...}, ...]
            or [] if no recipes have matching dependencies
        """
        result = service.get_recipes_by_dependency(dependency)
        return str(result)

    @server.tool()
    async def get_all_categories() -> str:
        """
        Get all unique categories from the OpenRewrite recipes database.

        Retrieves a list of all unique category names available in the OpenRewrite recipes database,
        sorted alphabetically.

        Returns:
            JSON string containing a list of unique category names.
            Response format: ["category1", "category2", "category3", ...]
        """
        result = service.get_all_categories()
        return str(result)

    @server.tool()
    async def get_subcategories_by_category(category: str) -> str:
        """
        Get all subcategories for a specific category from the OpenRewrite recipes database.

        Retrieves a list of all unique subcategory names that belong to the specified category
        in the OpenRewrite recipes database, sorted alphabetically.

        Args:
            category: The category name to filter by (e.g., "spring", "java", "testing")

        Returns:
            JSON string containing a list of unique subcategory names for the specified category.
            Response format: ["subcategory1", "subcategory2", "subcategory3", ...]
            or [] if category not found or has no subcategories
        """
        result = service.get_subcategories_by_category(category)
        return str(result)

    @server.tool()
    async def get_categories_with_subcategories() -> str:
        """
        Get all categories with their respective subcategories from the OpenRewrite recipes database.

        Retrieves a complete mapping of all categories and their associated subcategories
        from the OpenRewrite recipes database, sorted alphabetically.

        Returns:
            JSON string containing a list of category objects with their subcategories.
            Response format: [
                {"category": "category1", "sub-categories": ["sub1", "sub2"]},
                {"category": "category2", "sub-categories": ["sub3", "sub4"]},
                ...
            ]
        """
        result = service.get_categories_with_subcategories()
        return str(result)

    return server


def main():
    """
    Main entry point for the MCP server.
    Uses the fixed path 'resource/db/recipes.json' for recipes data.
    """
    server = build_server()
    server.run()
