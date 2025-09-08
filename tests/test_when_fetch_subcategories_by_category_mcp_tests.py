import pytest
from unittest.mock import MagicMock
from lib.mcp_service import RecipeMcpService


class WhenFetchSubcategoriesByCategoryFromMcpTests:
    @pytest.fixture
    def repo_mock(self):
        return MagicMock()

    @pytest.fixture
    def service(self, repo_mock):
        return RecipeMcpService(repo_mock)

    def test_that_valid_category_returns_sorted_unique_subcategories(self, service, repo_mock):
        sample_subcategories = ["spring", "hibernate", "jpa"]
        repo_mock.get_subcategories_by_category.return_value = sample_subcategories

        result = service.get_subcategories_by_category("java")

        assert isinstance(result, list), "Result should be a list"
        assert len(result) == 3, "Should return 3 subcategories"
        assert result == ["spring", "hibernate", "jpa"], "Subcategories should be sorted and unique"

    def test_that_nonexistent_category_returns_empty_list(self, service, repo_mock):
        repo_mock.get_subcategories_by_category.return_value = []

        result = service.get_subcategories_by_category("nonexistent")

        assert result == [], "Should return empty list for nonexistent category"

    def test_that_empty_category_returns_empty_list(self, service, repo_mock):
        result = service.get_subcategories_by_category("")

        assert result == [], "Should return empty list for empty category"
        repo_mock.get_subcategories_by_category.assert_not_called(), "Repository should not be called for empty input"

    def test_that_none_category_returns_empty_list(self, service, repo_mock):
        result = service.get_subcategories_by_category(None)

        assert result == [], "Should return empty list for None category"
        repo_mock.get_subcategories_by_category.assert_not_called(), "Repository should not be called for None input"

    def test_that_repo_exception_returns_empty_list(self, service, repo_mock):
        repo_mock.get_subcategories_by_category.side_effect = Exception("Database error")

        result = service.get_subcategories_by_category("java")

        assert result == [], "Should return empty list when repository throws exception"
