import json
import pytest
import os
import tempfile
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
def temp_json_file(sample_data):
    """Create a temporary JSON file with sample data."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_data, f)
        temp_path = f.name
    yield temp_path
    # Cleanup
    os.unlink(temp_path)


@pytest.fixture
def repo(temp_json_file):
    return RecipeRepository(temp_json_file)


class WhenFetchAllCategoriesTests:
    def test_that_fetching_all_categories_should_return_unique_sorted_list_test(self, repo):
        result = repo.get_all_categories()
        assert isinstance(result, list)
        assert json.dumps(result)  # serializable
        assert result == ["spring", "testing"]

    def test_that_fetching_all_categories_with_empty_dataset_should_return_empty_list_test(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([], f)
            temp_path = f.name

        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_all_categories()
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_that_fetching_all_categories_with_invalid_dataset_should_return_empty_list_test(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("null")
            temp_path = f.name

        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_all_categories()
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_that_fetching_all_categories_with_malformed_dataset_should_return_empty_list_test(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('"not a list"')
            temp_path = f.name

        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_all_categories()
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_that_fetching_all_categories_with_case_variations_should_normalize_to_lowercase_test(self):
        data = [
            {"category": "Spring"},
            {"category": "SPRING"},
            {"category": "Testing"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name

        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_all_categories()
            assert result == ["spring", "testing"]
        finally:
            os.unlink(temp_path)

    def test_that_fetching_all_categories_with_missing_category_field_should_skip_recipes_test(self):
        data = [
            {"name": "Recipe 1"},
            {"category": "spring", "name": "Recipe 2"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name

        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_all_categories()
            assert result == ["spring"]
        finally:
            os.unlink(temp_path)
