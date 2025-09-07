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
        assert "Menu de Consultas" in captured.out
        assert "[1] Listar todas as categorias" in captured.out
        assert "[2] Listar categorias com subcategorias" in captured.out
        assert "[3] Buscar subcategorias por categoria" in captured.out
        assert "[4] Buscar receitas por categoria" in captured.out
        assert "[5] Buscar receitas por tag" in captured.out
        assert "[6] Buscar receitas por nome" in captured.out
        assert "[7] Buscar receita por ID" in captured.out
        assert "[8] Buscar receitas por dependencia" in captured.out
        assert "[0] Voltar ao menu principal" in captured.out
