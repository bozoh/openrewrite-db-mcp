#!/usr/bin/env python3
"""
OpenRewrite Recipe Extractor - Main Application

This application extracts OpenRewrite recipes from HTML documentation
and generates a structured JSON database, or allows querying existing recipes.
"""

import sys
import json
from lib.recipe_extractor import RecipeExtractor
from lib.recipe_repository import RecipeRepository


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


def show_main_menu():
    """Display the main menu options."""
    print("\nOpenRewrite Recipe Extractor")
    print("=" * 40)
    print("[1] Extract recipes")
    print("[2] Query recipes")
    print("[0] Exit")
    print()


def show_queries_menu():
    """Display the queries menu options."""
    print("\nQueries Menu")
    print("=" * 20)
    print("[1] List all categories")
    print("[2] List categories with subcategories")
    print("[3] Get subcategories by category")
    print("[4] Get recipes by category")
    print("[5] Get recipes by tag")
    print("[6] Get recipes by name")
    print("[7] Get recipe by ID")
    print("[8] Get recipes by dependency")
    print("[0] Back to main menu")
    print()


def handle_queries():
    """Handle the queries menu."""
    repo = RecipeRepository('resource/db/recipes.json')

    while True:
        show_queries_menu()
        try:
            choice = input("Choose an option: ").strip()

            if choice == '0':
                print("Returning to main menu...")
                break
            elif choice == '1':
                # Listar todas as categorias
                try:
                    result = repo.get_all_categories()
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Error executing query: {e}")
            elif choice == '2':
                # Listar categorias com subcategorias
                try:
                    result = repo.get_categories_with_subcategories()
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Error executing query: {e}")
            elif choice == '3':
                # Get subcategories by category
                category = input("Enter category: ").strip()
                try:
                    result = repo.get_subcategories_by_category(category)
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Error executing query: {e}")
            elif choice == '4':
                # Get recipes by category
                category = input("Enter category: ").strip()
                subcategory = input("Enter subcategory (or leave empty): ").strip()
                subcategory = subcategory if subcategory else None
                try:
                    result = repo.get_recipes_by_category(category, subcategory)
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Error executing query: {e}")
            elif choice == '5':
                # Get recipes by tag
                tag = input("Enter tag: ").strip()
                try:
                    result = repo.get_recipes_by_tag(tag)
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Error executing query: {e}")
            elif choice == '6':
                # Get recipes by name
                name = input("Enter name (partial): ").strip()
                try:
                    result = repo.get_recipes_by_name(name)
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Error executing query: {e}")
            elif choice == '7':
                # Get recipe by ID
                recipe_id = input("Enter recipe ID: ").strip()
                try:
                    result = repo.get_recipe_by_id(recipe_id)
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Error executing query: {e}")
            elif choice == '8':
                # Get recipes by dependency
                dependency = input("Enter dependency (partial): ").strip()
                try:
                    result = repo.get_recipes_by_dependency(dependency)
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Error executing query: {e}")
            else:
                print("Invalid option. Please try again.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break
        except EOFError:
            print("\nInput terminated.")
            break


def main() -> int:
    """Main entry point for the application."""
    while True:
        show_main_menu()
        try:
            choice = input("Choose an option: ").strip()

            if choice == '0':
                print("Exiting...")
                return 0
            elif choice == '1':
                # Extract recipes
                app = RecipeExtractorApp()
                result = app.run()
                if isinstance(result, int):
                    return result
                else:
                    return 0
            elif choice == '2':
                # Query recipes
                handle_queries()
            else:
                print("Invalid option. Please try again.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return 1
        except EOFError:
            print("\nInput terminated.")
            return 0
        except StopIteration:
            return 0
        except Exception as e:
            print(f"Unexpected error: {e}")
            return 1


if __name__ == "__main__":
    sys.exit(main())
