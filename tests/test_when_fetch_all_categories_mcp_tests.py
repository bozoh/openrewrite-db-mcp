import pytest
from unittest.mock import MagicMock
from lib.mcp_service import RecipeMcpService


class WhenFetchAllCategoriesFromMcpTests:
    @pytest.fixture
    def repo_mock(self):
        return MagicMock()

    @pytest.fixture
    def service(self, repo_mock):
        return RecipeMcpService(repo_mock)

    def test_that_returns_sorted_unique_categories_list(self, service, repo_mock):
        sample_categories = ["java", "kotlin", "groovy"]
        repo_mock.get_all_categories.return_value = sample_categories

        result = service.get_all_categories()

        assert isinstance(result, list), "Result should be a list"
        assert len(result) == 3, "Should return 3 categories"
        assert result == ["java", "kotlin", "groovy"], "Categories should be sorted and unique"

    def test_that_repo_exception_returns_empty_list(self, service, repo_mock):
        repo_mock.get_all_categories.side_effect = Exception("Database error")

        result = service.get_all_categories()

        assert result == [], "Should return empty list when repository throws exception"
