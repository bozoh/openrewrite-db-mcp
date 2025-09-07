import os
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def extract_recipes():
    base_path = "resource/docs.openrewrite.org"
    recipes_file = "resource/db/recipes.json"
    recipes = []
    processed_recipes = set()
    category_counts = {}

    def parse_recipe_page(recipe_path, category, sub_category):
        """Parse individual recipe page and extract data"""
        try:
            with open(recipe_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            # Extract name from specific xpath: /html/body/div[1]/div[3]/div/div/main/div/div/div/div/article/div[2]/header/h1
            name = "Unknown"
            try:
                header_h1 = soup.select_one('body > div:nth-of-type(1) > div:nth-of-type(3) > div > div > main > div > div > div > div > article > div:nth-of-type(2) > header > h1')
                if header_h1:
                    name = header_h1.get_text().strip()
            except:
                # Fallback to title or h1
                title = soup.find('title')
                if title:
                    name = title.get_text().strip().replace(' | OpenRewrite Docs', '')
                else:
                    h1 = soup.find('h1')
                    if h1:
                        name = h1.get_text().strip()

            # Extract description from specific xpath: //html/body/div[1]/div[3]/div/div/main/div/div/div/div/article/div[2]/p[2]/em
            description = ""
            try:
                desc_em = soup.select_one('body > div:nth-of-type(1) > div:nth-of-type(3) > div > div > main > div > div > div > div > article > div:nth-of-type(2) > p:nth-of-type(2) > em')
                if desc_em:
                    description = desc_em.get_text().strip()
            except:
                # Fallback to meta description or first paragraph
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc:
                    description = meta_desc.get('content', '').strip()
                else:
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

            # If not found in tabs, try to find any mvn command
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

            # Tags: default to category and sub-category
            tags = []
            if category:
                tags.append(category)
            if sub_category:
                tags.append(sub_category)

            # Link: complete URL with https://docs.openrewrite.org/
            relative_path = recipe_path.replace(base_path + '/', '')
            link = f"https://docs.openrewrite.org/{relative_path}"

            recipe_data = {
                "name": name,
                "category": category,
                "sub-category": sub_category,
                "tags": tags,
                "description": description,
                "link": link,
                "package": package,
                "dependency": dependency,
                "mvn-command-line": mvn_command
            }

            return recipe_data

        except Exception as e:
            print(f"Error parsing {recipe_path}: {e}")
            return None

    def parse_category_page(category_path, category_name, current_sub_category=""):
        """Parse category page and find sub-categories or recipes recursively"""
        try:
            with open(category_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            # Find all links in the main content
            content = soup.find('main')
            if not content:
                return

            links = content.find_all('a', href=True)
            for link in links:
                href = link['href']
                if href.startswith('../') or href.startswith('http'):
                    continue

                # Convert relative links to absolute paths
                if href.startswith('./'):
                    href = href[2:]
                elif href.startswith('recipes/'):
                    pass
                else:
                    href = f"recipes/{href}"

                full_path = os.path.join(base_path, href)

                if os.path.exists(full_path):
                    if href.endswith('.html') and not href.endswith('README.html'):
                        # Check if it's a recipe page (has recipe content)
                        try:
                            with open(full_path, 'r', encoding='utf-8') as f:
                                page_soup = BeautifulSoup(f.read(), 'html.parser')
                                # Check if it has recipe-specific content
                                if page_soup.find('title') and 'OpenRewrite Docs' in page_soup.find('title').get_text():
                                    # Determine sub-category from path
                                    path_parts = href.replace('recipes/', '').replace('.html', '').split('/')
                                    recipe_name = path_parts[-1]

                                    # Build sub-category path
                                    if len(path_parts) > 1:
                                        sub_cat_parts = path_parts[:-1]  # All parts except the last (recipe name)
                                        if current_sub_category:
                                            sub_cat_parts = [current_sub_category] + sub_cat_parts
                                        sub_cat = '/'.join(sub_cat_parts)
                                    else:
                                        sub_cat = current_sub_category if current_sub_category else None

                                    # Skip if already processed
                                    if recipe_name in processed_recipes:
                                        continue

                                    print(f"Processing recipe: {recipe_name} (category: {category_name}, sub-category: {sub_cat})")
                                    recipe_data = parse_recipe_page(full_path, category_name, sub_cat)
                                    if recipe_data:
                                        recipes.append(recipe_data)
                                        processed_recipes.add(recipe_name)

                                        # Update category count
                                        cat_key = category_name
                                        if sub_cat:
                                            cat_key += f"/{sub_cat}"
                                        category_counts[cat_key] = category_counts.get(cat_key, 0) + 1

                        except Exception as e:
                            print(f"Error checking {full_path}: {e}")
                    elif href.endswith('/') or (not href.endswith('.html') and os.path.isdir(full_path)):
                        # This might be a sub-category directory
                        sub_dir_name = href.rstrip('/')
                        if '/' in sub_dir_name:
                            sub_dir_name = sub_dir_name.split('/')[-1]

                        # Build the sub-category path
                        new_sub_category = sub_dir_name
                        if current_sub_category:
                            new_sub_category = f"{current_sub_category}/{sub_dir_name}"

                        # Look for index.html in the sub-directory
                        index_path = os.path.join(full_path, 'index.html')
                        if os.path.exists(index_path):
                            print(f"Processing sub-category: {category_name}/{new_sub_category}")
                            parse_category_page(index_path, category_name, new_sub_category)

        except Exception as e:
            print(f"Error parsing category {category_path}: {e}")

    def parse_main_page():
        """Parse main recipes page to find categories"""
        main_path = os.path.join(base_path, "recipes", "recipes.html")
        if not os.path.exists(main_path):
            print(f"Main recipes file not found: {main_path}")
            return

        try:
            with open(main_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

            # Find category links
            links = soup.find_all('a', href=True)
            print(f"Found {len(links)} links in main page")
            category_count = 0
            for link in links:
                href = link['href']
                # Look for category links that are direct HTML files (not starting with http or ../)
                if (not href.startswith('http') and
                    not href.startswith('../') and
                    not href.startswith('recipes.html') and
                    href.endswith('.html') and
                    not href.endswith('README.html') and
                    '/' not in href):  # Direct category files like ai.html, java.html
                    category_name = href.replace('.html', '')
                    category_path = os.path.join(base_path, 'recipes', href)

                    if os.path.exists(category_path):
                        print(f"Processing category: {category_name}")
                        category_count += 1
                        parse_category_page(category_path, category_name)

            print(f"Total categories processed: {category_count}")

        except Exception as e:
            print(f"Error parsing main page: {e}")

    # Start processing
    print("Starting recipe extraction...")
    parse_main_page()

    # Filter out recipes without mvn-command-line
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
