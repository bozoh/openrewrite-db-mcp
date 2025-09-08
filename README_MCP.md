# OpenRewrite Recipes MCP Server

Este documento descreve como usar o servidor MCP (Model Context Protocol) para consultar receitas do OpenRewrite através de ferramentas MCP.

## Visão Geral

O servidor MCP expõe todas as funcionalidades de busca do `RecipeRepository` como ferramentas MCP, permitindo que agentes de IA consultem receitas de forma estruturada e padronizada.

## Ferramentas Disponíveis

### 1. `get_recipe_by_id`
Busca uma receita específica do OpenRewrite pelo ID.

**Parâmetros:**
- `recipe_id` (string): ID da receita a ser buscada (ex: "org.openrewrite.java.spring.AddSpringJdbc")

**Formato da resposta:**
```json
{
  "name": "Recipe Name",
  "id": "recipe.id",
  "category": "category",
  ...
}
```
Ou `{}` se não encontrada.

### 2. `get_recipes_by_name`
Busca receitas do OpenRewrite por correspondência parcial no nome (case-insensitive).

**Parâmetros:**
- `name_query` (string): Termo de busca no nome (ex: "spring", "jdbc")

**Formato da resposta:**
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
Ou `[]` se nenhuma receita corresponder.

### 3. `get_recipes_by_tag`
Busca receitas do OpenRewrite que contenham uma tag específica.

**Parâmetros:**
- `tag` (string): Tag a ser buscada (ex: "spring", "java", "database")

**Formato da resposta:**
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
Ou `[]` se nenhuma receita conter a tag.

### 4. `get_recipes_by_category`
Busca receitas do OpenRewrite por categoria e opcionalmente subcategoria.

**Parâmetros:**
- `category` (string): Categoria da receita (ex: "spring", "java", "testing")
- `subcategory` (string, opcional): Subcategoria para filtrar (ex: "jdbc", "web", "junit")

**Formato da resposta:**
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
Ou `[]` se nenhuma receita corresponder aos critérios.

### 5. `get_recipes_by_dependency`
Busca receitas do OpenRewrite por dependência (correspondência parcial, case-insensitive).

**Parâmetros:**
- `dependency` (string): Dependência a ser buscada (ex: "springframework", "junit", "org.springframework")

**Formato da resposta:**
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
Ou `[]` se nenhuma receita tiver dependências correspondentes.

### 6. `get_all_categories`
Retorna todas as categorias únicas disponíveis no banco de dados de receitas do OpenRewrite.

**Parâmetros:** Nenhum

**Formato da resposta:**
```json
["category1", "category2", "category3", ...]
```

### 7. `get_subcategories_by_category`
Retorna todas as subcategorias de uma categoria específica do OpenRewrite.

**Parâmetros:**
- `category` (string): Categoria para buscar subcategorias (ex: "spring", "java", "testing")

**Formato da resposta:**
```json
["subcategory1", "subcategory2", "subcategory3", ...]
```
Ou `[]` se a categoria não for encontrada ou não tiver subcategorias.

### 8. `get_categories_with_subcategories`
Retorna todas as categorias com suas respectivas subcategorias do banco de dados do OpenRewrite.

**Parâmetros:** Nenhum

**Formato da resposta:**
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

## Como Usar

### 1. Instalação das Dependências

```bash
uv sync
```

### 2. Executar o Servidor MCP

```bash
python -m mcp_server.main
```

Ou diretamente:

```bash
uv run python mcp_server/main.py
```

**Nota:** O servidor MCP sempre usa o arquivo fixo `resource/db/recipes.json` como fonte de dados.

### 3. Integração com Agentes

O servidor MCP se comunica via stdio, seguindo o protocolo MCP. Agentes compatíveis podem se conectar e usar as ferramentas listadas acima.

## Tratamento de Erros

- Entradas inválidas (None, string vazia, tipos incorretos) retornam resultados vazios apropriados
- Erros internos do repositório são capturados e retornam resultados vazios
- Todas as respostas são strings JSON válidas

## Formatos de Resposta

- `get_recipe_by_id`: `{"name": "...", "id": "..."}` ou `{}`
- Buscas de listas: `[{"name": "...", ...}]` ou `[]`
- Categorias: `["category1", "category2"]` ou `[]`
- Categorias com subcategorias: `[{"category": "java", "sub-categories": ["spring", "hibernate"]}]` ou `[]`

## Desenvolvimento

### Executar Testes

```bash
uv run pytest tests/test_when_*_mcp_tests.py -v
```

### Arquitetura

- `lib/mcp_service.py`: Camada de serviço que valida entradas e trata erros
- `mcp_server/server.py`: Servidor MCP com ferramentas registradas
- `mcp_server/main.py`: Ponto de entrada CLI

## Compatibilidade

- Python 3.10+
- MCP SDK 1.2.0+
- Funciona com qualquer cliente MCP compatível
