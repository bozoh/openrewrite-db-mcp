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
        }
    ]


@pytest.fixture
def repo(sample_data):
    loader = Mock(return_value=sample_data)
    return RecipeRepository(load_json_callable=loader)


class WhenValidatingJsonResponseFormatTests:
    def test_that_all_list_responses_should_be_json_serializable_test(self, repo):
        # Test all methods that return lists
        methods = [
            lambda: repo.get_all_categories(),
            lambda: repo.get_categories_with_subcategories(),
            lambda: repo.get_subcategories_by_category("spring"),
            lambda: repo.get_recipes_by_category("spring"),
            lambda: repo.get_recipes_by_tag("spring"),
            lambda: repo.get_recipes_by_name("spring"),
            lambda: repo.get_recipes_by_dependency("spring")
        ]

        for method in methods:
            result = method()
            assert isinstance(result, list)
            # Should not raise exception
            json_str = json.dumps(result)
            assert isinstance(json_str, str)

    def test_that_single_item_response_should_be_json_serializable_and_dict_test(self, repo):
        result = repo.get_recipe_by_id("org.openrewrite.java.spring.AddSpringJdbc")
        assert isinstance(result, dict)
        # Should not raise exception
        json_str = json.dumps(result)
        assert isinstance(json_str, str)

    def test_that_empty_results_should_be_empty_list_or_empty_dict_consistently_test(self):
        # Use empty dataset for this test
        loader = Mock(return_value=[])
        empty_repo = RecipeRepository(load_json_callable=loader)

        # Test methods that return lists
        list_methods = [
            lambda: empty_repo.get_all_categories(),
            lambda: empty_repo.get_categories_with_subcategories(),
            lambda: empty_repo.get_subcategories_by_category("nonexistent"),
            lambda: empty_repo.get_recipes_by_category("nonexistent"),
            lambda: empty_repo.get_recipes_by_tag("nonexistent"),
            lambda: empty_repo.get_recipes_by_name("nonexistent"),
            lambda: empty_repo.get_recipes_by_dependency("nonexistent")
        ]

        for method in list_methods:
            result = method()
            assert result == []

        # Test method that returns dict
        result = empty_repo.get_recipe_by_id("nonexistent")
        assert result == {}

    def test_that_recipe_objects_should_contain_expected_fields_test(self, repo):
        result = repo.get_recipes_by_category("spring")
        assert len(result) > 0

        recipe = result[0]
        expected_fields = [
            "id", "name", "description", "package", "dependency",
            "mvn-command-line", "category", "sub-category", "tags", "link"
        ]

        for field in expected_fields:
            assert field in recipe

    def test_that_category_mapping_should_have_correct_structure_test(self, repo):
        result = repo.get_categories_with_subcategories()
        assert len(result) > 0

        category_item = result[0]
        assert "category" in category_item
        assert "sub-categories" in category_item
        assert isinstance(category_item["category"], str)
        assert isinstance(category_item["sub-categories"], list)

    def test_that_json_serialization_should_preserve_data_integrity_test(self, repo):
        original_result = repo.get_recipes_by_category("spring")
        json_str = json.dumps(original_result)
        deserialized_result = json.loads(json_str)

        assert original_result == deserialized_result

    def test_that_large_datasets_should_be_json_serializable_test(self):
        # Create a large dataset
        large_data = []
        for i in range(1000):
            large_data.append({
                "name": f"Recipe {i}",
                "category": "test",
                "id": f"id_{i}",
                "tags": ["tag1", "tag2"],
                "dependency": f"dep_{i}"
            })

        loader = Mock(return_value=large_data)
        repo = RecipeRepository(load_json_callable=loader)

        result = repo.get_recipes_by_category("test")
        assert len(result) == 1000

        # Should not raise exception even with large data
        json_str = json.dumps(result)
        assert len(json_str) > 0
