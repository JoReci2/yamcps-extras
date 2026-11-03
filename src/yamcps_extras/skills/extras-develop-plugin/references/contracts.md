# Contrats publics et nommage

## Sommaire

- Compatibilité et imports
- Convention de nommage des plugins
- Logs et administration depuis 0.4.1

## Compatibilité et imports

Appliquer l’environnement `.venv` obligatoire décrit dans
`skill://extras-python/SKILL.md` avant toute commande de développement.
Utiliser `.venv/bin/python` (Windows : `.venv\Scripts\python.exe`) ;
réserver le Python système à la création de l’environnement.

Référence de ce guide : yamcps **0.4.1**, Python ≥ 3.12 et SDK `mcp>=2.3,<3`.
Pour un nouveau projet ciblant ces recettes, déclarer `yamcps>=0.4.1,<0.5`
dans les dépendances du plugin.
Vérifier les versions et imports dans l'environnement de développement ET celui du
serveur cible. Une distribution ou un wheel fourni par l'administrateur suffit,
sans sources du moteur :

```sh
.venv/bin/python -c "from importlib.metadata import version; print(version('yamcps'), version('mcp'))"
.venv/bin/python -c "from yamcps import ConfigSpec, ConnectorConfigs, RagConfig, RagContext; from yamcps.rag import RetrievalIndex"
```

Si une capacité manque, rester sur le contrat minimal ou obtenir un wheel du
moteur qui la fournit ; ne pas inventer une API ni installer un package RAG séparé.
Sur un poste hors ligne, utiliser un répertoire de wheels compatibles avec Python
et l'OS cibles : `.venv/bin/python -m pip install --no-index --find-links /chemin/wheels yamcps`.
Sans accès au runtime distant, faire vérifier cette compatibilité par son opérateur.

