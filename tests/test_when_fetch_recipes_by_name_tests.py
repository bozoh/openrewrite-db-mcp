import json
import pytest
import tempfile
import os
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
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_data, f)
        temp_path = f.name
    yield RecipeRepository(temp_path)
    os.unlink(temp_path)


class WhenFetchRecipesByNameTests:
    def test_that_partial_case_insensitive_name_search_should_return_matching_recipes_test(self, repo):
        result = repo.get_recipes_by_name("spring")
        assert isinstance(result, list)
        assert json.dumps(result)  # serializable
        assert len(result) == 2
        names = [r["name"].lower() for r in result]
        assert "add spring jdbc" in names
        assert "add spring web" in names

    def test_that_partial_name_search_with_middle_substring_should_match_test(self, repo):
        result = repo.get_recipes_by_name("jdbc")
        assert len(result) == 1
        assert result[0]["name"] == "Add Spring JDBC"

    def test_that_name_search_with_nonexistent_term_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_name("nonexistent")
        assert result == []

    def test_that_name_search_with_none_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_name(None)
        assert result == []

    def test_that_name_search_with_empty_string_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_name("")
        assert result == []

    def test_that_name_search_with_wrong_type_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_name(123)
        assert result == []

    def test_that_name_search_should_be_case_insensitive_test(self, repo):
        result = repo.get_recipes_by_name("SPRING")
        assert len(result) == 2

    def test_that_name_search_should_handle_recipes_without_name_test(self):
        data = [
            {"name": "Recipe 1"},
            {},  # no name
            {"name": None}  # None name
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_recipes_by_name("Recipe")
            assert len(result) == 1
            assert result[0]["name"] == "Recipe 1"
        finally:
            os.unlink(temp_path)

    def test_that_name_search_should_handle_non_string_names_test(self):
        data = [
            {"name": "Recipe 1"},
            {"name": 123}  # non-string name
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_recipes_by_name("Recipe")
            assert len(result) == 1
            assert result[0]["name"] == "Recipe 1"
        finally:
            os.unlink(temp_path)

    def test_that_name_search_should_return_multiple_matches_test(self):
        data = [
            {"name": "Spring Boot Recipe"},
            {"name": "Spring MVC Recipe"},
            {"name": "JUnit Recipe"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_recipes_by_name("Spring")
            assert len(result) == 2
            names = [r["name"] for r in result]
            assert "Spring Boot Recipe" in names
            assert "Spring MVC Recipe" in names
        finally:
            os.unlink(temp_path)

    def test_that_name_search_with_very_long_query_should_return_empty_list_test(self, repo):
        result = repo.get_recipes_by_name("x" * 10000)
        assert result == []

    def test_that_name_search_should_match_at_beginning_middle_and_end_test(self):
        data = [
            {"name": "Spring Boot Recipe"},
            {"name": "Recipe with Spring in middle"},
            {"name": "Recipe ending with Spring"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_recipes_by_name("Spring")
            assert len(result) == 3
        finally:
            os.unlink(temp_path)
