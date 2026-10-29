---
name: extras-develop-plugin
description: "Développer un plugin yamcps autonome sans accès au dépôt du moteur, à partir des ressources MCP de ce skill : contrat public, projet complet, configuration, secrets, RAG, tests, packaging et README uniforme. Utiliser pour créer ou faire évoluer un connecteur métier ou un plugin de skills."
---

# Développer un plugin yamcps sans le dépôt du moteur

Ce guide et son asset contiennent les informations nécessaires au développement.
Ne pas demander le clone de yamcps, ses documents internes ou le code d'un autre
plugin. Travailler dans un nouveau projet de plugin, ou respecter les consignes
locales du projet de plugin existant si elles sont accessibles.

## Lire les ressources depuis MCP

1. Lire cette ressource : `skill://extras-develop-plugin/SKILL.md`.
2. Lire le [projet complet et les recettes](assets/plugin-template.md) avec
   `resources/read` sur `skill://extras-develop-plugin/assets/plugin-template.md`.
   Un lien relatif désigne ici une ressource du skill, pas un fichier du dépôt.
   Les clients compatibles peuvent aussi employer `skills/list` et `skills/get` ;
   lire ensuite le contenu des fichiers indiqués dans les ressources retournées.
3. Copier les fichiers du projet minimal de l'asset dans l'espace de travail du
   développeur, puis les adapter. Toutes les recettes et le modèle de README sont
   dans ce même asset ; aucune autre documentation yamcps n'est nécessaire.

Le serveur MCP fournit des instructions et des fichiers en lecture. Le client
agent ou le développeur doit pouvoir écrire et exécuter du Python sur sa machine.
Si le client n'a que la lecture MCP, produire les fichiers et commandes à copier,
mais ne pas annoncer de création, de test ou d'installation déjà effectués.
L'administrateur du serveur cible installe ensuite le wheel dans l'environnement
Python de ce serveur et le redémarre ; le client MCP distant ne l'installe pas.

Avant toute modification, lire `skill://extras-changelog/SKILL.md` et son
historique pour la version du moteur utilisée. Charger
`skill://extras-python/SKILL.md` pour le code et les contrôles Python ; charger
`skill://extras-configure-cicd/SKILL.md` pour créer ou modifier un workflow.

## Compatibilité et contrat public

Référence de ce guide : yamcps **0.4.1**, Python ≥ 3.12 et SDK `mcp>=2.3,<3`.
Pour un nouveau projet ciblant ces recettes, déclarer `yamcps>=0.4.1,<0.5`
dans les dépendances du plugin.
Vérifier les versions et imports dans l'environnement de développement ET celui du
serveur cible. Une distribution ou un wheel fourni par l'administrateur suffit,
sans sources du moteur :

```sh
python -c "from importlib.metadata import version; print(version('yamcps'), version('mcp'))"
python -c "from yamcps import ConfigSpec, ConnectorConfigs, RagConfig, RagContext; from yamcps.rag import RetrievalIndex"
```

Si une capacité manque, rester sur le contrat minimal ou obtenir un wheel du
moteur qui la fournit ; ne pas inventer une API ni installer un package RAG séparé.
Sur un poste hors ligne, utiliser un répertoire de wheels compatibles avec Python
et l'OS cibles : `python -m pip install --no-index --find-links /chemin/wheels yamcps`.
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
dans l'asset et ne nécessitent pas de consulter le dépôt du moteur.

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

## Réaliser le plugin

1. Définir opérations, entrées/sorties, accès métier et effets de chaque outil.
   Partir du projet minimal de l'asset ; ne pas importer un autre plugin.
2. Ajouter seulement les capacités nécessaires avec les recettes de l'asset.
   Les hooks, la factory et `register()` ne doivent faire aucun appel réseau,
   accès aux sources, ingestion ou chargement de modèle. Garder RAG paresseux :
   ne pas accéder à `context.index` pendant le démarrage.
3. Typer les interfaces et documenter les fonctions publiques en anglais avec
   des docstrings Google. Suivre PEP 8 ; formater/linter avec Ruff (100 caractères).
   Borner les entrées et délais réseau, fermer les clients, simuler les API dans
   les tests. Déporter les opérations bloquantes hors des handlers async.
