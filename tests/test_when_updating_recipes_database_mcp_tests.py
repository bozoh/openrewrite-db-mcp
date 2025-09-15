import pytest
from unittest.mock import MagicMock
from lib.mcp_service import RecipeMcpService, JSON_URL, SHA256_URL, DEST_DIR


class WhenUpdatingRecipesDatabaseFromMcpTests:
    @pytest.fixture
    def repo_mock(self):
        return MagicMock()

    @pytest.fixture
    def service(self, repo_mock):
        return RecipeMcpService(repo_mock)

    def test_that_update_succeeds_and_returns_correct_structure(self, service, repo_mock):
        """Test successful update returns correct success structure."""
        expected_path = "resource/db/recipes.json"
        repo_mock.update_from_remote.return_value = expected_path

        result = service.update_recipes_database_fixed()

        assert isinstance(result, dict), "Result should be a dictionary"
        assert result["success"] is True, "Success should be True"
        assert result["json_path"] == expected_path, "JSON path should match"
        assert result["sha256_path"] == expected_path + ".sha256", "SHA256 path should be JSON path + .sha256"
        repo_mock.update_from_remote.assert_called_once_with(JSON_URL, SHA256_URL, DEST_DIR)

    def test_that_sha256_mismatch_returns_error_structure(self, service, repo_mock):
        """Test SHA-256 mismatch returns correct error structure."""
        error_msg = "SHA-256 hash mismatch: expected abc123, got def456"
        repo_mock.update_from_remote.side_effect = ValueError(error_msg)

        result = service.update_recipes_database_fixed()

        assert isinstance(result, dict), "Result should be a dictionary"
        assert result["success"] is False, "Success should be False"
        assert result["error"] == error_msg, "Error message should match"
        repo_mock.update_from_remote.assert_called_once_with(JSON_URL, SHA256_URL, DEST_DIR)

    def test_that_network_error_returns_error_structure(self, service, repo_mock):
        """Test network error returns correct error structure."""
        error_msg = "Failed to download recipes database: Connection timeout"
        repo_mock.update_from_remote.side_effect = RuntimeError(error_msg)

        result = service.update_recipes_database_fixed()

        assert isinstance(result, dict), "Result should be a dictionary"
        assert result["success"] is False, "Success should be False"
        assert result["error"] == error_msg, "Error message should match"
        repo_mock.update_from_remote.assert_called_once_with(JSON_URL, SHA256_URL, DEST_DIR)

    def test_that_unexpected_error_returns_error_structure(self, service, repo_mock):
        """Test unexpected error returns correct error structure."""
        error_msg = "Some unexpected error"
        repo_mock.update_from_remote.side_effect = Exception(error_msg)

        result = service.update_recipes_database_fixed()

        assert isinstance(result, dict), "Result should be a dictionary"
        assert result["success"] is False, "Success should be False"
        assert result["error"] == f"Unexpected error: {error_msg}", "Error message should be prefixed"
        repo_mock.update_from_remote.assert_called_once_with(JSON_URL, SHA256_URL, DEST_DIR)

    def test_that_fixed_urls_and_dest_are_used(self, service, repo_mock):
        """Test that the method uses the fixed URLs and destination directory."""
        repo_mock.update_from_remote.return_value = "resource/db/recipes.json"

        service.update_recipes_database_fixed()

        # Verify the exact call with fixed values
        repo_mock.update_from_remote.assert_called_once_with(
            "https://raw.githubusercontent.com/bozoh/openrewrite-db-mcp/main/resource/db/recipes.json",
            "https://raw.githubusercontent.com/bozoh/openrewrite-db-mcp/main/resource/db/recipes.json.sha256",
            "resource/db"
        )
