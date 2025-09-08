import pytest
from unittest.mock import MagicMock
from lib.mcp_service import RecipeMcpService


class WhenQueryRecipesByNameFromMcpTests:
    @pytest.fixture
    def repo_mock(self):
        return MagicMock()

    @pytest.fixture
    def service(self, repo_mock):
        return RecipeMcpService(repo_mock)

    def test_that_partial_case_insensitive_query_returns_matches(self, service, repo_mock):
        sample_recipes = [
            {"name": "Add Spring JDBC"},
            {"name": "Add Spring Web"}
        ]
        repo_mock.get_recipes_by_name.return_value = sample_recipes

        result = service.get_recipes_by_name("spring")

        assert isinstance(result, list), "Result should be a list"
        assert len(result) == 2, "Should return 2 matching recipes"
        assert result[0]["name"] == "Add Spring JDBC", "First recipe name should match"
        assert result[1]["name"] == "Add Spring Web", "Second recipe name should match"

    def test_that_nonexistent_term_returns_empty_list(self, service, repo_mock):
        repo_mock.get_recipes_by_name.return_value = []

        result = service.get_recipes_by_name("nonexistent")

        assert result == [], "Should return empty list for nonexistent term"

    def test_that_empty_string_returns_empty_list(self, service, repo_mock):
        result = service.get_recipes_by_name("")

        assert result == [], "Should return empty list for empty string"
        repo_mock.get_recipes_by_name.assert_not_called(), "Repository should not be called for empty input"

    def test_that_none_query_returns_empty_list(self, service, repo_mock):
        result = service.get_recipes_by_name(None)

        assert result == [], "Should return empty list for None input"
        repo_mock.get_recipes_by_name.assert_not_called(), "Repository should not be called for None input"

    def test_that_very_long_query_returns_empty_list(self, service, repo_mock):
        long_query = "x" * 10000
        repo_mock.get_recipes_by_name.return_value = []

        result = service.get_recipes_by_name(long_query)

        assert result == [], "Should return empty list for very long query"

    def test_that_repo_exception_returns_empty_list(self, service, repo_mock):
        repo_mock.get_recipes_by_name.side_effect = Exception("Database error")

        result = service.get_recipes_by_name("spring")

        assert result == [], "Should return empty list when repository throws exception"
