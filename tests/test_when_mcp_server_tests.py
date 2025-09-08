import pytest
from unittest.mock import patch, MagicMock
from mcp_server.server import build_server


class WhenMcpServerTests:
    @patch('mcp_server.server.RecipeRepository')
    @patch('mcp_server.server.RecipeMcpService')
    def test_that_server_can_be_built_with_fixed_path(self, mock_service, mock_repo):
        """Test that the MCP server can be built without errors using fixed path."""
        # Mock the repository and service
        mock_repo_instance = MagicMock()
        mock_service_instance = MagicMock()
        mock_repo.return_value = mock_repo_instance
        mock_service.return_value = mock_service_instance

        # This test verifies that the server can be instantiated
        server = build_server()

        # Verify that the server was created
        assert server is not None
        assert server.name == "openrewrite-recipes"

        # Verify that repository and service were created with the fixed path
        mock_repo.assert_called_once_with("resource/db/recipes.json")
        mock_service.assert_called_once_with(mock_repo_instance)
