import json
import pytest
from unittest.mock import Mock
from lib.recipe_repository import RecipeRepository


@pytest.fixture
def sample_data():
    return [
        {
            "name": "Add Spring JDBC",
            "description": "Add spring-boot-starter-jdbc",
            "package": "org.openrewrite.java.spring",
            "dependency": "org.springframework.boot:spring-boot-starter-jdbc",
            "mvn-command-line": "mvn -U -P rewrite ...",
            "category": "spring",
            "sub-category": "jdbc",
            "id": "org.openrewrite.java.spring.AddSpringJdbc",
            "tags": ["spring", "jdbc", "database"],
            "link": "https://docs.openrewrite.org/..."
        },
        {
            "name": "Add Spring Web",
            "description": "Add spring-boot-starter-web",
            "package": "org.openrewrite.java.spring",
            "dependency": "org.springframework.boot:spring-boot-starter-web",
            "mvn-command-line": "mvn -U -P rewrite ...",
            "category": "spring",
            "sub-category": "web",
            "id": "org.openrewrite.java.spring.AddSpringWeb",
            "tags": ["spring", "web"],
            "link": "https://docs.openrewrite.org/..."
        },
        {
            "name": "Migrate to JUnit 5",
            "description": "Rewrite tests to use JUnit Jupiter",
            "package": "org.openrewrite.testing",
            "dependency": "org.junit.jupiter:junit-jupiter",
            "mvn-command-line": "mvn -U -P rewrite ...",
            "category": "testing",
            "sub-category": "junit",
            "id": "org.openrewrite.testing.JUnit5Migration",
            "tags": ["test", "junit", "migration"],
            "link": "https://docs.openrewrite.org/..."
        }
    ]


@pytest.fixture
def repo(sample_data):
    loader = Mock(return_value=sample_data)
    return RecipeRepository(load_json_callable=loader)


class WhenFetchRecipesByCategoryAndSubcategoryTests:
    def test_that_fetching_recipes_by_existing_category_should_return_recipes_test(self, repo):
        result = repo.get_recipes_by_category("spring")
        assert isinstance(result, list)
        assert json.dumps(result)  # serializable
        assert len(result) == 2
        names = [r["name"] for r in result]
        assert "Add Spring JDBC" in names
        assert "Add Spring Web" in names

    def test_that_fetching_recipes_by_existing_category_and_subcategory_should_return_filtered_recipes_test(self, repo):
        result = repo.get_recipes_by_category("spring", "jdbc")
        assert isinstance(result, list)
        assert json.dumps(result)
        assert len(result) == 1
        assert result[0]["name"] == "Add Spring JDBC"

    def test_that_fetching_recipes_by_nonexistent_category_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_category("nonexistent")
        assert result == []

    def test_that_fetching_recipes_by_category_with_none_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_category(None)
        assert result == []

    def test_that_fetching_recipes_by_category_with_empty_string_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_category("")
        assert result == []

    def test_that_fetching_recipes_with_nonexistent_subcategory_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_category("spring", "nonexistent")
        assert result == []

    def test_that_fetching_recipes_with_none_subcategory_should_return_all_category_recipes_test(self, repo):
        result = repo.get_recipes_by_category("spring", None)
        assert len(result) == 2

    def test_that_fetching_recipes_with_empty_subcategory_should_return_all_category_recipes_test(self, repo):
        result = repo.get_recipes_by_category("spring", "")
        assert len(result) == 2

    def test_that_fetching_recipes_should_be_case_insensitive_for_category_and_subcategory_test(self, repo):
        result = repo.get_recipes_by_category("SPRING", "JDBC")
        assert len(result) == 1
        assert result[0]["name"] == "Add Spring JDBC"

    def test_that_fetching_recipes_with_very_long_category_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_category("x" * 10000)
        assert result == []

    def test_that_fetching_recipes_with_very_long_subcategory_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_category("spring", "x" * 10000)
        assert result == []

    def test_that_fetching_recipes_should_handle_wrong_types_test(self, repo):
        result = repo.get_recipes_by_category(123, 456)
        assert result == []

    def test_that_fetching_recipes_should_return_complete_recipe_objects_test(self, repo):
        result = repo.get_recipes_by_category("spring", "jdbc")
        assert len(result) == 1
        recipe = result[0]
        assert "id" in recipe
        assert "name" in recipe
        assert "category" in recipe
        assert "sub-category" in recipe
        assert "tags" in recipe
        assert "link" in recipe
