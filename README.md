# OpenRewrite Recipe Database MCP

A Python library for querying OpenRewrite recipes stored in JSON format using JSONPath expressions. Includes an MCP (Model Context Protocol) server for AI assistants.

## Overview

This project implements a comprehensive RecipeRepository class that provides various methods to query OpenRewrite recipes from a JSON database.

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

## Running the Project (CLI Mode)

To run the project in command-line interface mode, use the main.py script from the project root:

```bash
uv run python main.py
```

This will display the main menu with the following options:

- **[1] Extract recipes**: Extracts recipes from the downloaded HTML documentation and generates the JSON database.
- **[2] Query recipes**: Opens the queries menu to search and filter recipes.
- **[0] Exit**: Exits the application.

### Queries Menu

When selecting option [2] from the main menu, you'll access the queries menu with these options:

- **[1] List all categories**: Lists all unique categories.
- **[2] List categories with subcategories**: Lists categories with their subcategories.
- **[3] Get subcategories by category**: Searches subcategories for a specific category (requires input).
- **[4] Get recipes by category**: Searches recipes by category (optional subcategory).
- **[5] Get recipes by tag**: Searches recipes by tag.
- **[6] Get recipes by name**: Searches recipes by partial name match.
- **[7] Get recipe by ID**: Searches for a specific recipe by ID.
- **[8] Get recipes by dependency**: Searches recipes by dependency.
- **[0] Back to main menu**: Returns to the main menu.

All query results are displayed in JSON format.

## Getting the Recipe Data

To obtain the OpenRewrite recipes catalog data, first download the HTML documentation:

```bash
cd resource && wget --recursive --no-clobber --html-extension --convert-links --no-parent --reject="*.jpg,*.jpeg,*.png,*.gif,*.css,*.js,*.svg,*.webp,*.ico" https://docs.openrewrite.org/recipes
```

This command downloads the recipes documentation to `resource/docs.openrewrite.org/`, excluding images and other non-essential files.

After downloading, run the extraction process from the CLI (option [1] in main.py) to parse the HTML files and create the JSON database at `resource/db/recipes.json`.

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
- **update_recipes_database()** - Update the recipes database from fixed remote URLs

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

#### 9. `update_recipes_database`
Update the OpenRewrite recipes database from fixed remote URLs.

Downloads the latest recipes.json and recipes.json.sha256 from the main branch of the repository and saves them to the local database directory with SHA-256 verification.

**Parameters:** None (uses fixed URLs and destination directory)

**Response format:**
```json
{
  "success": true,
  "json_path": "resource/db/recipes.json",
  "sha256_path": "resource/db/recipes.json.sha256"
}
```
Or on error:
```json
{
  "success": false,
  "error": "error message"
}
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

## Contributing

This project follows TDD principles. When adding new features:

1. Write failing tests first
2. Implement the feature
3. Ensure all tests pass
4. Follow the established naming conventions

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
