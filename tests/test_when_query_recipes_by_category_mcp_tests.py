import pytest
from unittest.mock import MagicMock
from lib.mcp_service import RecipeMcpService


class WhenQueryRecipesByCategoryFromMcpTests:
    @pytest.fixture
    def repo_mock(self):
        return MagicMock()

    @pytest.fixture
    def service(self, repo_mock):
        return RecipeMcpService(repo_mock)

    def test_that_category_without_subcategory_returns_recipes_list(self, service, repo_mock):
        sample_recipes = [
            {"name": "Recipe 1", "category": "java"},
            {"name": "Recipe 2", "category": "java"}
        ]
        repo_mock.get_recipes_by_category.return_value = sample_recipes

        result = service.get_recipes_by_category("java")

        assert isinstance(result, list), "Result should be a list"
        assert len(result) == 2, "Should return 2 matching recipes"
        assert result[0]["name"] == "Recipe 1", "First recipe name should match"
        assert result[1]["name"] == "Recipe 2", "Second recipe name should match"

    def test_that_category_with_subcategory_returns_recipes_list(self, service, repo_mock):
        sample_recipes = [{"name": "Recipe 1", "category": "java", "sub-category": "spring"}]
        repo_mock.get_recipes_by_category.return_value = sample_recipes

        result = service.get_recipes_by_category("java", "spring")

        assert isinstance(result, list), "Result should be a list"
        assert len(result) == 1, "Should return 1 matching recipe"
        assert result[0]["name"] == "Recipe 1", "Recipe name should match"

    def test_that_nonexistent_category_returns_empty_list(self, service, repo_mock):
        repo_mock.get_recipes_by_category.return_value = []

        result = service.get_recipes_by_category("nonexistent")

        assert result == [], "Should return empty list for nonexistent category"

    def test_that_empty_category_returns_empty_list(self, service, repo_mock):
        result = service.get_recipes_by_category("")

        assert result == [], "Should return empty list for empty category"
        repo_mock.get_recipes_by_category.assert_not_called(), "Repository should not be called for empty input"

    def test_that_none_category_returns_empty_list(self, service, repo_mock):
        result = service.get_recipes_by_category(None)

        assert result == [], "Should return empty list for None category"
        repo_mock.get_recipes_by_category.assert_not_called(), "Repository should not be called for None input"

    def test_that_subcategory_filtering_is_case_insensitive(self, service, repo_mock):
        sample_recipes = [{"name": "Recipe 1", "category": "JAVA", "sub-category": "SPRING"}]
        repo_mock.get_recipes_by_category.return_value = sample_recipes

        result = service.get_recipes_by_category("java", "spring")

        assert len(result) == 1, "Should return 1 matching recipe with case insensitive filtering"

    def test_that_repo_exception_returns_empty_list(self, service, repo_mock):
        repo_mock.get_recipes_by_category.side_effect = Exception("Database error")

        result = service.get_recipes_by_category("java")

        assert result == [], "Should return empty list when repository throws exception"
