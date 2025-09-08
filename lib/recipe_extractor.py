import os
import json
from bs4 import BeautifulSoup
import re
import hashlib
from typing import List, Dict, Optional, Tuple


class RecipeExtractor:
    """Extracts OpenRewrite recipes from HTML documentation and generates JSON database."""

    def __init__(self, base_path: str = "resource/docs.openrewrite.org",
                 output_file: str = "resource/db/recipes.json"):
        self.base_path = base_path
        self.output_file = output_file
        self.recipes: List[Dict] = []
        self.processed_files = set()
        self.category_counts = {}

    def extract_recipes(self) -> List[Dict]:
        """Main method to extract recipes from documentation."""
        print("Starting recipe extraction using file system approach...")

        recipes_dir = os.path.join(self.base_path, 'recipes')
        if not os.path.exists(recipes_dir):
            print(f"Recipes directory not found: {recipes_dir}")
            return []

        self.process_directory(recipes_dir)

        # Filter out recipes without mvn-command-line
        self.recipes = [r for r in self.recipes if r.get('mvn-command-line')]

        # Save to JSON
        self.save_to_json()

        # Print statistics
        self.print_statistics()

        return self.recipes

    def parse_recipe_file(self, recipe_path: str) -> Optional[Dict]:
        """Parse individual recipe HTML file and extract data."""
        try:
            with open(recipe_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            # Extract name from title or h1
            name = "Unknown"
            title = soup.find('title')
            if title:
                name = title.get_text().strip().replace(' | OpenRewrite Docs', '')
            else:
                h1 = soup.find('h1')
                if h1:
                    name = h1.get_text().strip()

            # Extract description from meta description or first paragraph
            description = ""
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                description = meta_desc.get('content', '').strip()
            else:
                # Try to find description in the content
                h1 = soup.find('h1')
                if h1:
                    next_p = h1.find_next('p')
                    if next_p:
                        description = next_p.get_text().strip()

            # Extract Maven command line
            mvn_command = self._extract_maven_command(soup)

            # If no mvn command, skip this recipe
            if not mvn_command:
                return None

            # Extract package and dependency from Maven command
            package, dependency = self._extract_package_and_dependency(mvn_command, soup)

            # Swap name and description as per bug fix
            name, description = description, name

            # Set name to last part of package after last dot
            if package:
                name = package.split('.')[-1]

            return {
                "name": name,
                "description": description,
                "package": package,
                "dependency": dependency,
                "mvn-command-line": mvn_command
            }

        except Exception as e:
            print(f"Error parsing {recipe_path}: {e}")
            return None

    def _extract_maven_command(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract Maven command line from HTML content."""
        # Look for Maven Command Line tab content
        tabs = soup.find_all('div', class_='tabItem_Ymn6')
        for tab in tabs:
            tab_title = tab.find_previous('li', class_='tabs__item')
            if tab_title and 'Maven Command Line' in tab_title.get_text():
                pre = tab.find('pre')
                if pre:
                    code = pre.find('code')
                    if code:
                        return code.get_text().strip()

        # If not found in tabs, try to find any mvn command in pre blocks
        pre_blocks = soup.find_all('pre')
        for pre in pre_blocks:
            text = pre.get_text()
            if 'mvn ' in text and 'rewrite-maven-plugin' in text:
                return text.strip()

        return None

    def _extract_package_and_dependency(self, mvn_command: str, soup: BeautifulSoup) -> Tuple[Optional[str], Optional[str]]:
        """Extract package and dependency from Maven command and POM examples."""
        package = None
        dependency = None

        if mvn_command:
            # Look for -Drewrite.recipeArtifactCoordinates=
            dep_match = re.search(r'-Drewrite\.recipeArtifactCoordinates=([^\s]+)', mvn_command)
            if dep_match:
                dependency = dep_match.group(1)

            # Look for -Drewrite.activeRecipes=
            pkg_match = re.search(r'-Drewrite\.activeRecipes=([^\s]+)', mvn_command)
            if pkg_match:
                package = pkg_match.group(1)

        # If not found, try to extract from POM example
        if not package:
            pom_examples = soup.find_all('div', class_='codeBlockContent_biex')
            for example in pom_examples:
                text = example.get_text()
                if 'org.openrewrite' in text and 'rewrite-' in text:
                    # Extract groupId and artifactId
                    group_match = re.search(r'<groupId>([^<]+)</groupId>', text)
                    artifact_match = re.search(r'<artifactId>([^<]+)</artifactId>', text)
                    if group_match and artifact_match:
                        package = f"{group_match.group(1)}:{artifact_match.group(1)}"
                        dependency = package
                        break

        return package, dependency

    def determine_category_and_subcategory(self, file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """Determine category and subcategory from file path."""
        # Remove base path and get relative path
        rel_path = file_path.replace(self.base_path + '/', '')

        # Split path into parts
        path_parts = rel_path.split('/')

        # Remove 'recipes' from the beginning if present
        if path_parts[0] == 'recipes':
            path_parts = path_parts[1:]

        # Category is the first folder
        category = path_parts[0] if len(path_parts) > 1 else None

        # Sub-category is everything between category and filename
        if len(path_parts) > 2:
            sub_category_parts = path_parts[1:-1]  # Everything except first and last
            sub_category = '/'.join(sub_category_parts)

            # If sub-category has the same name as category, set to null
            if sub_category == category:
                sub_category = None
        else:
            sub_category = None

        return category, sub_category

    def process_directory(self, directory_path: str) -> None:
        """Process all HTML files in a directory recursively."""
        try:
            for root, dirs, files in os.walk(directory_path):
                # Skip the root recipes directory
                if root == os.path.join(self.base_path, 'recipes'):
                    continue

                for file in files:
                    if file.endswith('.html') and not file.endswith('README.html'):
                        file_path = os.path.join(root, file)

                        # Skip if already processed
                        if file_path in self.processed_files:
                            continue

                        # Determine category and subcategory
                        category, sub_category = self.determine_category_and_subcategory(file_path)

                        if category:
                            print(f"Processing: {file} (category: {category}, sub-category: {sub_category})")

                            # Parse the recipe
                            recipe_data = self.parse_recipe_file(file_path)
                            if recipe_data:
                                # Add category and subcategory info
                                recipe_data["category"] = category
                                recipe_data["sub-category"] = sub_category

                                # Generate unique ID
                                id_string = f"{recipe_data['name']}{recipe_data['category']}{recipe_data['sub-category'] or ''}"
                                recipe_data["id"] = hashlib.md5(id_string.encode()).hexdigest()

                                # Create tags
                                tags = []
                                if category:
                                    tags.append(category)
                                if sub_category:
                                    tags.append(sub_category)
                                recipe_data["tags"] = tags

                                # Create link
                                relative_path = file_path.replace(self.base_path + '/', '')
                                recipe_data["link"] = f"https://docs.openrewrite.org/{relative_path}"

                                self.recipes.append(recipe_data)
                                self.processed_files.add(file_path)

                                # Update category count
                                cat_key = category
                                if sub_category:
                                    cat_key += f"/{sub_category}"
                                self.category_counts[cat_key] = self.category_counts.get(cat_key, 0) + 1

        except Exception as e:
            print(f"Error processing directory {directory_path}: {e}")

    def save_to_json(self) -> None:
        """Save extracted recipes to JSON file."""
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.recipes, f, indent=2, ensure_ascii=False)

    def print_statistics(self) -> None:
        """Print extraction statistics."""
        total_recipes = len(self.recipes)
        open_source = total_recipes  # Assuming all are open source
        proprietary = 0

        print(f"\nExtraction complete!")
        print(f"Total recipes extracted: {total_recipes}")
        print(f"Open source recipes: {open_source}")
        print(f"Proprietary recipes: {proprietary}")
        print("\nRecipes per category:")
        for category, count in sorted(self.category_counts.items()):
            print(f"  {category}: {count}")
