import pytest
import json
import hashlib
import os
import tempfile
import requests
from unittest.mock import patch, Mock
from lib.recipe_repository import RecipeRepository


class WhenUpdatingRecipesDatabaseTests:
    """Test cases for updating recipes database from remote URLs."""

    def test_should_download_and_save_json_and_sha256_when_hash_matches(self, tmp_path):
        """Test successful download and save when SHA-256 hash matches."""
        # Setup
        db_dir = tmp_path / "db"
        json_url = "https://example.com/recipes.json"
        sha256_url = "https://example.com/recipes.json.sha256"

        # Sample JSON content
        json_content = {
            "name": "TestRecipe",
            "description": "A test recipe",
            "package": "org.openrewrite.test",
            "dependency": "org.openrewrite:test:1.0.0",
            "mvn-command-line": "mvn rewrite:run -Drewrite.activeRecipes=org.openrewrite.test.TestRecipe"
        }
        json_bytes = json.dumps(json_content, indent=2).encode('utf-8')

        # Calculate expected SHA-256
        expected_hash = hashlib.sha256(json_bytes).hexdigest()

        # Mock responses
        sha256_response = Mock()
        sha256_response.status_code = 200
        sha256_response.text = f"{expected_hash}\n"

        json_response = Mock()
        json_response.status_code = 200
        json_response.content = json_bytes

        repo = RecipeRepository("dummy.json")

        # Execute
        with patch('requests.get') as mock_get:
            mock_get.side_effect = [sha256_response, json_response]
            result_path = repo.update_from_remote(json_url, sha256_url, dest_dir=str(db_dir))

        # Verify
        assert result_path == str(db_dir / "recipes.json")
        assert (db_dir / "recipes.json").exists()
        assert (db_dir / "recipes.json.sha256").exists()

        # Verify JSON content
        with open(db_dir / "recipes.json", 'rb') as f:
            saved_content = f.read()
        assert saved_content == json_bytes

        # Verify SHA-256 file content
        with open(db_dir / "recipes.json.sha256", 'r') as f:
            saved_hash = f.read().strip()
        assert saved_hash == expected_hash

        # Verify hash of saved file matches
        actual_hash = hashlib.sha256(json_bytes).hexdigest()
        assert actual_hash == expected_hash

    def test_should_not_write_files_and_raise_when_hash_mismatch(self, tmp_path):
        """Test that files are not written and ValueError is raised when hash doesn't match."""
        # Setup
        db_dir = tmp_path / "db"
        db_dir.mkdir()
        json_url = "https://example.com/recipes.json"
        sha256_url = "https://example.com/recipes.json.sha256"

        # Pre-create files to ensure they are not overwritten
        json_file = db_dir / "recipes.json"
        sha256_file = db_dir / "recipes.json.sha256"
        json_file.write_text('{"pre-existing": "content"}')
        sha256_file.write_text("pre-existing-hash\n")

        original_json_content = json_file.read_text()
        original_sha256_content = sha256_file.read_text()

        # Sample JSON content
        json_content = {
            "name": "TestRecipe",
            "description": "A test recipe"
        }
        json_bytes = json.dumps(json_content).encode('utf-8')

        # Mock responses with mismatched hash
        sha256_response = Mock()
        sha256_response.status_code = 200
        sha256_response.text = "mismatched_hash_value\n"

        json_response = Mock()
        json_response.status_code = 200
        json_response.content = json_bytes

        repo = RecipeRepository("dummy.json")

        # Execute and verify
        with patch('requests.get') as mock_get:
            mock_get.side_effect = [sha256_response, json_response]
            with pytest.raises(ValueError, match="SHA-256 hash mismatch"):
                repo.update_from_remote(json_url, sha256_url, dest_dir=str(db_dir))

        # Verify files were not modified
        assert json_file.read_text() == original_json_content
        assert sha256_file.read_text() == original_sha256_content

    def test_should_raise_and_not_write_on_network_errors(self, tmp_path):
        """Test that RuntimeError is raised and no files written on network errors."""
        # Setup
        db_dir = tmp_path / "db"
        json_url = "https://example.com/recipes.json"
        sha256_url = "https://example.com/recipes.json.sha256"

        repo = RecipeRepository("dummy.json")

        # Execute and verify
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
            with pytest.raises(RuntimeError, match="Failed to download"):
                repo.update_from_remote(json_url, sha256_url, dest_dir=str(db_dir))

        # Verify no files were created
        assert not (db_dir / "recipes.json").exists()
        assert not (db_dir / "recipes.json.sha256").exists()
