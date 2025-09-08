import pytest
from unittest.mock import MagicMock
from lib.mcp_service import RecipeMcpService


class WhenQueryRecipesByTagFromMcpTests:
    @pytest.fixture
    def repo_mock(self):
        return MagicMock()

    @pytest.fixture
    def service(self, repo_mock):
        return RecipeMcpService(repo_mock)

    def test_that_existing_tag_returns_recipes_list(self, service, repo_mock):
        sample_recipes = [{"name": "Add Spring JDBC", "tags": ["spring", "jdbc"]}]
        repo_mock.get_recipes_by_tag.return_value = sample_recipes

        result = service.get_recipes_by_tag("spring")

        assert isinstance(result, list), "Result should be a list"
        assert len(result) == 1, "Should return 1 matching recipe"
        assert result[0]["name"] == "Add Spring JDBC", "Recipe name should match"
        assert "spring" in result[0]["tags"], "Recipe should contain the tag"

    def test_that_nonexistent_tag_returns_empty_list(self, service, repo_mock):
        repo_mock.get_recipes_by_tag.return_value = []

        result = service.get_recipes_by_tag("nonexistent")

        assert result == [], "Should return empty list for nonexistent tag"

    def test_that_empty_string_returns_empty_list(self, service, repo_mock):
        result = service.get_recipes_by_tag("")

        assert result == [], "Should return empty list for empty string"
        repo_mock.get_recipes_by_tag.assert_not_called(), "Repository should not be called for empty input"

    def test_that_none_tag_returns_empty_list(self, service, repo_mock):
        result = service.get_recipes_by_tag(None)

        assert result == [], "Should return empty list for None input"
        repo_mock.get_recipes_by_tag.assert_not_called(), "Repository should not be called for None input"

    def test_that_very_long_tag_returns_empty_list(self, service, repo_mock):
        long_tag = "x" * 10000
        repo_mock.get_recipes_by_tag.return_value = []

        result = service.get_recipes_by_tag(long_tag)

        assert result == [], "Should return empty list for very long tag"

    def test_that_repo_exception_returns_empty_list(self, service, repo_mock):
        repo_mock.get_recipes_by_tag.side_effect = Exception("Database error")

        result = service.get_recipes_by_tag("spring")

        assert result == [], "Should return empty list when repository throws exception"
