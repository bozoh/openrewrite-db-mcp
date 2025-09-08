#!/usr/bin/env python3
"""
Example usage of the RecipeRepository class.
"""

import json
import os
from lib.recipe_repository import RecipeRepository


def create_sample_json():
    """Create a sample JSON file for demonstration."""
    sample_data = [
        {
            "name": "Add Spring JDBC",
            "description": "Add spring-boot-starter-jdbc",
            "package": "org.openrewrite.java.spring",
            "dependency": "org.springframework.boot:spring-boot-starter-jdbc",
            "mvn-command-line": "mvn -U -P rewrite ...",
            "category": "spring",
            "sub-category": "jdbc",
            "id": "org.openrewrite.java.spring.AddSpringJdbc",
            "tags": ["spring", "jdbc", "database"],
            "link": "https://docs.openrewrite.org/..."
        },
        {
            "name": "Add Spring Web",
            "description": "Add spring-boot-starter-web",
            "package": "org.openrewrite.java.spring",
            "dependency": "org.springframework.boot:spring-boot-starter-web",
            "mvn-command-line": "mvn -U -P rewrite ...",
            "category": "spring",
            "sub-category": "web",
            "id": "org.openrewrite.java.spring.AddSpringWeb",
            "tags": ["spring", "web"],
            "link": "https://docs.openrewrite.org/..."
        },
        {
            "name": "Migrate to JUnit 5",
            "description": "Rewrite tests to use JUnit Jupiter",
            "package": "org.openrewrite.testing",
            "dependency": "org.junit.jupiter:junit-jupiter",
            "mvn-command-line": "mvn -U -P rewrite ...",
            "category": "testing",
            "sub-category": "junit",
            "id": "org.openrewrite.testing.JUnit5Migration",
            "tags": ["test", "junit", "migration"],
            "link": "https://docs.openrewrite.org/..."
        }
    ]

    json_file = "sample_recipes.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)

    return json_file


def main():
    """Demonstrate RecipeRepository usage."""
    # Create sample JSON file
    json_file = create_sample_json()

    try:
        # Create repository with JSON file path
        repo = RecipeRepository(json_file)

        print("=== Recipe Repository Demo ===\n")

        # Get all categories
        print("1. All Categories:")
        categories = repo.get_all_categories()
        print(json.dumps(categories, indent=2))
        print()

        # Get categories with subcategories
        print("2. Categories with Subcategories:")
        cat_with_sub = repo.get_categories_with_subcategories()
        print(json.dumps(cat_with_sub, indent=2))
        print()

        # Get subcategories for a specific category
        print("3. Subcategories for 'spring':")
        subcats = repo.get_subcategories_by_category("spring")
        print(json.dumps(subcats, indent=2))
        print()

        # Get recipes by category
        print("4. Recipes in 'spring' category:")
        recipes = repo.get_recipes_by_category("spring")
        for recipe in recipes:
            print(f"  - {recipe['name']} ({recipe['sub-category']})")
        print()

        # Get recipes by tag
        print("5. Recipes with 'jdbc' tag:")
        recipes = repo.get_recipes_by_tag("jdbc")
        for recipe in recipes:
            print(f"  - {recipe['name']}")
        print()

        # Search recipes by name
        print("6. Recipes containing 'Spring' in name:")
        recipes = repo.get_recipes_by_name("Spring")
        for recipe in recipes:
            print(f"  - {recipe['name']}")
        print()

        # Get recipe by ID
        print("7. Recipe by ID:")
        recipe = repo.get_recipe_by_id("org.openrewrite.java.spring.AddSpringJdbc")
        if recipe:
            print(f"  - Found: {recipe['name']}")
            print(f"  - Description: {recipe['description']}")
        else:
            print("  - Recipe not found")
        print()

        # Get recipes by dependency
        print("8. Recipes with 'spring-boot' dependency:")
        recipes = repo.get_recipes_by_dependency("spring-boot")
        for recipe in recipes:
            print(f"  - {recipe['name']} -> {recipe['dependency']}")
        print()

    finally:
        # Cleanup
        if os.path.exists(json_file):
            os.remove(json_file)


if __name__ == "__main__":
    main()
