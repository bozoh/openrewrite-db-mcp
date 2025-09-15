import pytest
import json
import hashlib
import os
import tempfile
from lib.recipe_extractor import RecipeExtractor


class WhenGeneratingSha256Tests:
    """Test cases for SHA-256 hash generation functionality."""

    def test_should_generate_sha256_file_after_saving_json(self, tmp_path):
        """Test that SHA-256 file is generated after saving JSON."""
        # Setup
        json_file = tmp_path / "resource" / "db" / "test_recipes.json"
        extractor = RecipeExtractor(output_file=str(json_file))
        extractor.recipes = [
            {
                "name": "TestRecipe",
                "description": "A test recipe",
                "package": "org.openrewrite.test",
                "dependency": "org.openrewrite:test:1.0.0",
                "mvn-command-line": "mvn rewrite:run -Drewrite.activeRecipes=org.openrewrite.test.TestRecipe"
            }
        ]

        # Execute
        extractor.save_to_json()

        # Verify JSON file exists
        assert json_file.exists()

        # Verify SHA-256 file exists
        sha256_file = json_file.with_suffix(json_file.suffix + ".sha256")
        assert sha256_file.exists()

        # Verify SHA-256 content matches actual file hash
        expected_hash = self._calculate_sha256(str(json_file))
        with open(sha256_file, 'r', encoding='utf-8') as f:
            actual_hash = f.read().strip()

        assert actual_hash == expected_hash
        assert len(actual_hash) == 64  # SHA-256 hex is 64 characters

    def test_should_overwrite_existing_sha256_file(self, tmp_path):
        """Test that existing SHA-256 file is overwritten with new hash."""
        # Setup
        json_file = tmp_path / "resource" / "db" / "test_recipes.json"
        sha256_file = json_file.with_suffix(json_file.suffix + ".sha256")

        # Create existing SHA-256 file with wrong content
        os.makedirs(json_file.parent, exist_ok=True)
        with open(sha256_file, 'w', encoding='utf-8') as f:
            f.write("wrong_hash_value\n")

        extractor = RecipeExtractor(output_file=str(json_file))
        extractor.recipes = [
            {
                "name": "UpdatedRecipe",
                "description": "An updated test recipe",
                "package": "org.openrewrite.updated",
                "dependency": "org.openrewrite:updated:2.0.0",
                "mvn-command-line": "mvn rewrite:run -Drewrite.activeRecipes=org.openrewrite.updated.UpdatedRecipe"
            }
        ]

        # Execute
        extractor.save_to_json()

        # Verify SHA-256 file was overwritten with correct hash
        expected_hash = self._calculate_sha256(str(json_file))
        with open(sha256_file, 'r', encoding='utf-8') as f:
            actual_hash = f.read().strip()

        assert actual_hash == expected_hash
        assert actual_hash != "wrong_hash_value"

    def test_should_handle_empty_recipes_list(self, tmp_path):
        """Test SHA-256 generation with empty recipes list."""
        # Setup
        json_file = tmp_path / "resource" / "db" / "empty_recipes.json"
        extractor = RecipeExtractor(output_file=str(json_file))
        extractor.recipes = []

        # Execute
        extractor.save_to_json()

        # Verify files exist
        assert json_file.exists()
        sha256_file = json_file.with_suffix(json_file.suffix + ".sha256")
        assert sha256_file.exists()

        # Verify SHA-256 content
        expected_hash = self._calculate_sha256(str(json_file))
        with open(sha256_file, 'r', encoding='utf-8') as f:
            actual_hash = f.read().strip()

        assert actual_hash == expected_hash

    def test_should_handle_large_content_efficiently(self, tmp_path):
        """Test SHA-256 generation with larger content to verify chunked reading."""
        # Setup
        json_file = tmp_path / "resource" / "db" / "large_recipes.json"
        extractor = RecipeExtractor(output_file=str(json_file))

        # Create a larger recipes list to test chunked reading
        large_recipes = []
        for i in range(100):
            large_recipes.append({
                "name": f"Recipe{i}",
                "description": f"Description for recipe {i} with some additional text to make it longer",
                "package": f"org.openrewrite.test.Recipe{i}",
                "dependency": f"org.openrewrite:test{i}:1.0.{i}",
                "mvn-command-line": f"mvn rewrite:run -Drewrite.activeRecipes=org.openrewrite.test.Recipe{i}"
            })
        extractor.recipes = large_recipes

        # Execute
        extractor.save_to_json()

        # Verify files exist and hash is correct
        assert json_file.exists()
        sha256_file = json_file.with_suffix(json_file.suffix + ".sha256")
        assert sha256_file.exists()

        expected_hash = self._calculate_sha256(str(json_file))
        with open(sha256_file, 'r', encoding='utf-8') as f:
            actual_hash = f.read().strip()

        assert actual_hash == expected_hash

    def _calculate_sha256(self, file_path: str) -> str:
        """Helper method to calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
