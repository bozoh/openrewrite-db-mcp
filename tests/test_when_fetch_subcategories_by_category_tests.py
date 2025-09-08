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


class WhenFetchSubcategoriesByCategoryTests:
    def test_that_fetching_subcategories_by_existing_category_should_return_unique_sorted_list_test(self, repo):
        result = repo.get_subcategories_by_category("spring")
        assert isinstance(result, list)
        assert json.dumps(result)  # serializable
        assert result == ["jdbc", "web"]

    def test_that_fetching_subcategories_by_nonexistent_category_should_return_empty_list_test(self, repo):
        result = repo.get_subcategories_by_category("nonexistent")
        assert result == []

    def test_that_fetching_subcategories_by_category_with_none_should_return_empty_list_test(self, repo):
        result = repo.get_subcategories_by_category(None)
        assert result == []

    def test_that_fetching_subcategories_by_category_with_empty_string_should_return_empty_list_test(self, repo):
        result = repo.get_subcategories_by_category("")
        assert result == []

    def test_that_fetching_subcategories_by_category_with_wrong_type_should_return_empty_list_test(self, repo):
        result = repo.get_subcategories_by_category(123)
        assert result == []

    def test_that_fetching_subcategories_should_be_case_insensitive_on_category_test(self, repo):
        result = repo.get_subcategories_by_category("SPRING")
        assert result == ["jdbc", "web"]

    def test_that_fetching_subcategories_should_return_unique_values_test(self):
        data = [
            {"category": "spring", "sub-category": "jdbc"},
            {"category": "spring", "sub-category": "jdbc"},  # duplicate
            {"category": "spring", "sub-category": "web"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_subcategories_by_category("spring")
            assert result == ["jdbc", "web"]
        finally:
            os.unlink(temp_path)

    def test_that_fetching_subcategories_should_handle_recipes_without_subcategory_test(self):
        data = [
            {"category": "spring", "sub-category": "jdbc"},
            {"category": "spring"},  # no subcategory
            {"category": "testing", "sub-category": "junit"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_subcategories_by_category("spring")
            assert result == ["jdbc"]
        finally:
            os.unlink(temp_path)

    def test_that_fetching_subcategories_should_normalize_case_test(self):
        data = [
            {"category": "Spring", "sub-category": "JDBC"},
            {"category": "Spring", "sub-category": "Web"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_subcategories_by_category("spring")
            assert result == ["jdbc", "web"]
        finally:
            os.unlink(temp_path)

    def test_that_fetching_subcategories_with_very_long_category_should_return_empty_list_test(self, repo):
        result = repo.get_subcategories_by_category("x" * 10000)
        assert result == []
