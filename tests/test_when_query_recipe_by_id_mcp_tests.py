import pytest
from unittest.mock import MagicMock
from lib.mcp_service import RecipeMcpService


class WhenQueryRecipeByIdFromMcpTests:
    @pytest.fixture
    def repo_mock(self):
        return MagicMock()

    @pytest.fixture
    def service(self, repo_mock):
        return RecipeMcpService(repo_mock)

    def test_that_existing_id_returns_recipe_dict(self, service, repo_mock):
        sample_recipe = {"name": "Add Spring JDBC", "id": "org.openrewrite.java.spring.AddSpringJdbc"}
        repo_mock.get_recipe_by_id.return_value = sample_recipe

        result = service.get_recipe_by_id("org.openrewrite.java.spring.AddSpringJdbc")

        assert isinstance(result, dict), "Result should be a dictionary"
        assert result["name"] == "Add Spring JDBC", "Recipe name should match"
        assert result["id"] == "org.openrewrite.java.spring.AddSpringJdbc", "Recipe ID should match"

    def test_that_nonexistent_id_returns_empty_dict(self, service, repo_mock):
        repo_mock.get_recipe_by_id.return_value = {}

        result = service.get_recipe_by_id("nonexistent.id")

        assert result == {}, "Should return empty dict for nonexistent ID"

    def test_that_empty_string_returns_empty_dict(self, service, repo_mock):
        result = service.get_recipe_by_id("")

        assert result == {}, "Should return empty dict for empty string"
        repo_mock.get_recipe_by_id.assert_not_called(), "Repository should not be called for empty input"

    def test_that_none_id_returns_empty_dict(self, service, repo_mock):
        result = service.get_recipe_by_id(None)

        assert result == {}, "Should return empty dict for None input"
        repo_mock.get_recipe_by_id.assert_not_called(), "Repository should not be called for None input"

    def test_that_very_long_id_returns_empty_dict(self, service, repo_mock):
        long_id = "x" * 10000
        repo_mock.get_recipe_by_id.return_value = {}

        result = service.get_recipe_by_id(long_id)

        assert result == {}, "Should return empty dict for very long ID"

    def test_that_repo_exception_returns_empty_dict(self, service, repo_mock):
        repo_mock.get_recipe_by_id.side_effect = Exception("Database error")

        result = service.get_recipe_by_id("some.id")

        assert result == {}, "Should return empty dict when repository throws exception"
