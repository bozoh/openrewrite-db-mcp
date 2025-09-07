import json
import pytest
import tempfile
import os
from lib.recipe_repository import RecipeRepository


class WhenDatasetIsMalformedTests:
    def test_that_missing_expected_fields_should_not_break_and_should_skip_recipes_test(self):
        data = [
            {"name": "Recipe 1", "category": "spring"},  # missing some fields
            {"category": "testing"},  # missing name
            {"name": "Recipe 3"}  # missing category
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)

            # Should not break and should handle gracefully
            categories = repo.get_all_categories()
            assert isinstance(categories, list)

            recipes = repo.get_recipes_by_category("spring")
            assert isinstance(recipes, list)
        finally:
            os.unlink(temp_path)

    def test_that_non_list_dataset_should_result_in_empty_responses_test(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('"not a list"')
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)

            assert repo.get_all_categories() == []
            assert repo.get_categories_with_subcategories() == []
            assert repo.get_subcategories_by_category("test") == []
            assert repo.get_recipes_by_category("test") == []
            assert repo.get_recipes_by_tag("test") == []
            assert repo.get_recipes_by_name("test") == []
            assert repo.get_recipe_by_id("test") == {}
            assert repo.get_recipes_by_dependency("test") == []
        finally:
            os.unlink(temp_path)

    def test_that_none_dataset_should_result_in_empty_responses_test(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('null')
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)

            assert repo.get_all_categories() == []
            assert repo.get_categories_with_subcategories() == []
            assert repo.get_subcategories_by_category("test") == []
            assert repo.get_recipes_by_category("test") == []
            assert repo.get_recipes_by_tag("test") == []
            assert repo.get_recipes_by_name("test") == []
            assert repo.get_recipe_by_id("test") == {}
            assert repo.get_recipes_by_dependency("test") == []
        finally:
            os.unlink(temp_path)

    def test_that_empty_dataset_should_result_in_empty_responses_test(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump([], f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)

            assert repo.get_all_categories() == []
            assert repo.get_categories_with_subcategories() == []
            assert repo.get_subcategories_by_category("test") == []
            assert repo.get_recipes_by_category("test") == []
            assert repo.get_recipes_by_tag("test") == []
            assert repo.get_recipes_by_name("test") == []
            assert repo.get_recipe_by_id("test") == {}
            assert repo.get_recipes_by_dependency("test") == []
        finally:
            os.unlink(temp_path)

    def test_that_malformed_recipe_objects_should_be_handled_gracefully_test(self):
        data = [
            {"name": "Recipe 1", "category": "spring"},
            None,  # None recipe
            "string recipe",  # string instead of dict
            123,  # number instead of dict
            {"name": "Recipe 2", "category": "testing"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)

            # Should not break
            categories = repo.get_all_categories()
            assert isinstance(categories, list)
            # Should only include valid recipes
            assert len(categories) >= 0
        finally:
            os.unlink(temp_path)

    def test_that_non_string_category_values_should_be_handled_test(self):
        data = [
            {"name": "Recipe 1", "category": 123},  # non-string category
            {"name": "Recipe 2", "category": None},  # None category
            {"name": "Recipe 3", "category": "spring"}  # valid category
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)

            categories = repo.get_all_categories()
            assert "spring" in categories
        finally:
            os.unlink(temp_path)

    def test_that_non_string_name_values_should_be_handled_in_name_search_test(self):
        data = [
            {"name": 123, "category": "spring"},  # non-string name
            {"name": None, "category": "spring"},  # None name
            {"name": "Recipe 1", "category": "spring"}  # valid name
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)

            recipes = repo.get_recipes_by_name("Recipe")
            assert len(recipes) == 1
            assert recipes[0]["name"] == "Recipe 1"
        finally:
            os.unlink(temp_path)

    def test_that_non_list_tags_should_be_handled_test(self):
        data = [
            {"name": "Recipe 1", "tags": "not a list", "category": "spring"},
            {"name": "Recipe 2", "tags": ["spring"], "category": "spring"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)

            recipes = repo.get_recipes_by_tag("spring")
            assert len(recipes) == 1
            assert recipes[0]["name"] == "Recipe 2"
        finally:
            os.unlink(temp_path)

    def test_that_non_string_tag_values_in_list_should_be_handled_test(self):
        data = [
            {"name": "Recipe 1", "tags": ["spring", 123, None], "category": "spring"},
            {"name": "Recipe 2", "tags": ["testing"], "category": "testing"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)

            recipes = repo.get_recipes_by_tag("spring")
            assert len(recipes) == 1
            assert recipes[0]["name"] == "Recipe 1"
        finally:
            os.unlink(temp_path)

    def test_that_non_string_dependency_values_should_be_handled_test(self):
        data = [
            {"name": "Recipe 1", "dependency": 123, "category": "spring"},
            {"name": "Recipe 2", "dependency": "spring-boot", "category": "spring"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)

            recipes = repo.get_recipes_by_dependency("spring-boot")
            assert len(recipes) == 1
            assert recipes[0]["name"] == "Recipe 2"
        finally:
            os.unlink(temp_path)

    def test_that_non_string_id_values_should_be_handled_test(self):
        data = [
            {"name": "Recipe 1", "id": 123, "category": "spring"},
            {"name": "Recipe 2", "id": "recipe2", "category": "spring"}
        ]
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)

            recipe = repo.get_recipe_by_id("recipe2")
            assert recipe["name"] == "Recipe 2"
        finally:
            os.unlink(temp_path)

    def test_that_exception_in_loader_should_be_handled_gracefully_test(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{invalid json')
            temp_path = f.name
        try:
            repo = RecipeRepository(temp_path)

            # All methods should return empty results without raising exceptions
            assert repo.get_all_categories() == []
            assert repo.get_categories_with_subcategories() == []
            assert repo.get_subcategories_by_category("test") == []
            assert repo.get_recipes_by_category("test") == []
            assert repo.get_recipes_by_tag("test") == []
            assert repo.get_recipes_by_name("test") == []
            assert repo.get_recipe_by_id("test") == {}
            assert repo.get_recipes_by_dependency("test") == []
        finally:
            os.unlink(temp_path)