| Élément | Contrat |
| --- | --- |
| Distribution / module / identifiant | `yamcps-weather` / `yamcps_weather` / `weather` ; noms kebab-case pour les identifiants, underscores pour les modules |
| Découverte | Entry point dans `yamcps.connectors`, nom égal à `id`, valeur `module:classe_ou_factory` appelable sans argument |
| Base obligatoire | `id: str`, `register(server: MCPServer) -> None` synchrone ; aucune classe mère yamcps imposée |
| Enregistrement | `from mcp.server import MCPServer` ; décorateurs `@server.tool()`, `@server.prompt()` ou `@server.resource("scheme://...")` ; handlers sync ou async |
| Noms et collisions | Préfixer outils/prompts par `<id>_` (tirets de l'id remplacés par `_`) et choisir des URI propres ; doublons refusés |
| Configs facultatives | Deux hooks synchrones : `required_configs() -> Iterable[ConfigSpec]`, `configure_configs(configs: ConnectorConfigs) -> None` |
| Secrets facultatifs | `required_secrets() -> Iterable[SecretSpec]` pour l'assistant ; `configure(secrets: ConnectorSecrets) -> None` pour recevoir les valeurs |
| Secrets conditionnels (0.4.0) | `required_secrets_for_configs(configs: ConnectorConfigs) -> Iterable[SecretSpec]`, sous-ensemble du catalogue `required_secrets()` |
| RAG facultatif | Deux hooks synchrones : `rag_config() -> RagConfig`, `configure_rag(context: RagContext) -> None` |
| Skills facultatifs | `skill_roots() -> Iterable[Path]`, une racine par skill embarqué |
| Démarrage 0.4.0 | Résolution des configs → sélection des secrets requis → résolution des secrets → injection secrets puis configs → RAG → catalogue des skills → handlers |

Les imports des capacités sont publics : `from yamcps import ConfigSpec,
ConnectorConfigs, SecretSpec, ConnectorSecrets, RagConfig, RagContext`.
Pour la composition et les tests : `from yamcps.server import create_server`.
Pour les documents, l’index natif et le contrat de backend :
`from yamcps.rag import Document, Index, RetrievalIndex`.
Depuis yamcps 0.3.0, `RagConfig(index_factory=...)` permet un backend détenu par le
plugin ; la factory reste paresseuse et possède sa configuration de modèle.
`Index(..., source_namespace="weather")` et `Document(source_namespace="weather", ...)`
permettent des citations propres au plugin. Le moteur n'ajoute aucun outil RAG ni
ressource de citation automatiquement : les exposer dans le plugin si nécessaire.
Le moteur ne fournit pas de sandbox pour le code des plugins.

Le contrat est vérifié sur le [tag officiel v0.4.1](https://github.com/JoReci2/yamcps/blob/v0.4.1/CONTRIBUTING.md).
Cette référence sert à la traçabilité ; les recettes nécessaires restent embarquées
dans le modèle `assets/plugin-template.md` et ne nécessitent pas de consulter le dépôt du moteur.

Le hook de secrets conditionnels reçoit les configs résolues avant toute injection.
Il est synchrone, sans réseau et retourne uniquement des noms uniques présents dans
`required_secrets()`. Sans ce hook, tous les secrets déclarés restent requis.
Le plugin filtre lui-même ses outils et ses racines de skills selon sa configuration.
Voir la recette embarquée ; aucune suppression de secret du coffre n'est implicite.

## Convention de nommage des plugins

Déduire `id` du nom de distribution en retirant uniquement le préfixe initial
`yamcps-`. Conserver tous les segments suivants : `yamcps-<nom-plugin>`
donne `<nom-plugin>`, en conservant l’intégralité du nom après ce préfixe.
Utiliser cet identifiant complet pour l’entry point et `--connector`.
`<nom-plugin>` représente un nom quelconque en kebab-case, avec un ou plusieurs
segments ; `<nom_plugin>` et `<NOM_PLUGIN>` sont ses formes avec underscores,
respectivement en minuscules et majuscules. Les placeholders `<action>`,
`<CHAMP_CONFIG>` et `<CHAMP_SECRET>` sont à remplacer par les noms réels,
normalisés selon la ligne concernée. Aucun segment métier particulier n’est imposé.

| Élément | Règle | Forme générique pour `yamcps-<nom-plugin>` |
| --- | --- | --- |
| Module Python | Distribution avec tirets remplacés par `_` | `yamcps_<nom_plugin>` |
| Identifiant et entry point | Distribution sans le préfixe initial `yamcps-` | `<nom-plugin>` |
| Outil / prompt | Identifiant en snake_case + `_` + action | `<nom_plugin>_<action>` |
| Skill et dossier | Identifiant complet + `-` + action | `<nom-plugin>-<action>` |
| URI du skill | `skill://<nom-du-skill>/SKILL.md` | `skill://<nom-plugin>-<action>/SKILL.md` |
| Champ de configuration | Nom local en kebab-case dans `ConfigSpec` | `endpoint` |
| Variable de configuration | `YAMCPS_` + identifiant + `_` + champ, en majuscules avec `_` | `YAMCPS_<NOM_PLUGIN>_<CHAMP_CONFIG>` |
| Champ secret | Nom local en kebab-case dans `SecretSpec` | `api-token` |
| Clé du secret | Même normalisation que les configurations | `YAMCPS_<NOM_PLUGIN>_<CHAMP_SECRET>` |

Conserver le préfixe technique `YAMCPS_` des clés : le moteur le requiert.
Ne pas répéter l’identifiant dans `ConfigSpec("endpoint")`,
`SecretSpec("api-token")`, `configs.require("endpoint")` ou
`secrets.require("api-token")` : le moteur ajoute leur espace de noms.
Les variables Python locales restent en snake_case selon le skill Python.
Les noms MCP sont déclarés par le plugin ; le moteur ne les préfixe pas.

Lors de l’adaptation du projet `weather` de l’asset, remplacer ensemble distribution,
module, `id`, entry point, outils, skills, URI, clés et commandes du README.
Pour un plugin existant, inventorier les anciens noms et prévoir la migration des
consignes, clients, configurations et clés du vault avant tout renommage ; ne pas
supprimer silencieusement les valeurs existantes. Extras respecte déjà cette règle :
`yamcps-extras` → `extras`, skills `extras-*`.

## Logs et administration depuis 0.4.1

Utiliser un logger `yamcps.connectors.<id>` sans configurer de handler ni son niveau,
et conserver la propagation. La CLI gère stderr : INFO normalement, DEBUG avec
`yamcps serve --connector <id> --verbose`. L’hôte configure les logs si le serveur
est créé par l’API Python. Les bibliothèques tierces gardent leur niveau habituel.
Ne jamais journaliser les valeurs de configuration, secrets, entrées/sorties
métier, payloads HTTP ou exceptions brutes, même en DEBUG ; le moteur ne les nettoie
pas pour le plugin. Les logs ne sont pas des notifications MCP.

Pour documenter `configs list`, `configs edit` et `secrets edit`, et distinguer
édition du catalogue complet et secrets actifs, suivre la recette de l’asset.
Conserver des `ConfigSpec`/`SecretSpec` exacts et des descriptions utiles : la CLI
s’appuie sur ces déclarations. Aucun hook supplémentaire n’est nécessaire.
Un plugin existant limité au contrat 0.4.0 peut garder son minimum ; exiger 0.4.1
s’il utilise `remove`/`expected` des stores. Les nouvelles commandes nécessitent
un moteur 0.4.1 sur la machine de l’opérateur.

