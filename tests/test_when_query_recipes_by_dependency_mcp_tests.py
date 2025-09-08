import pytest
from unittest.mock import MagicMock
from lib.mcp_service import RecipeMcpService


class WhenQueryRecipesByDependencyFromMcpTests:
    @pytest.fixture
    def repo_mock(self):
        return MagicMock()

    @pytest.fixture
    def service(self, repo_mock):
        return RecipeMcpService(repo_mock)

    def test_that_partial_case_insensitive_dependency_returns_matches(self, service, repo_mock):
        sample_recipes = [
            {"name": "Recipe 1", "dependency": "org.springframework"},
            {"name": "Recipe 2", "dependency": "org.springframework.web"}
        ]
        repo_mock.get_recipes_by_dependency.return_value = sample_recipes

        result = service.get_recipes_by_dependency("springframework")

        assert isinstance(result, list), "Result should be a list"
        assert len(result) == 2, "Should return 2 matching recipes"
        assert result[0]["name"] == "Recipe 1", "First recipe name should match"
        assert result[1]["name"] == "Recipe 2", "Second recipe name should match"

    def test_that_nonexistent_dependency_returns_empty_list(self, service, repo_mock):
        repo_mock.get_recipes_by_dependency.return_value = []

        result = service.get_recipes_by_dependency("nonexistent")

        assert result == [], "Should return empty list for nonexistent dependency"

    def test_that_empty_dependency_returns_empty_list(self, service, repo_mock):
        result = service.get_recipes_by_dependency("")

        assert result == [], "Should return empty list for empty dependency"
        repo_mock.get_recipes_by_dependency.assert_not_called(), "Repository should not be called for empty input"

    def test_that_none_dependency_returns_empty_list(self, service, repo_mock):
        result = service.get_recipes_by_dependency(None)

        assert result == [], "Should return empty list for None dependency"
        repo_mock.get_recipes_by_dependency.assert_not_called(), "Repository should not be called for None input"

    def test_that_very_long_dependency_returns_empty_list(self, service, repo_mock):
        long_dependency = "x" * 10000
        repo_mock.get_recipes_by_dependency.return_value = []

        result = service.get_recipes_by_dependency(long_dependency)

        assert result == [], "Should return empty list for very long dependency"

    def test_that_repo_exception_returns_empty_list(self, service, repo_mock):
        repo_mock.get_recipes_by_dependency.side_effect = Exception("Database error")

        result = service.get_recipes_by_dependency("springframework")

        assert result == [], "Should return empty list when repository throws exception"
