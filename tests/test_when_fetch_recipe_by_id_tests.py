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


class WhenFetchRecipeByIdTests:
    def test_that_fetching_recipe_by_existing_id_should_return_single_recipe_json_test(self, repo):
        result = repo.get_recipe_by_id("org.openrewrite.java.spring.AddSpringJdbc")
        assert isinstance(result, dict)
        assert json.dumps(result)  # serializable
        assert result["name"] == "Add Spring JDBC"
        assert result["id"] == "org.openrewrite.java.spring.AddSpringJdbc"

    def test_that_fetching_recipe_by_nonexistent_id_should_return_empty_json_test(self, repo):
        result = repo.get_recipe_by_id("nonexistent.id")
        assert result == {}

    def test_that_fetching_recipe_by_id_with_none_should_return_empty_json_test(self, repo):
        result = repo.get_recipe_by_id(None)
        assert result == {}

    def test_that_fetching_recipe_by_id_with_empty_string_should_return_empty_json_test(self, repo):
        result = repo.get_recipe_by_id("")
        assert result == {}

    def test_that_fetching_recipe_by_id_with_wrong_type_should_return_empty_json_test(self, repo):
        result = repo.get_recipe_by_id(123)
        assert result == {}

    def test_that_fetching_recipe_by_id_should_be_case_sensitive_test(self, repo):
        result = repo.get_recipe_by_id("ORG.OPENREWRITE.JAVA.SPRING.ADDSPRINGJDBC")
        assert result == {}  # Should not find due to case sensitivity

    def test_that_fetching_recipe_by_id_should_return_complete_recipe_object_test(self, repo):
        result = repo.get_recipe_by_id("org.openrewrite.java.spring.AddSpringJdbc")
        assert "id" in result
        assert "name" in result
        assert "category" in result
        assert "sub-category" in result
        assert "tags" in result
        assert "link" in result
        assert "description" in result
        assert "package" in result
        assert "dependency" in result
        assert "mvn-command-line" in result

    def test_that_fetching_recipe_by_id_should_handle_recipes_without_id_test(self):
        data = [
            {"name": "Recipe 1", "id": "recipe1"},
            {"name": "Recipe 2"}  # no id
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)
        result = repo.get_recipe_by_id("recipe1")
        assert result["name"] == "Recipe 1"

    def test_that_fetching_recipe_by_id_should_handle_non_string_ids_test(self):
        data = [
            {"name": "Recipe 1", "id": "recipe1"},
            {"name": "Recipe 2", "id": 123}  # non-string id
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)
        result = repo.get_recipe_by_id("recipe1")
        assert result["name"] == "Recipe 1"

    def test_that_fetching_recipe_by_id_with_very_long_id_should_return_empty_json_test(self, repo):
        result = repo.get_recipe_by_id("x" * 10000)
        assert result == {}

    def test_that_fetching_recipe_by_id_should_return_first_match_test(self):
        data = [
            {"name": "Recipe 1", "id": "duplicate"},
            {"name": "Recipe 2", "id": "duplicate"}  # duplicate id
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)
        result = repo.get_recipe_by_id("duplicate")
        assert result["name"] == "Recipe 1"  # Should return first match
