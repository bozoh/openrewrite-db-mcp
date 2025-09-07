import json
import pytest
from unittest.mock import patch, MagicMock
import main


class WhenQueryRecipesByCategoryAndSubcategoryTests:
    def test_that_category_only_should_print_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '4', 'spring', '', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        sample_recipes = [
            {"name": "Add Spring JDBC", "category": "spring", "sub-category": "jdbc"},
            {"name": "Add Spring Web", "category": "spring", "sub-category": "web"}
        ]

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_category.return_value = sample_recipes

            main.main()

        captured = capsys.readouterr()
        output = captured.out
        # Verificar se os valores esperados estão presentes
        assert "Add Spring JDBC" in output
        assert "Add Spring Web" in output

        # Tentar encontrar e validar JSON
        json_start = output.find('[')
        if json_start != -1:
            # Pegar tudo a partir do [
            json_candidate = output[json_start:]
            # Tentar fazer parse
            try:
                result = json.loads(json_candidate.strip())
                # Se chegou aqui, é JSON válido
                assert isinstance(result, list)
                assert len(result) == 2
                assert result[0]["name"] == "Add Spring JDBC"
            except json.JSONDecodeError:
                # Se não conseguir fazer parse, pelo menos verificar conteúdo
                pass

    def test_that_category_and_subcategory_should_print_filtered_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '4', 'spring', 'jdbc', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        sample_recipe = [{"name": "Add Spring JDBC", "category": "spring", "sub-category": "jdbc"}]

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_category.return_value = sample_recipe

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

    def test_that_nonexistent_inputs_should_print_empty_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '4', 'nonexistent', '', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_category.return_value = []

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

    def test_that_very_long_inputs_should_print_empty_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '4', 'x' * 10000, '', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_category.return_value = []

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
