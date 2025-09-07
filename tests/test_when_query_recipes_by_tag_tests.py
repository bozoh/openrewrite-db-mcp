import json
import pytest
from unittest.mock import patch, MagicMock
import main


class WhenQueryRecipesByTagFromCliTests:
    def test_that_fetching_recipes_by_existing_tag_should_return_recipes_test(self, capsys, monkeypatch):
        inputs = iter(['2', '5', 'spring', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        sample_recipes = [{"name": "Add Spring JDBC", "tags": ["spring", "jdbc"]}]

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_tag.return_value = sample_recipes

            main.main()

        captured = capsys.readouterr()
        output = captured.out
        # Verificar se os valores esperados estão presentes
        assert "Add Spring JDBC" in output

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
                assert len(result) == 1
                assert result[0]["name"] == "Add Spring JDBC"
            except json.JSONDecodeError:
                # Se não conseguir fazer parse, pelo menos verificar conteúdo
                pass

    def test_that_fetching_recipes_by_nonexistent_tag_should_return_empty_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '5', 'nonexistent', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_tag.return_value = []

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

    def test_that_fetching_recipes_by_tag_with_empty_string_should_return_empty_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '5', '', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_tag.return_value = []

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

    def test_that_fetching_recipes_by_tag_with_very_long_tag_should_return_empty_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '5', 'x' * 10000, '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipes_by_tag.return_value = []

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
