# openrewrite-db-mcp

A Python tool that extracts OpenRewrite recipes from the official documentation and generates a structured JSON database for easy access and management.

## Prerequisites

- Python 3.10 or higher
- uv package manager (install via `pip install uv` or follow [uv installation guide](https://github.com/astral-sh/uv))

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd openrewrite-db-mcp
   ```

2. Install dependencies using uv:
   ```bash
   uv pip install -r requirements.txt
   ```

   Or if using uv's project management:
   ```bash
   uv sync
   ```

## Setup

Download the OpenRewrite recipes catalog from the official documentation:

```bash
cd resource && wget --recursive --no-clobber --html-extension --convert-links --no-parent --reject="*.jpg,*.jpeg,*.png,*.gif,*.css,*.js,*.svg,*.webp,*.ico" https://docs.openrewrite.org/recipes
```

This command will download all recipe documentation files to `resource/docs.openrewrite.org/recipes/`.

## Usage

Run the extraction script to process the downloaded recipes and generate the database:

```bash
python extract_recipes.py
```

The script will:
- Parse HTML files from `resource/docs.openrewrite.org/recipes/`
- Extract recipe metadata (name, description, Maven commands, dependencies)
- Categorize recipes by type and subcategory
- Generate a JSON database at `resource/db/recipes.json`

## Output

The generated `resource/db/recipes.json` contains an array of recipe objects with the following structure:

```json
{
  "id": "unique-hash",
  "name": "Recipe Name",
  "description": "Recipe description",
  "category": "category-name",
  "sub-category": "sub-category-name",
  "package": "org.openrewrite:rewrite-recipe-name",
  "dependency": "org.openrewrite:rewrite-recipe-name",
  "mvn-command-line": "mvn rewrite:run -Drewrite.activeRecipes=org.openrewrite.recipe-name",
  "tags": ["category", "sub-category"],
  "link": "https://docs.openrewrite.org/recipes/category/recipe-name"
}
```

## Project Structure

```
openrewrite-db-mcp/
├── extract_recipes.py          # Main extraction script
├── pyproject.toml              # Project configuration
├── requirements.txt            # Python dependencies
├── resource/
│   ├── db/
│   │   └── recipes.json        # Generated recipes database
│   └── docs.openrewrite.org/   # Downloaded documentation
├── .python-version             # Python version specification
└── README.md                   # This file
```

## Contributing

1. Ensure you have uv installed and configured
2. Follow the installation and setup steps above
3. Make your changes
4. Test the extraction script
5. Submit a pull request

## License

MIT - [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT)
