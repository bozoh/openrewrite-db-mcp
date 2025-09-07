import json
import pytest
from unittest.mock import patch, MagicMock
import main


class WhenCliInputValidationAndNavigationTests:
    def test_that_invalid_main_menu_option_should_print_error_and_reprompt_test(self, capsys, monkeypatch):
        inputs = iter(['x', '3', '1'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeExtractorApp'):
            result = main.main()

        captured = capsys.readouterr()
        assert "Opção inválida" in captured.out
        assert result == 0  # Should continue to extraction

    def test_that_invalid_queries_menu_option_should_print_error_and_reprompt_test(self, capsys, monkeypatch):
        inputs = iter(['2', '99', '1', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository'):
            main.main()

        captured = capsys.readouterr()
        assert "Opção inválida" in captured.out

    def test_that_user_can_exit_queries_menu_and_then_program_test(self, capsys, monkeypatch):
        inputs = iter(['2', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository'):
            result = main.main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Voltando ao menu principal" in captured.out

    def test_that_all_query_responses_should_be_json_serializable_test(self, capsys, monkeypatch):
        # Test multiple queries to ensure all return valid JSON
        inputs = iter(['2', '1', '2', '3', 'spring', '4', 'spring', '', '5', 'spring', '6', 'spring', '7', 'test.id', '8', 'spring', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance

            # Mock all methods to return valid data
            mock_instance.get_all_categories.return_value = ["spring", "testing"]
            mock_instance.get_categories_with_subcategories.return_value = [{"category": "spring", "sub-categories": ["jdbc"]}]
            mock_instance.get_subcategories_by_category.return_value = ["jdbc", "web"]
            mock_instance.get_recipes_by_category.return_value = [{"name": "Test Recipe"}]
            mock_instance.get_recipes_by_tag.return_value = [{"name": "Tagged Recipe"}]
            mock_instance.get_recipes_by_name.return_value = [{"name": "Named Recipe"}]
            mock_instance.get_recipe_by_id.return_value = {"name": "ID Recipe"}
            mock_instance.get_recipes_by_dependency.return_value = [{"name": "Dependency Recipe"}]

            main.main()

        captured = capsys.readouterr()
        # Should not have any JSON parsing errors in the output
        # If there were errors, they would appear in stderr or as exceptions
        assert "Erro ao executar consulta" not in captured.out

    def test_that_main_menu_exit_works_correctly_test(self, capsys, monkeypatch):
        inputs = iter(['0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        result = main.main()

        assert result == 0
        captured = capsys.readouterr()
        assert "Saindo" in captured.out
