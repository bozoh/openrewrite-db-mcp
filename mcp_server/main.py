#!/usr/bin/env python3
"""
Main entry point for the OpenRewrite MCP server.
Uses the fixed path 'resource/db/recipes.json' for recipes data.
"""

from mcp_server.server import main


if __name__ == "__main__":
    main()
