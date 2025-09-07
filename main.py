#!/usr/bin/env python3
"""
OpenRewrite Recipe Extractor - Main Application

This application extracts OpenRewrite recipes from HTML documentation
and generates a structured JSON database.
"""

import sys
from lib.recipe_extractor import RecipeExtractor


class RecipeExtractorApp:
    """Main application class for recipe extraction."""

    def __init__(self):
        """Initialize the application with default settings."""
        self.extractor = RecipeExtractor()

    def run(self) -> int:
        """
        Run the recipe extraction process.

        Returns:
            int: Exit code (0 for success, 1 for failure)
        """
        try:
            print("OpenRewrite Recipe Extractor")
            print("=" * 40)

            recipes = self.extractor.extract_recipes()

            if not recipes:
                print("No recipes were extracted. Please check your documentation files.")
                return 1

            print(f"\nSuccessfully extracted {len(recipes)} recipes!")
            return 0

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return 1
        except Exception as e:
            print(f"An error occurred: {e}")
            return 1

    def get_recipe_count(self) -> int:
        """Get the number of extracted recipes."""
        return len(self.extractor.recipes)

    def get_categories(self) -> dict:
        """Get the category counts."""
        return self.extractor.category_counts


def main() -> int:
    """Main entry point for the application."""
    app = RecipeExtractorApp()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
