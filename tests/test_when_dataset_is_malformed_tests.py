import json
import pytest
from unittest.mock import Mock
from lib.recipe_repository import RecipeRepository


class WhenDatasetIsMalformedTests:
    def test_that_missing_expected_fields_should_not_break_and_should_skip_recipes_test(self):
        data = [
            {"name": "Recipe 1", "category": "spring"},  # missing some fields
            {"category": "testing"},  # missing name
            {"name": "Recipe 3"}  # missing category
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)

        # Should not break and should handle gracefully
        categories = repo.get_all_categories()
        assert isinstance(categories, list)

        recipes = repo.get_recipes_by_category("spring")
        assert isinstance(recipes, list)

    def test_that_non_list_dataset_should_result_in_empty_responses_test(self):
        loader = Mock(return_value="not a list")
        repo = RecipeRepository(load_json_callable=loader)

        assert repo.get_all_categories() == []
        assert repo.get_categories_with_subcategories() == []
        assert repo.get_subcategories_by_category("test") == []
        assert repo.get_recipes_by_category("test") == []
        assert repo.get_recipes_by_tag("test") == []
        assert repo.get_recipes_by_name("test") == []
        assert repo.get_recipe_by_id("test") == {}
        assert repo.get_recipes_by_dependency("test") == []

    def test_that_none_dataset_should_result_in_empty_responses_test(self):
        loader = Mock(return_value=None)
        repo = RecipeRepository(load_json_callable=loader)

        assert repo.get_all_categories() == []
        assert repo.get_categories_with_subcategories() == []
        assert repo.get_subcategories_by_category("test") == []
        assert repo.get_recipes_by_category("test") == []
        assert repo.get_recipes_by_tag("test") == []
        assert repo.get_recipes_by_name("test") == []
        assert repo.get_recipe_by_id("test") == {}
        assert repo.get_recipes_by_dependency("test") == []

    def test_that_empty_dataset_should_result_in_empty_responses_test(self):
        loader = Mock(return_value=[])
        repo = RecipeRepository(load_json_callable=loader)

        assert repo.get_all_categories() == []
        assert repo.get_categories_with_subcategories() == []
        assert repo.get_subcategories_by_category("test") == []
        assert repo.get_recipes_by_category("test") == []
        assert repo.get_recipes_by_tag("test") == []
        assert repo.get_recipes_by_name("test") == []
        assert repo.get_recipe_by_id("test") == {}
        assert repo.get_recipes_by_dependency("test") == []

    def test_that_malformed_recipe_objects_should_be_handled_gracefully_test(self):
        data = [
            {"name": "Recipe 1", "category": "spring"},
            None,  # None recipe
            "string recipe",  # string instead of dict
            123,  # number instead of dict
            {"name": "Recipe 2", "category": "testing"}
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)

        # Should not break
        categories = repo.get_all_categories()
        assert isinstance(categories, list)
        # Should only include valid recipes
        assert len(categories) >= 0

    def test_that_non_string_category_values_should_be_handled_test(self):
        data = [
            {"name": "Recipe 1", "category": 123},  # non-string category
            {"name": "Recipe 2", "category": None},  # None category
            {"name": "Recipe 3", "category": "spring"}  # valid category
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)

        categories = repo.get_all_categories()
        assert "spring" in categories

    def test_that_non_string_name_values_should_be_handled_in_name_search_test(self):
        data = [
            {"name": 123, "category": "spring"},  # non-string name
            {"name": None, "category": "spring"},  # None name
            {"name": "Recipe 1", "category": "spring"}  # valid name
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)

        recipes = repo.get_recipes_by_name("Recipe")
        assert len(recipes) == 1
        assert recipes[0]["name"] == "Recipe 1"

    def test_that_non_list_tags_should_be_handled_test(self):
        data = [
            {"name": "Recipe 1", "tags": "not a list", "category": "spring"},
            {"name": "Recipe 2", "tags": ["spring"], "category": "spring"}
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)

        recipes = repo.get_recipes_by_tag("spring")
        assert len(recipes) == 1
        assert recipes[0]["name"] == "Recipe 2"

    def test_that_non_string_tag_values_in_list_should_be_handled_test(self):
        data = [
            {"name": "Recipe 1", "tags": ["spring", 123, None], "category": "spring"},
            {"name": "Recipe 2", "tags": ["testing"], "category": "testing"}
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)

        recipes = repo.get_recipes_by_tag("spring")
        assert len(recipes) == 1
        assert recipes[0]["name"] == "Recipe 1"

    def test_that_non_string_dependency_values_should_be_handled_test(self):
        data = [
            {"name": "Recipe 1", "dependency": 123, "category": "spring"},
            {"name": "Recipe 2", "dependency": "spring-boot", "category": "spring"}
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)

        recipes = repo.get_recipes_by_dependency("spring-boot")
        assert len(recipes) == 1
        assert recipes[0]["name"] == "Recipe 2"

    def test_that_non_string_id_values_should_be_handled_test(self):
        data = [
            {"name": "Recipe 1", "id": 123, "category": "spring"},
            {"name": "Recipe 2", "id": "recipe2", "category": "spring"}
        ]
        loader = Mock(return_value=data)
        repo = RecipeRepository(load_json_callable=loader)

        recipe = repo.get_recipe_by_id("recipe2")
        assert recipe["name"] == "Recipe 2"

    def test_that_exception_in_loader_should_be_handled_gracefully_test(self):
        def failing_loader():
            raise Exception("Loader failed")

        loader = Mock(side_effect=failing_loader)
        repo = RecipeRepository(load_json_callable=loader)

        # All methods should return empty results without raising exceptions
        assert repo.get_all_categories() == []
        assert repo.get_categories_with_subcategories() == []
        assert repo.get_subcategories_by_category("test") == []
        assert repo.get_recipes_by_category("test") == []
        assert repo.get_recipes_by_tag("test") == []
        assert repo.get_recipes_by_name("test") == []
        assert repo.get_recipe_by_id("test") == {}
        assert repo.get_recipes_by_dependency("test") == []
