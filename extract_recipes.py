import os
import json
from bs4 import BeautifulSoup
import re

def extract_recipes():
    base_path = "resource/docs.openrewrite.org"
    recipes_file = "resource/db/recipes.json"
    recipes = []
    processed_files = set()
    category_counts = {}

    def parse_recipe_file(recipe_path):
        """Parse individual recipe HTML file and extract data"""
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
            mvn_command = None

            # Look for Maven Command Line tab content
            tabs = soup.find_all('div', class_='tabItem_Ymn6')
            for tab in tabs:
                tab_title = tab.find_previous('li', class_='tabs__item')
                if tab_title and 'Maven Command Line' in tab_title.get_text():
                    pre = tab.find('pre')
                    if pre:
                        code = pre.find('code')
                        if code:
                            mvn_command = code.get_text().strip()
                    break

            # If not found in tabs, try to find any mvn command in pre blocks
            if not mvn_command:
                pre_blocks = soup.find_all('pre')
                for pre in pre_blocks:
                    text = pre.get_text()
                    if 'mvn ' in text and 'rewrite-maven-plugin' in text:
                        mvn_command = text.strip()
                        break

            # If still no mvn command, skip this recipe
            if not mvn_command:
                return None

            # Extract package and dependency from Maven command
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

    def determine_category_and_subcategory(file_path):
        """Determine category and subcategory from file path"""
        # Remove base path and get relative path
        rel_path = file_path.replace(base_path + '/', '')

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

    def process_directory(directory_path):
        """Process all HTML files in a directory recursively"""
        try:
            for root, dirs, files in os.walk(directory_path):
                # Skip the root recipes directory
                if root == os.path.join(base_path, 'recipes'):
                    continue

                for file in files:
                    if file.endswith('.html') and not file.endswith('README.html'):
                        file_path = os.path.join(root, file)

                        # Skip if already processed
                        if file_path in processed_files:
                            continue

                        # Determine category and subcategory
                        category, sub_category = determine_category_and_subcategory(file_path)

                        if category:
                            print(f"Processing: {file} (category: {category}, sub-category: {sub_category})")

                            # Parse the recipe
                            recipe_data = parse_recipe_file(file_path)
                            if recipe_data:
                                # Add category and subcategory info
                                recipe_data["category"] = category
                                recipe_data["sub-category"] = sub_category

                                # Create tags
                                tags = []
                                if category:
                                    tags.append(category)
                                if sub_category:
                                    tags.append(sub_category)
                                recipe_data["tags"] = tags

                                # Create link
                                relative_path = file_path.replace(base_path + '/', '')
                                recipe_data["link"] = f"https://docs.openrewrite.org/{relative_path}"

                                recipes.append(recipe_data)
                                processed_files.add(file_path)

                                # Update category count
                                cat_key = category
                                if sub_category:
                                    cat_key += f"/{sub_category}"
                                category_counts[cat_key] = category_counts.get(cat_key, 0) + 1

        except Exception as e:
            print(f"Error processing directory {directory_path}: {e}")

    # Start processing
    print("Starting recipe extraction using file system approach...")

    recipes_dir = os.path.join(base_path, 'recipes')
    if os.path.exists(recipes_dir):
        process_directory(recipes_dir)
    else:
        print(f"Recipes directory not found: {recipes_dir}")
        return

    # Filter out recipes without mvn-command-line (shouldn't happen but just in case)
    recipes = [r for r in recipes if r.get('mvn-command-line')]

    # Save to JSON
    os.makedirs(os.path.dirname(recipes_file), exist_ok=True)
    with open(recipes_file, 'w', encoding='utf-8') as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)

    # Print statistics
    total_recipes = len(recipes)
    open_source = total_recipes  # Assuming all are open source
    proprietary = 0

    print(f"\nExtraction complete!")
    print(f"Total recipes extracted: {total_recipes}")
    print(f"Open source recipes: {open_source}")
    print(f"Proprietary recipes: {proprietary}")
    print("\nRecipes per category:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count}")

if __name__ == "__main__":
    extract_recipes()
