import json
import pytest
from unittest.mock import patch, MagicMock
import main


class WhenQuerySubcategoriesByCategoryTests:
    def test_that_prompt_for_category_then_print_valid_json_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '3', 'spring', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_subcategories_by_category.return_value = ["jdbc", "web"]

            main.main()

        captured = capsys.readouterr()
        lines = captured.out.split('\n')
        json_line = None
        for line in lines:
            if line.strip().startswith('[') and 'jdbc' in line:
                json_line = line.strip()
                break

        assert json_line is not None
        result = json.loads(json_line)
        assert result == ["jdbc", "web"]

    def test_that_empty_or_none_category_input_should_result_in_empty_list_and_message_test(self, capsys, monkeypatch):
        inputs = iter(['2', '3', '', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_subcategories_by_category.return_value = []

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

    def test_that_errors_should_be_handled_test(self, capsys, monkeypatch):
        inputs = iter(['2', '3', 'spring', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_subcategories_by_category.side_effect = Exception("Database error")

            main.main()

        captured = capsys.readouterr()
        assert "Erro ao executar consulta: Database error" in captured.out
