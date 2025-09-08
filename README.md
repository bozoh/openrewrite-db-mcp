# OpenRewrite Recipe Database MCP

A Python library for querying OpenRewrite recipes stored in JSON format using JSONPath expressions. Includes an MCP (Model Context Protocol) server for AI assistants.

## Overview

This project implements a comprehensive RecipeRepository class that provides various methods to query OpenRewrite recipes from a JSON database. The implementation follows TDD (Test-Driven Development) principles with extensive unit test coverage.

## Features

The RecipeRepository class provides the following query methods:

- **get_all_categories()** - Get all unique categories
- **get_categories_with_subcategories()** - Get categories with their subcategories
- **get_subcategories_by_category(category)** - Get subcategories for a specific category
- **get_recipes_by_category(category, subcategory=None)** - Get recipes by category and optional subcategory
- **get_recipes_by_tag(tag)** - Get recipes containing a specific tag
- **get_recipes_by_name(name_query)** - Search recipes by partial name match (case-insensitive)
- **get_recipe_by_id(recipe_id)** - Get a single recipe by its ID
- **get_recipes_by_dependency(dependency)** - Get recipes by dependency (partial match)

All methods return results in JSON format and handle edge cases gracefully.

## Installation

1. Install uv if not already installed:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install Python dependencies:
```bash
uv sync
```

3. Run tests:
```bash
uv run pytest tests/
```

## Usage

```python
from lib.recipe_repository import RecipeRepository

# Create repository with JSON file path
repo = RecipeRepository("path/to/recipes.json")

# Query examples
categories = repo.get_all_categories()
recipes = repo.get_recipes_by_category("spring")
recipe = repo.get_recipe_by_id("org.openrewrite.java.spring.AddSpringJdbc")
```

## Test Coverage

The project includes comprehensive unit tests covering:

- **Success scenarios** for all methods
- **Failure scenarios** (empty results, non-existent items)
- **Invalid input handling** (wrong types, None values, empty strings)
- **Edge cases** (very long strings, malformed data)
- **JSON serialization validation**
- **Robustness against malformed datasets**

### Test Results
```
======================== 100 passed in 0.47s ========================
```

## Project Structure

```
.
├── lib/
│   ├── __init__.py
│   ├── recipe_repository.py          # Main RecipeRepository class
│   ├── mcp_service.py                # MCP service layer
│   └── recipe_extractor.py           # Recipe extraction utilities
├── mcp_server/
│   ├── __init__.py
│   ├── main.py                       # MCP server entry point
│   └── server.py                     # MCP server implementation
├── resource/
│   └── db/
│       └── recipes.json              # Recipe database
├── tests/
│   ├── __init__.py
│   ├── sample_recipes.json           # Test data
│   ├── test_when_fetch_all_categories_tests.py
│   ├── test_when_fetch_categories_with_subcategories_tests.py
│   ├── test_when_fetch_subcategories_by_category_tests.py
│   ├── test_when_fetch_recipes_by_category_and_subcategory_tests.py
│   ├── test_when_fetch_recipes_by_tag_tests.py
│   ├── test_when_fetch_recipes_by_name_tests.py
│   ├── test_when_fetch_recipe_by_id_tests.py
│   ├── test_when_fetch_recipes_by_dependency_tests.py
│   ├── test_when_validating_json_response_format_tests.py
│   ├── test_when_dataset_is_malformed_tests.py
│   ├── test_when_mcp_server_tests.py
│   └── test_when_running_mcp_server_with_uvx_tests.py
├── example_usage.py                   # Usage examples
├── main.py                           # CLI interface
├── pyproject.toml                    # Project configuration and dependencies
├── pytest.ini                        # Test configuration
├── README.md                         # This file
├── README_MCP.md                     # MCP-specific documentation
└── uv.lock                           # uv lock file
```

## Key Design Decisions

1. **Dependency Injection**: Uses a callable for data loading to support different data sources
2. **Lazy Loading**: Data is loaded only when first accessed
3. **Robust Error Handling**: Gracefully handles malformed data, missing fields, and exceptions
4. **Case-Insensitive Search**: Most searches are case-insensitive for better usability
5. **JSON-First**: All responses are JSON-serializable
6. **Type Safety**: Validates input types and handles edge cases

## Testing Strategy

- **100 unit tests** covering all methods and edge cases
- **TDD approach** with tests written before implementation
- **Mock usage** for isolating external dependencies
- **Comprehensive fixtures** with realistic sample data
- **Naming conventions** following the specified format

## Dependencies

- `pytest` - Testing framework
- `jsonpath-ng` - JSONPath query support (imported but not used in current implementation)
- `beautifulsoup4`, `requests`, `lxml` - For HTML parsing (from existing code)

## Running Tests

```bash
# Run all tests
uv run pytest tests/

# Run specific test file
uv run pytest tests/test_when_fetch_all_categories_tests.py

# Run with verbose output
uv run pytest tests/ -v

# Run example
uv run python example_usage.py
```

## Data Format

The expected JSON structure for recipes:

```json
[
  {
    "name": "string",
    "description": "string",
    "package": "string",
    "dependency": "string",
    "mvn-command-line": "string",
    "category": "string",
    "sub-category": "string",
    "id": "string",
    "tags": ["string"],
    "link": "string"
  }
]
```

## MCP Server

This project includes a Model Context Protocol (MCP) server that exposes the recipe database functionality to AI assistants and other MCP-compatible clients.

### Running the MCP Server

#### Option 1: From local directory
```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Run the MCP server
uvx --from . openrewrite-db-mcp
```

#### Option 2: Directly from GitHub repository
```bash
# Run the MCP server directly from the GitHub repository
uvx --from git+https://github.com/bozoh/openrewrite-db-mcp openrewrite-db-mcp
```

### MCP Server Features

The MCP server provides the following tools:

- **get_recipe_by_id(recipe_id)** - Get a single recipe by its ID
- **get_recipes_by_name(name_query)** - Search recipes by partial name match
- **get_recipes_by_tag(tag)** - Get recipes containing a specific tag
- **get_recipes_by_category(category, subcategory)** - Get recipes by category and optional subcategory
- **get_recipes_by_dependency(dependency)** - Get recipes by dependency package name
- **get_all_categories()** - Get all unique categories
- **get_subcategories_by_category(category)** - Get subcategories for a specific category
- **get_categories_with_subcategories()** - Get all categories with their subcategories

All tools return results in JSON format and are designed to work seamlessly with AI assistants.

## Contributing

This project follows TDD principles. When adding new features:

1. Write failing tests first
2. Implement the feature
3. Ensure all tests pass
4. Follow the established naming conventions

## License

This project is part of the OpenRewrite ecosystem.
