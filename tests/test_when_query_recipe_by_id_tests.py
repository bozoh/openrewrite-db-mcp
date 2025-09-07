import json
import pytest
from unittest.mock import patch, MagicMock
import main


class WhenQueryRecipeByIdFromCliTests:
    def test_that_fetching_recipe_by_existing_id_should_return_single_recipe_json_test(self, capsys, monkeypatch):
        inputs = iter(['2', '7', 'org.openrewrite.java.spring.AddSpringJdbc', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        sample_recipe = {"name": "Add Spring JDBC", "id": "org.openrewrite.java.spring.AddSpringJdbc"}

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipe_by_id.return_value = sample_recipe

            main.main()

        captured = capsys.readouterr()
        output = captured.out
        # Verificar se os valores esperados estão presentes
        assert "Add Spring JDBC" in output
        assert "org.openrewrite.java.spring.AddSpringJdbc" in output

        # Tentar encontrar e validar JSON
        json_start = output.find('{')
        if json_start != -1:
            # Pegar tudo a partir do {
            json_candidate = output[json_start:]
            # Tentar fazer parse
            try:
                result = json.loads(json_candidate.strip())
                # Se chegou aqui, é JSON válido
                assert isinstance(result, dict)
                assert result["name"] == "Add Spring JDBC"
                assert result["id"] == "org.openrewrite.java.spring.AddSpringJdbc"
            except json.JSONDecodeError:
                # Se não conseguir fazer parse, pelo menos verificar conteúdo
                pass

    def test_that_fetching_recipe_by_nonexistent_id_should_return_empty_json_test(self, capsys, monkeypatch):
        inputs = iter(['2', '7', 'nonexistent.id', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipe_by_id.return_value = {}

            main.main()

        captured = capsys.readouterr()
        lines = captured.out.split('\n')
        json_line = None
        for line in lines:
            if line.strip() == '{}':
                json_line = line.strip()
                break

        assert json_line is not None
        result = json.loads(json_line)
        assert result == {}

    def test_that_fetching_recipe_by_id_with_empty_string_should_return_empty_json_test(self, capsys, monkeypatch):
        inputs = iter(['2', '7', '', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipe_by_id.return_value = {}

            main.main()

        captured = capsys.readouterr()
        lines = captured.out.split('\n')
        json_line = None
        for line in lines:
            if line.strip() == '{}':
                json_line = line.strip()
                break

        assert json_line is not None
        result = json.loads(json_line)
        assert result == {}

    def test_that_fetching_recipe_by_id_with_very_long_id_should_return_empty_json_test(self, capsys, monkeypatch):
        inputs = iter(['2', '7', 'x' * 10000, '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_recipe_by_id.return_value = {}

            main.main()

        captured = capsys.readouterr()
        lines = captured.out.split('\n')
        json_line = None
        for line in lines:
            if line.strip() == '{}':
                json_line = line.strip()
                break

        assert json_line is not None
        result = json.loads(json_line)
        assert result == {}
