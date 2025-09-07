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


class WhenFetchRecipesByTagTests:
    def test_that_fetching_recipes_by_existing_tag_should_return_recipes_test(self, repo):
        result = repo.get_recipes_by_tag("jdbc")
        assert isinstance(result, list)
        assert json.dumps(result)  # serializable
        assert len(result) == 1
        assert result[0]["name"] == "Add Spring JDBC"

    def test_that_fetching_recipes_by_nonexistent_tag_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_tag("nonexistent")
        assert result == []

    def test_that_fetching_recipes_by_tag_with_none_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_tag(None)
        assert result == []

    def test_that_fetching_recipes_by_tag_with_empty_string_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_tag("")
        assert result == []

    def test_that_fetching_recipes_by_tag_with_wrong_type_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_tag(123)
        assert result == []

    def test_that_fetching_recipes_by_tag_should_be_case_insensitive_test(self, repo):
        result = repo.get_recipes_by_tag("JDBC")
        assert len(result) == 1
        assert result[0]["name"] == "Add Spring JDBC"

    def test_that_fetching_recipes_by_tag_should_return_multiple_recipes_test(self):
        data = [
            {"name": "Recipe 1", "tags": ["spring", "web"]},
            {"name": "Recipe 2", "tags": ["spring", "jdbc"]},
            {"name": "Recipe 3", "tags": ["testing"]}
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)
        result = repo.get_recipes_by_tag("spring")
        assert len(result) == 2
        names = [r["name"] for r in result]
        assert "Recipe 1" in names
        assert "Recipe 2" in names

    def test_that_fetching_recipes_by_tag_should_handle_recipes_without_tags_test(self):
        data = [
            {"name": "Recipe 1", "tags": ["spring"]},
            {"name": "Recipe 2"},  # no tags
            {"name": "Recipe 3", "tags": []}  # empty tags
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)
        result = repo.get_recipes_by_tag("spring")
        assert len(result) == 1
        assert result[0]["name"] == "Recipe 1"

    def test_that_fetching_recipes_by_tag_should_handle_non_list_tags_test(self):
        data = [
            {"name": "Recipe 1", "tags": ["spring"]},
            {"name": "Recipe 2", "tags": "invalid"},  # non-list tags
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)
        result = repo.get_recipes_by_tag("spring")
        assert len(result) == 1
        assert result[0]["name"] == "Recipe 1"

    def test_that_fetching_recipes_by_tag_should_handle_non_string_tag_values_test(self):
        data = [
            {"name": "Recipe 1", "tags": ["spring", 123]},  # mixed types
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)
        result = repo.get_recipes_by_tag("spring")
        assert len(result) == 1
        assert result[0]["name"] == "Recipe 1"

    def test_that_fetching_recipes_by_tag_with_very_long_tag_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_tag("x" * 10000)
        assert result == []
