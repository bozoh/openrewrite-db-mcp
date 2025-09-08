import json
import pytest
from unittest.mock import patch, MagicMock
import main


@pytest.fixture
def mock_extractor():
    with patch('main.RecipeExtractorApp') as mock_app:
        mock_instance = MagicMock()
        mock_app.return_value = mock_instance
        mock_instance.run.return_value = 0
        yield mock_instance


class WhenUserChoosesExtractionTests:
    def test_that_main_menu_should_offer_extraction_and_queries_options_test(self, capsys, monkeypatch):
        inputs = iter(['1'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeExtractorApp'):
            main.main()

        captured = capsys.readouterr()
        assert "OpenRewrite Recipe Extractor" in captured.out
        assert "[1] Extract recipes" in captured.out
        assert "[2] Query recipes" in captured.out

    def test_that_choosing_extraction_should_call_recipe_extractor_and_return_success_code_test(self, mock_extractor, capsys, monkeypatch):
        inputs = iter(['1'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        result = main.main()

        assert result == 0
        mock_extractor.run.assert_called_once()

    def test_that_extraction_with_failure_should_return_failure_code_test(self, monkeypatch):
        inputs = iter(['1'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeExtractorApp') as mock_app:
            mock_instance = MagicMock()
            mock_app.return_value = mock_instance
            mock_instance.run.return_value = 1

            result = main.main()

        assert result == 1

    def test_that_extraction_should_handle_keyboard_interrupt_and_return_failure_test(self, capsys, monkeypatch):
        inputs = iter(['1'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeExtractorApp') as mock_app:
            mock_instance = MagicMock()
            mock_app.return_value = mock_instance
            mock_instance.run.side_effect = KeyboardInterrupt()

            result = main.main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Operation cancelled by user" in captured.out

    def test_that_extraction_should_handle_generic_exception_and_return_failure_test(self, capsys, monkeypatch):
        inputs = iter(['1'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        with patch('main.RecipeExtractorApp') as mock_app:
            mock_instance = MagicMock()
            mock_app.return_value = mock_instance
            mock_instance.run.side_effect = Exception("Test error")

            result = main.main()

        assert result == 1
        captured = capsys.readouterr()
        assert "Unexpected error: Test error" in captured.out
