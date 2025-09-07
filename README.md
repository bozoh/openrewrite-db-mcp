cd resource
wget --recursive --no-clobber --html-extension --convert-links --no-parent --reject="*.jpg,*.jpeg,*.png,*.gif,*.css,*.js,*.svg,*.webp,*.ico" https://docs.openrewrite.org/recipes

mvn -U org.openrewrite.maven:rewrite-maven-plugin:run -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-codemods:RELEASE -Drewrite.activeRecipes=org.openrewrite.codemods.cleanup.jest.NoJasmineGlobals -Drewrite.exportDatatables=true


Vôce é um agente perito em extração de dado de arquivos html usando python .

Seu objetivo e ler  o arquivo `resource/docs.openrewrite.org/recipes/recipes.html` e planejar a criação de um programa python para extrair todas as receitas listadas nele e nos links que ele tem, de forma recursiva, salvando-as em um arquivo JSON no seguinte estrutura:
```json
[
    {
        "name": "<NOME DA RECEITA>",
        "category": "<CATEGORIA DA RECEITA>",
        "sub-category": "<SUB-CATEGORIA DA RECEITA>",
        "tags": ["<TAG1>", "<TAG2>"],
        "description": "<DESCRIÇÃO DA RECEITA>",
        "link": "<LINK DA RECEITA>",
        "package": "<PACKAGE DA RECEITA>",
        "dependency": "<PACKAGE DA DEPENDÊCIA DA RECEITA>",
        "mvn-command-line": "<MAVE COMMAND LINE>"
       },
]
/html/body/div[1]/div[3]/div/div/main/div/div/div/div/article/div[2]/div[2]/div/div[4]/div/div[2]/pre/code/span

que deve ser salvo no arquivo `resource/db/recipes.json`

Foque em extrair o mvn-command-line corretamente, se não existir, deve ser nulo.
O mvn-command-line é a string que fica em `mvn -U org.openrewrite.maven:rewrite-maven-plugin:run -Drewrite.recipeArtifactCoordinates=<PACKAGE DA DEPENDÊCIA DA RECEITA> -Drewrite.activeRecipes=<NOME DA RECEITA> -Drewrite.exportDatatables=true`
Fica dentro da tag `<span class=token-line`, porém á muitas tags `<span class=token-line` no html, é imperativo que o mvn-command-line seja extraído corretamente.
Tente o XPATH /html/body/div[1]/div[3]/div/div/main/div/div/div/div/article/div[2]/div[2]/div/div[4]/div/div[2]/pre/code/span para extrair o mvn-command-line, se não funcionar, tente outro XPATH.

A categoria é o nome da pasta do arquivo html, por exemplo, se o arquivo html for `docs.openrewrite.org/recipes/java/refactorings/UseStringMethods.html`, a categoria é `java` e a sub-categoria `refactorings`.

Não modifique o arquivo html, apenas leia ele.
Não modifique a estrutura do JSON, apenas preencha os campos.
O campo tags é uma lista de strings, se não houver tags, deve ser preenchido com a categoria e sub-categoria.

O programa deve informar o progresso da extração no console, indicando quantas receitas foram extraídas e quantas faltam.

O final do programa deve imprimir no console o total de receitas extraídas, quantas são open source e quantas são proprietárias, quantas receitas por categoria.


docs.openrewrite.org/recipes/recipes.html


está quase certo, o nome do <PAKCAGE DA RECEITA> está  errado,  ele deve ser o que fica em `- Drewrite.activeRecipes=<PACKAGE DA RECEITA>` no `mvn-command-line`,  vode colou o PACKAGE DA RECEITA na `desctiption`,  precisa acertar a description também


Melhorou mas:

* O nome da receita  deve ser o que fica na tag `<header><h1>`, como nesse xpath `/html/body/div[1]/div[3]/div/div/main/div/div/div/div/article/div[2]/header/h1`

* O description fica logo abaixo do `<header>` em uma tag `<em>` com o xpath `//html/body/div[1]/div[3]/div/div/main/div/div/div/div/article/div[2]/p[2]/em`
o descrition ainda está errado,  ele deve ser o texto que fica logo abaixo do nome da receita,  e não o PACKAGE DA RECEITA,  veja o exemplo:

