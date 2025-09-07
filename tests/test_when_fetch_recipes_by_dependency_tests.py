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


class WhenFetchRecipesByDependencyTests:
    def test_that_fetching_recipes_by_existing_dependency_should_return_recipes_test(self, repo):
        result = repo.get_recipes_by_dependency("spring-boot-starter-jdbc")
        assert isinstance(result, list)
        assert json.dumps(result)  # serializable
        assert len(result) == 1
        assert result[0]["name"] == "Add Spring JDBC"

    def test_that_fetching_recipes_by_dependency_partial_should_match_test(self, repo):
        result = repo.get_recipes_by_dependency("jdbc")
        assert len(result) == 1
        assert result[0]["name"] == "Add Spring JDBC"

    def test_that_fetching_recipes_by_nonexistent_dependency_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_dependency("nonexistent")
        assert result == []

    def test_that_fetching_recipes_by_dependency_with_none_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_dependency(None)
        assert result == []

    def test_that_fetching_recipes_by_dependency_with_empty_string_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_dependency("")
        assert result == []

    def test_that_fetching_recipes_by_dependency_with_wrong_type_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_dependency(123)
        assert result == []

    def test_that_fetching_recipes_by_dependency_should_be_case_insensitive_test(self, repo):
        result = repo.get_recipes_by_dependency("SPRING-BOOT-STARTER-JDBC")
        assert len(result) == 1
        assert result[0]["name"] == "Add Spring JDBC"

    def test_that_fetching_recipes_by_dependency_should_return_multiple_matches_test(self):
        data = [
            {"name": "Recipe 1", "dependency": "org.springframework:spring-core"},
            {"name": "Recipe 2", "dependency": "org.springframework:spring-web"},
            {"name": "Recipe 3", "dependency": "junit:junit"}
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)
        result = repo.get_recipes_by_dependency("org.springframework")
        assert len(result) == 2
        names = [r["name"] for r in result]
        assert "Recipe 1" in names
        assert "Recipe 2" in names

    def test_that_fetching_recipes_by_dependency_should_handle_recipes_without_dependency_test(self):
        data = [
            {"name": "Recipe 1", "dependency": "spring-boot"},
            {"name": "Recipe 2"}  # no dependency
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)
        result = repo.get_recipes_by_dependency("spring-boot")
        assert len(result) == 1
        assert result[0]["name"] == "Recipe 1"

    def test_that_fetching_recipes_by_dependency_should_handle_non_string_dependencies_test(self):
        data = [
            {"name": "Recipe 1", "dependency": "spring-boot"},
            {"name": "Recipe 2", "dependency": 123}  # non-string dependency
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)
        result = repo.get_recipes_by_dependency("spring-boot")
        assert len(result) == 1
        assert result[0]["name"] == "Recipe 1"

    def test_that_fetching_recipes_by_dependency_with_very_long_dependency_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_dependency("x" * 10000)
        assert result == []

    def test_that_fetching_recipes_by_dependency_should_match_at_beginning_middle_and_end_test(self):
        data = [
            {"name": "Recipe 1", "dependency": "spring-boot-starter"},
            {"name": "Recipe 2", "dependency": "org.springframework:spring-boot-starter"},
            {"name": "Recipe 3", "dependency": "starter-web"}
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)
        result = repo.get_recipes_by_dependency("starter")
        assert len(result) == 3
