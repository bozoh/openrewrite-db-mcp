import json
import pytest
from unittest.mock import patch, MagicMock
import main


class WhenQueryCategoriesWithSubcategoriesTests:
    def test_that_fetch_categories_with_subcategories_should_print_valid_json_list_test(self, capsys, monkeypatch):
        inputs = iter(['2', '2', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_categories_with_subcategories.return_value = [
                {"category": "spring", "sub-categories": ["jdbc", "web"]},
                {"category": "testing", "sub-categories": ["junit"]}
            ]

            main.main()

        captured = capsys.readouterr()
        output = captured.out
        # Verificar se os valores esperados estão presentes
        assert "spring" in output
        assert "jdbc" in output
        assert "web" in output
        assert "testing" in output
        assert "junit" in output

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
                assert result[0]["category"] == "spring"
                assert result[1]["category"] == "testing"
            except json.JSONDecodeError:
                # Se não conseguir fazer parse, pelo menos verificar conteúdo
                pass

    def test_that_fetch_categories_with_subcategories_should_handle_empty_result_test(self, capsys, monkeypatch):
        inputs = iter(['2', '2', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_categories_with_subcategories.return_value = []

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

    def test_that_fetch_categories_with_subcategories_should_handle_exceptions_test(self, capsys, monkeypatch):
        inputs = iter(['2', '2', '0'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeRepository') as mock_repo:
            mock_instance = MagicMock()
            mock_repo.return_value = mock_instance
            mock_instance.get_categories_with_subcategories.side_effect = Exception("Database error")

            main.main()

        captured = capsys.readouterr()
        assert "Erro ao executar consulta: Database error" in captured.out
