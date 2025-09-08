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


class WhenFetchCategoriesWithSubcategoriesTests:
    def test_that_fetching_categories_with_subcategories_should_return_mapping_test(self, repo):
        result = repo.get_categories_with_subcategories()
        assert isinstance(result, list)
        assert json.dumps(result)  # serializable

        expected = [
            {"category": "spring", "sub-categories": ["jdbc", "web"]},
            {"category": "testing", "sub-categories": ["junit"]}
        ]
        assert result == expected

    def test_that_fetching_categories_with_subcategories_with_empty_dataset_should_return_empty_list_test(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([], f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_categories_with_subcategories()
            assert result == []
        finally:
            os.unlink(temp_path)

    def test_that_fetching_categories_with_subcategories_should_return_unique_subcategories_test(self):
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
            result = repo.get_categories_with_subcategories()

            assert len(result) == 1
            assert result[0]["category"] == "spring"
            assert set(result[0]["sub-categories"]) == {"jdbc", "web"}
        finally:
            os.unlink(temp_path)

    def test_that_fetching_categories_with_subcategories_should_handle_recipes_without_subcategory_test(self):
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
            result = repo.get_categories_with_subcategories()

            expected = [
                {"category": "spring", "sub-categories": ["jdbc"]},
                {"category": "testing", "sub-categories": ["junit"]}
            ]
            assert result == expected
        finally:
            os.unlink(temp_path)

    def test_that_fetching_categories_with_subcategories_should_normalize_case_test(self):
        data = [
            {"category": "Spring", "sub-category": "JDBC"},
            {"category": "SPRING", "sub-category": "Web"},
            {"category": "Testing", "sub-category": "JUnit"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_categories_with_subcategories()

            expected = [
                {"category": "spring", "sub-categories": ["jdbc", "web"]},
                {"category": "testing", "sub-categories": ["junit"]}
            ]
            assert result == expected
        finally:
            os.unlink(temp_path)

    def test_that_fetching_categories_with_subcategories_should_sort_categories_and_subcategories_test(self):
        data = [
            {"category": "zebra", "sub-category": "zulu"},
            {"category": "alpha", "sub-category": "beta"},
            {"category": "zebra", "sub-category": "alpha"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)
            result = repo.get_categories_with_subcategories()

            assert result[0]["category"] == "alpha"
            assert result[0]["sub-categories"] == ["beta"]
            assert result[1]["category"] == "zebra"
            assert result[1]["sub-categories"] == ["alpha", "zulu"]
        finally:
            os.unlink(temp_path)