4. Préserver stdout pour MCP stdio ; utiliser les logs stderr. Garder HTTP local
   par défaut. Ne pas ajouter d'authentification ou d'accès distant implicitement.
   Masquer les credentials ; ne jamais retourner les exceptions brutes d'une API.
   Décrire les effets réels via `ToolAnnotations` plutôt que déclarer une mutation
   en lecture seule. Les skills sont des fichiers servis, pas des scripts exécutés.
5. Appliquer le README uniforme ci-dessous et le modèle de l'asset. Inventorier
   seulement les outils, skills, configs et secrets réellement implémentés.
6. Exécuter les commandes de l'asset dans le projet autonome : découverte par
   entry point, tests unittest/MCP en mémoire et stdio, build wheel/sdist,
   installation du wheel et lecture du skill hors du projet. Ajouter des tests
   métier et de non-régression ainsi que les cas de collisions et d'erreurs utiles.
   Pour une modification liée à HTTP, tester aussi ce transport local.
7. Appliquer les contrôles qualité et la couverture de l'asset (objectif >80 %).
   Livrer les fichiers, le wheel, les commandes d'installation sur le serveur
   cible et les résultats réellement obtenus. Ne pas publier sur PyPI ni installer
   sur le serveur distant sans demande correspondante.

## Structure obligatoire du README des plugins

Conserver exactement ces titres, dans cet ordre, pour tout plugin créé ou modifié :

```markdown
# nom du plugin
## Description
## Quickstart
## Outils
## Skills
## Variable de configuration
## Secret
```

- Remplacer le titre principal par le nom de distribution réel (`yamcps-<nom>`).
  Écrire une description courte du rôle et du périmètre du plugin.
- Dans Quickstart, donner les prérequis, l'installation réellement disponible,
  les étapes de configuration nécessaires puis la commande de démarrage avec
  `--connector <id>`. Privilégier `yamcps configs set` pour les paramètres en clair
  et `yamcps secrets set` pour le vault ; aucun export ni secret en argument requis.
  Inclure l'ingestion préalable si nécessaire et un exemple d'utilisation court.
  Ne pas proposer une installation PyPI si le plugin n'y est pas publié.
- Dans Outils, fournir un tableau `Outil | Description` avec les noms MCP exacts
  des handlers enregistrés, leurs fonctions et leurs effets si pertinents.
- Dans Skills, fournir un tableau `Skill | Description` correspondant aux noms
  et descriptions des `SKILL.md` fournis par `skill_roots()`. Lier les fichiers
  locaux lorsque possible et expliquer leur lecture MCP dans Quickstart si utile.
- Dans Variable de configuration, fournir un tableau
  `Variable | Nom du champ | Description | Obligatoire | Valeur par défaut`.
  Relever les paramètres réellement consommés et les déclarations `ConfigSpec` ;
  vérifier les clés `YAMCPS_*` dans le code plutôt que les déduire approximativement.
  Distinguer une valeur vide autorisée de l'absence de défaut. Expliquer la commande
  de configuration dans Quickstart ; ces clés JSON ne nécessitent pas d'export.
- Dans Secret, fournir un tableau
  `Secret | Nom du champ | Description | Obligatoire` avec les clés exactes et les
  champs utilisés par `SecretSpec` / `ConnectorSecrets`. Décrire leur configuration
  via le vault dans Quickstart ; ne jamais inclure de valeur réelle ni de défaut
  contenant un identifiant sensible. Ne pas classer un secret comme config en clair.
- Garder les quatre tableaux même si une catégorie est vide : utiliser une ligne
  `Aucun` (ou `Aucune` pour les variables) et `—` dans les autres colonnes. Ne pas
  inventer de capacité, de paramètre ou de secret pour remplir une section.
- Préserver les informations utiles d'un README existant en les plaçant dans les
  sections correspondantes ou dans des guides liés ; garder ces six sections de
  niveau 2 et déplacer les détails longs vers la documentation spécialisée.
  Avant livraison, comparer les tableaux au code et vérifier commandes et liens.

## Résultat attendu

Un projet de plugin indépendant, installable avec le moteur distribué, documenté,
testé et livré sans dépendance au dépôt yamcps. Distinguer les étapes exécutées
localement de celles qui restent à effectuer sur le serveur cible.


### Secrets conditionnels (à partir de yamcps 0.4.0)

