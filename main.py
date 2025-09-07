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
    print("[1] Extrair receitas")
    print("[2] Consultar receitas")
    print("[0] Sair")
    print()


def show_queries_menu():
    """Display the queries menu options."""
    print("\nMenu de Consultas")
    print("=" * 20)
    print("[1] Listar todas as categorias")
    print("[2] Listar categorias com subcategorias")
    print("[3] Buscar subcategorias por categoria")
    print("[4] Buscar receitas por categoria")
    print("[5] Buscar receitas por tag")
    print("[6] Buscar receitas por nome")
    print("[7] Buscar receita por ID")
    print("[8] Buscar receitas por dependencia")
    print("[0] Voltar ao menu principal")
    print()


def handle_queries():
    """Handle the queries menu."""
    repo = RecipeRepository('resource/db/recipes.json')

    while True:
        show_queries_menu()
        try:
            choice = input("Escolha uma opção: ").strip()

            if choice == '0':
                print("Voltando ao menu principal...")
                break
            elif choice == '1':
                # Listar todas as categorias
                try:
                    result = repo.get_all_categories()
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Erro ao executar consulta: {e}")
            elif choice == '2':
                # Listar categorias com subcategorias
                try:
                    result = repo.get_categories_with_subcategories()
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Erro ao executar consulta: {e}")
            elif choice == '3':
                # Buscar subcategorias por categoria
                category = input("Digite a categoria: ").strip()
                try:
                    result = repo.get_subcategories_by_category(category)
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Erro ao executar consulta: {e}")
            elif choice == '4':
                # Buscar receitas por categoria
                category = input("Digite a categoria: ").strip()
                subcategory = input("Digite a subcategoria (ou deixe vazio): ").strip()
                subcategory = subcategory if subcategory else None
                try:
                    result = repo.get_recipes_by_category(category, subcategory)
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Erro ao executar consulta: {e}")
            elif choice == '5':
                # Buscar receitas por tag
                tag = input("Digite a tag: ").strip()
                try:
                    result = repo.get_recipes_by_tag(tag)
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Erro ao executar consulta: {e}")
            elif choice == '6':
                # Buscar receitas por nome
                name = input("Digite o nome (parcial): ").strip()
                try:
                    result = repo.get_recipes_by_name(name)
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Erro ao executar consulta: {e}")
            elif choice == '7':
                # Buscar receita por ID
                recipe_id = input("Digite o ID da receita: ").strip()
                try:
                    result = repo.get_recipe_by_id(recipe_id)
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Erro ao executar consulta: {e}")
            elif choice == '8':
                # Buscar receitas por dependencia
                dependency = input("Digite a dependencia (parcial): ").strip()
                try:
                    result = repo.get_recipes_by_dependency(dependency)
                    print(json.dumps(result, ensure_ascii=False))
                except Exception as e:
                    print(f"Erro ao executar consulta: {e}")
            else:
                print("Opção inválida. Tente novamente.")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            break
        except EOFError:
            print("\nEntrada terminada.")
            break


def main() -> int:
    """Main entry point for the application."""
    while True:
        show_main_menu()
        try:
            choice = input("Escolha uma opção: ").strip()

            if choice == '0':
                print("Saindo...")
                return 0
            elif choice == '1':
                # Extrair receitas
                app = RecipeExtractorApp()
                result = app.run()
                if isinstance(result, int):
                    return result
                else:
                    return 0
            elif choice == '2':
                # Consultar receitas
                handle_queries()
            else:
                print("Opção inválida. Tente novamente.")
        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            return 1
        except EOFError:
            print("\nEntrada terminada.")
            return 0
        except StopIteration:
            return 0
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return 1


if __name__ == "__main__":
    sys.exit(main())
