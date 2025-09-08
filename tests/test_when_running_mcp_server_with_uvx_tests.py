import sys
import types
import pytest
from unittest.mock import patch, MagicMock

try:
    import tomllib  # Python 3.11+
except Exception:
    import tomli as tomllib  # fallback

class WhenRunningMcpServerWithUvxTests:
    @pytest.fixture
    def fixture_pyproject_dict(self):
        with open("pyproject.toml", "rb") as f:
            data = tomllib.load(f)
        return data

    def test_that_console_script_entry_is_declared(self, fixture_pyproject_dict):
        project = fixture_pyproject_dict.get("project", {})
        scripts = project.get("scripts", {})
        assert "openrewrite-db-mcp" in scripts, "Expected console script 'openrewrite-db-mcp' to be declared under [project.scripts]"
        assert scripts["openrewrite-db-mcp"] == "mcp_server.main:main", "Console script must point to 'mcp_server.main:main'"

    def test_that_console_script_declares_valid_target(self, fixture_pyproject_dict):
        project = fixture_pyproject_dict.get("project", {})
        scripts = project.get("scripts", {})
        target = scripts.get("openrewrite-db-mcp")
        assert isinstance(target, str) and ":" in target, "Script target must be in the form 'module:func'"
        module_name, func_name = target.split(":", 1)
        mod = __import__(module_name, fromlist=["*"])
        func = getattr(mod, func_name, None)
        assert callable(func), f"Target function '{func_name}' must be callable in module '{module_name}'"

    @patch("mcp_server.server.build_server")
    def test_that_main_invokes_server_run(self, mock_build_server):
        server_mock = MagicMock()
        mock_build_server.return_value = server_mock

        # Import here to ensure patches are applied correctly
        from mcp_server import server
        server.main()

        server_mock.run.assert_called_once_with()