* O link deve ser  a url completa adicionando o `https://docs.openrewrite.org/`

Exemplo de receita correta:
```json
    {
        "name": "Migrate to Java 21",
        "category": "java",
        "sub-category": "migrate",
        "tags": ["java21"],
        "description": "This recipe will apply changes commonly needed when migrating to Java 21. This recipe will also replace deprecated API with equivalents when there is a clear migration strategy. Build files will also be updated to use Java 21 as the target/source and plugins will be also be upgraded to versions that are compatible with Java 21.",
        "link": "https://docs.openrewrite.org/recipes/java/migrate/upgradetojava21.html",
        "package": "org.openrewrite.java.migrate.UpgradeToJava21",
        "dependency": "org.openrewrite.recipe:rewrite-migrate-java:RELEASE",
        "mvn-command-line": "mvn -U org.openrewrite.maven:rewrite-maven-plugin:run -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-migrate-java:RELEASE -Drewrite.activeRecipes=org.openrewrite.java.migrate.UpgradeToJava21 -Drewrite.exportDatatables=true"
    },
```


quase lá, mas: 
* você está deixando de processar algunas receitas  como java/migrate, java/migrate/lombok/lombokvaluetorecord.html, tem que processar todas as receitas recursivamente.  

* e o nome da caetrgoria e sub-categoria está errado,  veja o exemplo acima,  a categoria é `java` e a sub-categoria `migrate/lombok`. A sub-categoria é o caminho completo da pasta,  não apenas a última pasta.
* Caso não haja sub-categoria,  deve ser nulo.
* Caso não haja tags,  deve ser uma lista com a categoria e sub-categoria.
* Caso nao haja mvn-command-line,  REMOVA A RECEITA DO JSON.

exemplo de receita correta:
```json
    {
        "name": "Convert @lombok.Value class to Record",
        "category": "java",
        "sub-category": "migrate/lombok",
        "tags": ["lombok"],
        "description": "Convert Lombok @Value annotated classes to standard Java Records.",
        "link": "https://docs.openrewrite.org/recipes/java/migrate/lombok/lombokvaluetorecord",
        "package": "org.openrewrite.java.migrate.lombok.LombokValueToRecord",
        "dependency": "org.openrewrite.recipe:rewrite-migrate-java:RELEASE",
        "mvn-command-line": "mvn -U org.openrewrite.maven:rewrite-maven-plugin:run -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-migrate-java:RELEASE -Drewrite.activeRecipes=org.openrewrite.java.migrate.lombok.LombokValueToRecord -Drewrite.exportDatatables=true"
    },
```


AInda não está processando tudo, vamos tentar uma outra abordagem.
* ao invés de tentar pegar todos os links do arquivo recipes.html,  tente pegar todas as pastas e sub-pastas dentro de resource/docs.openrewrite.org/recipes,  e para cada pasta,  pegue todos os arquivos html dentro dela,  e processe cada arquivo html individualmente 
* Não é necessário pegar os htmls da pasta resource/docs.openrewrite.org/recipes,  apenas das sub-pastas.
* Não é necessário mais process´ar os links dos arquivos html,  apenas extrair os dados do arquivo html.
* Se a categoria e a sub-categoria forem iguais, coloque null nas sub-categoria.




Vôce é um agente perito em extração de dado de arquivos html usando python .

analise o arquivo  `extract_recipes.py`  e o modifique para acrescentar um id único para cada receita extraída,  o id deve ser um hash md5 do campo `name` + `category` + `sub-category`,  o id deve ser salvo no campo `id` no JSON.:

```json
[
    {
        "id": "<ID ÚNICO>",
        "name": "<NOME DA RECEITA>",
        "category": "<CATEGORIA DA RECEITA>",
        "sub-category": "<SUB-CATEGORIA DA RECEITA>",
        "tags": ["<TAG1>", "<TAG2>"],
        "description": "<DESCRIÇÃO DA RECEITA>",
        "link": "<LINK DA RECEITA>",
        "package": "<PACKAGE DA RECEITA>",
        "dependency": "<PACKAGE DA DEPENDÊCIA DA RECEITA>",
        "mvn-command-line": "<MAVE COMMAND LINE>"
       },
]
```