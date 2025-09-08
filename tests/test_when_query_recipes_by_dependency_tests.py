import json
import pytest
from unittest.mock import patch, MagicMock
import main


class WhenQueryRecipesByDependencyFromCliTests:
    def test_that_fetching_recipes_by_existing_dependency_should_return_recipes_test(self, capsys, monkeypatch):
        inputs = iter(['2', '8', 'spring-boot-starter-jdbc', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        sample_recipes = [{"name": "Add Spring JDBC", "dependency": "org.springframework.boot:spring-boot-starter-jdbc"}]

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_dependency.return_value = sample_recipes

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
        assert len(result) == 1
        assert result[0]["name"] == "Add Spring JDBC"

    def test_that_fetching_recipes_by_dependency_partial_should_match_test(self, capsys, monkeypatch):
        inputs = iter(['2', '8', 'jdbc', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        sample_recipes = [{"name": "Add Spring JDBC", "dependency": "org.springframework.boot:spring-boot-starter-jdbc"}]

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_dependency.return_value = sample_recipes

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
        assert len(result) == 1

    def test_that_fetching_recipes_by_nonexistent_dependency_should_return_empty_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '8', 'nonexistent', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_dependency.return_value = []

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

    def test_that_fetching_recipes_by_dependency_with_empty_string_should_return_empty_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '8', '', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_dependency.return_value = []

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

    def test_that_fetching_recipes_by_dependency_with_very_long_dependency_should_return_empty_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '8', 'x' * 10000, '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_dependency.return_value = []

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
