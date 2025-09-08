import pytest
from unittest.mock import MagicMock
from lib.mcp_service import RecipeMcpService


class WhenFetchCategoriesWithSubcategoriesFromMcpTests:
    @pytest.fixture
    def repo_mock(self):
        return MagicMock()

    @pytest.fixture
    def service(self, repo_mock):
        return RecipeMcpService(repo_mock)

    def test_that_returns_list_of_objects_with_category_and_subcategories(self, service, repo_mock):
        sample_categories = [
            {"category": "java", "sub-categories": ["spring", "hibernate"]},
            {"category": "kotlin", "sub-categories": ["android", "jvm"]}
        ]
        repo_mock.get_categories_with_subcategories.return_value = sample_categories

        result = service.get_categories_with_subcategories()

        assert isinstance(result, list), "Result should be a list"
        assert len(result) == 2, "Should return 2 category objects"
        assert result[0]["category"] == "java", "First category should match"
        assert result[0]["sub-categories"] == ["spring", "hibernate"], "First subcategories should match"
        assert result[1]["category"] == "kotlin", "Second category should match"
        assert result[1]["sub-categories"] == ["android", "jvm"], "Second subcategories should match"

    def test_that_repo_exception_returns_empty_list(self, service, repo_mock):
        repo_mock.get_categories_with_subcategories.side_effect = Exception("Database error")

        result = service.get_categories_with_subcategories()

        assert result == [], "Should return empty list when repository throws exception"
