import json
import pytest
from unittest.mock import patch, MagicMock
import main


class WhenQueryRecipesByNameFromCliTests:
    def test_that_partial_case_insensitive_name_search_should_return_matching_recipes_test(self, capsys, monkeypatch):
        inputs = iter(['2', '6', 'spring', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        sample_recipes = [
            {"name": "Add Spring JDBC"},
            {"name": "Add Spring Web"}
        ]

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_name.return_value = sample_recipes

            main.main()

        captured = capsys.readouterr()
        lines = captured.out.split('\n')
        json_line = None
        for line in lines:
            if line.strip().startswith('[') and '"name"' in line:
                json_line = line.strip()
                break

        assert json_line is not None
        result = json.loads(json_line)
        assert len(result) == 2

    def test_that_name_search_with_nonexistent_term_should_return_empty_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '6', 'nonexistent', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_name.return_value = []

            main.main()

        captured = capsys.readouterr()
        lines = captured.out.split('\n')
        json_line = None
        for line in lines:
            if line.strip() == '[]':
                json_line = line.strip()
                break

        assert json_line is not None
        result = json.loads(json_line)
        assert result == []

    def test_that_name_search_with_empty_string_should_return_empty_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '6', '', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_name.return_value = []

            main.main()

        captured = capsys.readouterr()
        lines = captured.out.split('\n')
        json_line = None
        for line in lines:
            if line.strip() == '[]':
                json_line = line.strip()
                break

        assert json_line is not None
        result = json.loads(json_line)
        assert result == []

    def test_that_name_search_with_very_long_query_should_return_empty_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '6', 'x' * 10000, '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_name.return_value = []

            main.main()

        captured = capsys.readouterr()
        lines = captured.out.split('\n')
        json_line = None
        for line in lines:
            if line.strip() == '[]':
                json_line = line.strip()
                break

        assert json_line is not None
        result = json.loads(json_line)
        assert result == []
