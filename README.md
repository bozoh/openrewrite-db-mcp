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
├── LICENSE                           # MIT License
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
# Run the MCP server directly from the GitHub repository (after merge to main/master)
uvx --from git+https://github.com/bozoh/openrewrite-db-mcp openrewrite-db-mcp

# Or specify a specific branch/tag
uvx --from git+https://github.com/bozoh/openrewrite-db-mcp@develop openrewrite-db-mcp
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

## MCP Server Details

### Available Tools

#### 1. `get_recipe_by_id`
Search for a specific OpenRewrite recipe by ID.

**Parameters:**
- `recipe_id` (string): Recipe ID to search for (e.g., "org.openrewrite.java.spring.AddSpringJdbc")

**Response format:**
```json
{
  "name": "Recipe Name",
  "id": "recipe.id",
  "category": "category",
  ...
}
```
Or `{}` if not found.

#### 2. `get_recipes_by_name`
Search OpenRewrite recipes by partial name match (case-insensitive).

**Parameters:**
- `name_query` (string): Search term for name (e.g., "spring", "jdbc")

**Response format:**
```json
[
  {
    "name": "Recipe Name",
    "id": "recipe.id",
    "category": "category",
    ...
  },
  ...
]
```
Or `[]` if no recipes match.

#### 3. `get_recipes_by_tag`
Search OpenRewrite recipes containing a specific tag.

**Parameters:**
- `tag` (string): Tag to search for (e.g., "spring", "java", "database")

**Response format:**
```json
[
  {
    "name": "Recipe Name",
    "id": "recipe.id",
    "tags": ["tag1", "tag2"],
    ...
  },
  ...
]
```
Or `[]` if no recipes contain the tag.

#### 4. `get_recipes_by_category`
Search OpenRewrite recipes by category and optionally subcategory.

**Parameters:**
- `category` (string): Recipe category (e.g., "spring", "java", "testing")
- `subcategory` (string, optional): Subcategory to filter by (e.g., "jdbc", "web", "junit")

**Response format:**
```json
[
  {
    "name": "Recipe Name",
    "id": "recipe.id",
    "category": "category",
    "sub-category": "subcategory",
    ...
  },
  ...
]
```
Or `[]` if no recipes match the criteria.

#### 5. `get_recipes_by_dependency`
Search OpenRewrite recipes by dependency (partial match, case-insensitive).

**Parameters:**
- `dependency` (string): Dependency to search for (e.g., "springframework", "junit", "org.springframework")

**Response format:**
```json
[
  {
    "name": "Recipe Name",
    "id": "recipe.id",
    "dependency": "dependency.string",
    ...
  },
  ...
]
```
Or `[]` if no recipes have matching dependencies.

#### 6. `get_all_categories`
Get all unique categories from the OpenRewrite recipes database.

**Parameters:** None

**Response format:**
```json
["category1", "category2", "category3", ...]
```

#### 7. `get_subcategories_by_category`
Get all subcategories for a specific category from the OpenRewrite recipes database.

**Parameters:**
- `category` (string): Category to get subcategories for (e.g., "spring", "java", "testing")

**Response format:**
```json
["subcategory1", "subcategory2", "subcategory3", ...]
```
Or `[]` if category not found or has no subcategories.

#### 8. `get_categories_with_subcategories`
Get all categories with their respective subcategories from the OpenRewrite recipes database.

**Parameters:** None

**Response format:**
```json
[
  {
    "category": "category1",
    "sub-categories": ["sub1", "sub2"]
  },
  {
    "category": "category2",
    "sub-categories": ["sub3", "sub4"]
  },
  ...
]
```

### VSCode Configuration

To use the MCP server with VSCode and AI assistants, configure it in your VSCode settings:

#### Option 1: Local Configuration
```json
{
  "mcp": {
    "servers": {
      "openrewrite-db": {
        "command": "uvx",
        "args": ["--from", ".", "openrewrite-db-mcp"]
      }
    }
  }
}
```

#### Option 2: Remote Configuration (after merge to main/master)
```json
{
  "mcp": {
    "servers": {
      "openrewrite-db": {
        "command": "uvx",
        "args": ["--from", "git+https://github.com/bozoh/openrewrite-db-mcp", "openrewrite-db-mcp"]
      }
    }
  }
}
```

#### Option 3: Remote Configuration from develop branch
```json
{
  "mcp": {
    "servers": {
      "openrewrite-db": {
        "command": "uvx",
        "args": ["--from", "git+https://github.com/bozoh/openrewrite-db-mcp@develop", "openrewrite-db-mcp"]
      }
    }
  }
}
```

### Error Handling

- Invalid inputs (None, empty strings, wrong types) return appropriate empty results
- Internal repository errors are caught and return empty results
- All responses are valid JSON strings

### Response Formats

- `get_recipe_by_id`: `{"name": "...", "id": "..."}` or `{}`
- List searches: `[{"name": "...", ...}]` or `[]`
- Categories: `["category1", "category2"]` or `[]`
- Categories with subcategories: `[{"category": "java", "sub-categories": ["spring", "hibernate"]}]` or `[]`

### Architecture

- `lib/mcp_service.py`: Service layer that validates inputs and handles errors
- `mcp_server/server.py`: MCP server with registered tools
- `mcp_server/main.py`: CLI entry point

## Contributing

This project follows TDD principles. When adding new features:

1. Write failing tests first
2. Implement the feature
3. Ensure all tests pass
4. Follow the established naming conventions

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