Le hook public facultatif synchrone
`required_secrets_for_configs(configs: ConnectorConfigs) -> Iterable[SecretSpec]`
sélectionne les secrets requis à partir de la configuration résolue, sans dépendre
d'un appel préalable à `configure_configs`. `required_secrets()` reste le catalogue
complet : le résultat conditionnel contient exclusivement des `SecretSpec` de ce
catalogue, identifiés par nom, sans doublon. Les descriptions du catalogue sont
utilisées pour les saisies. Sans ce hook, tous les secrets du catalogue restent requis.
Les déclarations invalides et les hooks asynchrones provoquent un `ConnectorError`
sans exposer leur diagnostic brut.

Ordre de démarrage : chargement normal des connecteurs sélectionnés ; résolution
des configurations (fichier, environnement, défauts, ou `config_values` explicite) ;
évaluation des besoins conditionnels ; collecte des seuls secrets manquants ;
`configure(secrets)` ; `configure_configs(configs)` ; RAG ; indexation des skills ;
enregistrement des outils. Toutes les sélections sont évaluées avant la première
demande de secret. Le hook valide lui-même la sélection métier ; le moteur ne
connaît aucun service ARR. Il ne doit faire aucun appel réseau.

Exemple à intégrer à un connecteur unique `arr` (implémenter aussi
`register(server)` et éventuellement `skill_roots()`) :

```python
from yamcps import ConfigSpec, ConnectorConfigs, ConnectorSecrets, SecretSpec


class ArrConnector:
    id = "arr"

    def required_configs(self) -> list[ConfigSpec]:
        """Declare the mandatory explicit service selection."""
        return [ConfigSpec("enabled-services", "Services activés, par exemple sonarr,seerr")]

    def required_secrets(self) -> list[SecretSpec]:
        """Return the complete credential catalogue."""
        return [
            SecretSpec(f"{service}-api-key")
            for service in ("sonarr", "radarr", "prowlarr", "seerr")
        ]

    def selected_services(self, configs: ConnectorConfigs) -> list[str]:
        """Validate the explicit service selection.

        Args:
            configs: Resolved plaintext settings.

        Returns:
            Selected service identifiers.

        Raises:
            ValueError: The selection is empty, duplicated or contains unknown names.
        """
        services = [name.strip() for name in configs.require("enabled-services").split(",")]
        allowed = {"sonarr", "radarr", "prowlarr", "seerr"}
        if (
            not services
            or any(name not in allowed for name in services)
            or len(set(services)) != len(services)
        ):
            raise ValueError("Invalid enabled-services selection")
        return services

    def required_secrets_for_configs(self, configs: ConnectorConfigs) -> list[SecretSpec]:
        """Select credentials before settings are injected.

        Args:
            configs: Resolved connector configuration.

        Returns:
            Only credentials for the selected services.
        """
        return [SecretSpec(f"{name}-api-key") for name in self.selected_services(configs)]

    def configure(self, secrets: ConnectorSecrets) -> None:
        """Retain credentials until the selected services are configured.

        Args:
            secrets: Connector-scoped credentials.
        """
        self.secrets = secrets

    def configure_configs(self, configs: ConnectorConfigs) -> None:
        """Configure only selected services before tools and skills are registered.

        Args:
            configs: Resolved connector settings.
        """
        self.services = self.selected_services(configs)
        self.api_keys = {
            name: self.secrets.require(f"{name}-api-key") for name in self.services
        }
```

Le plugin expose ensuite uniquement les outils et racines de skills de
`self.services`, sous sa responsabilité. Le moteur ne filtre pas les outils ou
les skills. Ne jamais retourner ni logger `api_keys`.

`yamcps configs set` reste indépendant des secrets.
`yamcps secrets set --connector arr --config-file /chemin/config.json` résout la
sélection avant de proposer les secrets actifs ; `--name` refuse un secret inactif
ou absent du catalogue conditionnel. Sans terminal et sans sélection requise,
la commande échoue en indiquant `yamcps configs set --connector arr`, sans lire
stdin ni demander tous les secrets. Désactiver un service ne supprime aucune
valeur du coffre ; sa réactivation réutilise les secrets existants au démarrage.
L'assistant explicite permet toujours de les conserver ou de les remplacer.

Redémarrer après modification : aucun changement dynamique à chaud.
Un plugin utilisant ce hook doit déclarer `yamcps>=0.4.0,<0.5` ; ce contrat n'est
pas disponible dans yamcps 0.3.0. Ce minimum reste valable avec le moteur 0.4.1 ;
les commandes d’édition introduites en 0.4.1 exigent cette dernière version.
