import json
import pytest
from unittest.mock import patch, MagicMock
import main


class WhenUserChoosesQueriesMenuTests:
    def test_that_main_should_not_prompt_for_json_path_and_use_fixed_resource_path_test(self, monkeypatch):
        inputs = iter(['2', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance

            main.main()

            # Verifica que RecipeRepository foi chamado com o path fixo
            mock_repo.assert_called_once_with('resource/db/recipes.json')

    def test_that_queries_menu_should_list_available_options_and_accept_selection_test(self, capsys, monkeypatch):
        inputs = iter(['2', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository'):
            main.main()

        captured = capsys.readouterr()
        assert "Queries Menu" in captured.out
        assert "[1] List all categories" in captured.out
        assert "[2] List categories with subcategories" in captured.out
        assert "[3] Get subcategories by category" in captured.out
        assert "[4] Get recipes by category" in captured.out
        assert "[5] Get recipes by tag" in captured.out
        assert "[6] Get recipes by name" in captured.out
        assert "[7] Get recipe by ID" in captured.out
        assert "[8] Get recipes by dependency" in captured.out
        assert "[0] Back to main menu" in captured.out
