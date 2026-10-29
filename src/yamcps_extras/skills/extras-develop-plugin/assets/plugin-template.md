# Projet autonome, recettes et README

Ce fichier est servi à `skill://extras-develop-plugin/assets/plugin-template.md`.
Il ne nécessite pas le dépôt du moteur. Le projet minimal expose un outil local
et un skill ; les recettes suivantes sont optionnelles et ne sont pas actives
avant leur ajout explicite au code.

Pour adapter ce projet, appliquer la section « Convention de nommage des plugins »
de `skill://extras-develop-plugin/SKILL.md` : retirer seulement le préfixe initial
`yamcps-` de la distribution pour obtenir l’identifiant complet, y compris ses
segments intermédiaires. `yamcps-<nom-plugin>` utilise `<nom-plugin>`,
`<nom_plugin>_<action>`, `<nom-plugin>-<action>`,
`YAMCPS_<NOM_PLUGIN>_<CHAMP_CONFIG>` et `YAMCPS_<NOM_PLUGIN>_<CHAMP_SECRET>`.
Dans le modèle README, `<id>_<outil>` utilise l’identifiant avec `_` à la place
des tirets ; `<id>-<action>` conserve les tirets.

## Projet minimal complet

Créer un dossier `yamcps-weather` avec exactement les fichiers ci-dessous.
Les titres de niveau 3 indiquent les chemins relatifs à ce nouveau dossier.
Ajouter aussi un `README.md` avec le modèle final, en l'adaptant à ce plugin.

### pyproject.toml

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "yamcps-weather"
version = "0.1.0"
description = "Example standalone yamcps connector"
requires-python = ">=3.12"
dependencies = ["yamcps>=0.4.1,<0.5"]

[project.optional-dependencies]
dev = ["build", "hatchling", "editables", "ruff", "mypy", "coverage", "bandit", "radon"]

[project.entry-points."yamcps.connectors"]
weather = "yamcps_weather:WeatherConnector"

[tool.hatch.build.targets.wheel]
packages = ["src/yamcps_weather"]

[tool.hatch.build.targets.sdist]
include = ["/src", "/tests", "/README.md", "/pyproject.toml"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.mypy]
python_version = "3.12"
strict = true
```

### src/yamcps_weather/__init__.py

```python
import logging
from collections.abc import Iterable
from pathlib import Path

from mcp.server import MCPServer
from mcp.types import ToolAnnotations


logger = logging.getLogger("yamcps.connectors.weather")


class WeatherConnector:
    """Expose a local status tool and a bundled usage skill."""

    id = "weather"

    def skill_roots(self) -> Iterable[Path]:
        """Return the installed skill directory.

        Returns:
            Bundled roots, independent of the current working directory.
        """
        return [Path(__file__).parent / "skills" / "weather-use"]

    def register(self, server: MCPServer) -> None:
        """Register read-only MCP tools.

        Args:
            server: Server receiving this connector's handlers.
        """

        @server.tool(
            annotations=ToolAnnotations(
                read_only_hint=True, destructive_hint=False, idempotent_hint=True
            )
        )
        async def weather_status() -> str:
            """Report readiness without contacting a weather service."""
            logger.debug("Reporting local readiness")
            return "ready"
```

### src/yamcps_weather/skills/weather-use/SKILL.md

```markdown
---
name: weather-use
description: Vérifier la disponibilité du connecteur weather avec son outil de statut local. Utiliser pour vérifier que ce plugin répond, sans obtenir de prévisions météo.
---

# Vérifier le connecteur weather

Appeler `weather_status`. La réponse `ready` confirme la disponibilité locale du
plugin ; elle ne valide pas de service météo externe et ne fournit aucune prévision.
```

### tests/test_weather.py

```python
import sys
import unittest
from importlib.metadata import entry_points

from mcp import Client, StdioServerParameters
from yamcps.server import create_server


class WeatherTests(unittest.IsolatedAsyncioTestCase):
    def test_installed_entry_point(self):
        entries = [e for e in entry_points(group="yamcps.connectors") if e.name == "weather"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].load()().id, "weather")

    async def exercise(self, target):
        async with Client(target) as client:
            self.assertEqual(
                {tool.name for tool in (await client.list_tools()).tools}, {"weather_status"}
            )
            result = await client.call_tool("weather_status", {})
            self.assertFalse(result.is_error)
            self.assertEqual(result.structured_content["result"], "ready")
            skill = await client.read_resource("skill://weather-use/SKILL.md")
            self.assertIn("weather_status", skill.contents[0].text)

    async def test_memory(self):
        await self.exercise(create_server(["weather"]))

    async def test_stdio(self):
        await self.exercise(
            StdioServerParameters(
                command=sys.executable,
                args=["-m", "yamcps", "serve", "--connector", "weather"],
            )
        )


if __name__ == "__main__":
    unittest.main()
```

Le skill n'est pas installé dans le client par ce projet. `skill_roots()` retourne
une racine par skill ; nom YAML et nom de dossier sont identiques, en minuscules
kebab-case, préfixés par `weather-`, de 64 caractères maximum. Chaque racine doit
contenir `SKILL.md` avec `name` et `description` non vide. Des assets peuvent être
ajoutés dans ce dossier : ils seront servis sous `skill://weather-use/<chemin>`.
Ne pas utiliser de symlinks ni de chemins sortant de la racine. Le catalogue est
figé au démarrage : redémarrer après modification. Hatchling embarque les fichiers
placés sous le module ; vérifier leur présence dans le wheel construit.
Pour des skills seuls, retirer le handler de `register` et ajuster les assertions
des tests ; une méthode avec seulement sa docstring reste un enregistrement vide.

## Installation, validation et livraison sans clone du moteur

Depuis le projet autonome :

```sh
python -m venv .venv
# Activer cet environnement selon le système.
python -m pip install -e '.[dev]'
python -c "from importlib.metadata import version; print(version('yamcps'), version('mcp'))"
yamcps connectors list
python -m unittest discover -s tests -p 'test_*.py'
ruff format src tests
ruff check src tests
mypy src
radon cc src -s -a
bandit -r src
coverage run --source=yamcps_weather -m unittest discover -s tests -p 'test_*.py'
coverage report --show-missing --fail-under=81
python -m build
```

Si le moteur est fourni par l'administrateur, installer son wheel et ses dépendances
avant le plugin. Pour un poste hors ligne, remplacer l'installation par
les commandes suivantes, puis construire avec `python -m build --no-isolation` :

```sh
python -m pip install --no-index --find-links /chemin/wheels hatchling editables build
python -m pip install --no-build-isolation --no-index --find-links /chemin/wheels -e '.[dev]'
```

Le répertoire de wheels doit contenir toutes les dépendances et les outils de
construction pour la plateforme cible ; un accès MCP seul ne les télécharge pas.
`editables` est nécessaire à l'installation de développement Hatchling ; sans ce
wheel, installer le wheel construit du plugin plutôt qu'utiliser `-e`.

Pour vérifier le wheel hors du projet, créer un second environnement et y installer
le wheel produit ainsi que yamcps et ses dépendances. Utiliser des chemins absolus :

```sh
python -m venv /chemin/absolu/wheel-check
/chemin/absolu/wheel-check/bin/python -m pip install /chemin/absolu/yamcps-weather/dist/yamcps_weather-0.1.0-py3-none-any.whl
cd /un/dossier/hors-du-projet
/chemin/absolu/wheel-check/bin/python -m unittest discover -s /chemin/absolu/yamcps-weather/tests -p 'test_*.py'
```

Sous Windows, utiliser `Scripts/python.exe` au lieu de `bin/python`. Ne pas définir
`PYTHONPATH` vers les sources pendant ce contrôle. Les tests vérifient découverte,
appel MCP en mémoire/stdio et lecture du skill installé. Pour HTTP local :
`yamcps serve --connector weather --transport http --port 8000`, puis connecter
un client MCP à `http://127.0.0.1:8000/mcp`. Arrêter le serveur après le contrôle.
Le démarrage stdio est `yamcps serve --connector weather` ; stdout appartient au MCP.
Pour un client distant, installer le wheel dans le runtime du serveur, puis
redémarrer/reconnecter. Répéter `--connector` pour combiner les plugins ; sans cette
option tous les entry points installés sont sélectionnés par ordre alphabétique.
Pour tester le refus des doublons, passer par la composition yamcps, par exemple
`create_server(["weather", "weather"])` doit lever `ValueError`. Un `MCPServer`
SDK utilisé directement n'applique pas nécessairement le refus du moteur.

## Recette : configurations et secrets

Imports publics : `from yamcps import ConfigSpec, ConnectorConfigs, SecretSpec,
ConnectorSecrets`. Ajouter ces méthodes DANS la classe du plugin, avant `register` :

```python
def required_configs(self) -> list[ConfigSpec]:
    """Declare the nonsecret service endpoint."""
    return [ConfigSpec("endpoint", "URL sans identifiants", default="http://localhost")]


def configure_configs(self, configs: ConnectorConfigs) -> None:
    """Receive the endpoint before registration.

    Args:
        configs: Connector-scoped plaintext settings.
    """
    self.endpoint = configs.require("endpoint")


def required_secrets(self) -> list[SecretSpec]:
    """Declare the API token without its value."""
    return [SecretSpec("api-token", "Token du service météo")]


def configure(self, secrets: ConnectorSecrets) -> None:
    """Receive masked credentials before registration.

    Args:
        secrets: Connector-scoped credentials.
    """
    self.token = secrets.require("api-token")
```

`ConfigSpec(name, description="", default=None)` déclare une chaîne obligatoire
sans défaut ; `default=""` ou un autre défaut la rend facultative. Utiliser
`configs.get(name) -> str | None` pour les valeurs vides autorisées, `require(name)`
pour une chaîne non vide. Les champs sont uniques et en kebab-case.
`SecretSpec(name, description="")` décrit un secret du catalogue ; sans sélection
conditionnelle, tous les secrets du catalogue sont requis.
`secrets.get(name)` retourne `SecretStr | None`, `require(name)` retourne `SecretStr`.
Extraire la valeur par `get_secret_value()` uniquement au moment d'appeler l'API.
`secrets.token_auth("api-token").authorization_header()` fournit un Bearer masqué ;
`secrets.basic_auth()` utilise les champs `username` et `password`. Les secrets ne
sont pas l'authentification du client MCP ; ce sont les credentials du service métier.

La clé est `YAMCPS_` + identifiant et champ en majuscules, tirets remplacés par `_` :
`endpoint` → `YAMCPS_WEATHER_ENDPOINT`, `api-token` → `YAMCPS_WEATHER_API_TOKEN`.
Les configs sont en clair dans `~/.config/yamcps/config.json`. Priorité : fichier,
puis ancienne variable d'environnement si absente du fichier, puis défaut ; une
valeur vide enregistrée prévaut. Le vault chiffré est distinct. Configurer avant
le lancement depuis un terminal, sans secrets dans les arguments ni export :

```sh
yamcps configs set --connector weather
yamcps secrets set --connector weather
yamcps serve --connector weather
```

`yamcps configs set --connector weather --name endpoint --value http://localhost`
permet une saisie non interactive non secrète. Serve et les commandes configs
acceptent `--config-file /chemin/absolu/yamcps.json`. Les champs requis manquants
sont demandés au démarrage interactif ; sans terminal, échec explicite sans lecture
du flux MCP. Un redémarrage est nécessaire après changement de configuration.
Pour tester sans toucher aux fichiers utilisateur, fournir à `create_server`
`config_values={"YAMCPS_WEATHER_ENDPOINT": "http://localhost"}` et
`secret_values={"YAMCPS_WEATHER_API_TOKEN": "fake-test-token"}` (valeurs de test).
Sans les hooks, aucune de ces capacités n'est requise pour un plugin minimal.

## Recette : logs et administration (yamcps 0.4.1)

Le logger du projet minimal hérite de la configuration du moteur. Ne pas appeler
`basicConfig`, `addHandler`, `setLevel` ni désactiver `propagate` dans le plugin.
DEBUG décrit les étapes de diagnostic, INFO les événements utiles en exploitation,
WARNING/ERROR les anomalies. Utiliser des messages sans valeurs de configuration,
secrets, arguments/résultats d’outils, corps/en-têtes HTTP ou exceptions brutes.
Le moteur ne filtre pas les messages arbitraires du plugin. L’API Python laisse
la configuration des handlers à l’application hôte.

```sh
yamcps serve --connector weather --verbose
```

Pour un client stdio, ajouter `--verbose` aux arguments du serveur ; les logs
restent sur stderr et ne sont pas des notifications MCP. Ne pas activer les logs
DEBUG des bibliothèques HTTP/MCP pour obtenir ceux du connecteur.
Tester les traces ajoutées avec un logger capturé et des valeurs fictives : absence
de données sensibles en DEBUG, propagation conservée et réponse MCP inchangée.

Si le plugin déclare des configs/secrets, documenter ces commandes dans Quickstart :

```sh
yamcps configs list --connector weather
yamcps configs edit --connector weather
yamcps secrets edit --connector weather
```

`configs list` présente Name, Description, Default et Stored value ; il montre les
valeurs stockées sans résoudre l’environnement ni appeler `configure_configs` ou
collecter de secrets. Une sortie redirigée est du TSV avec en-tête, pas un tableau
Rich à parser. `NO_COLOR` désactive les couleurs. La découverte `connectors list`
n’importe pas les plugins. Garder les déclarations sans réseau ni effets métier.

Les éditeurs exigent un terminal ; pour une automatisation, conserver `configs set`
et le provisionnement prévu du coffre. `serve` n’ouvre aucun éditeur plein écran.
`Ctrl+S` enregistre, `Ctrl+Q`/`Ctrl+C` annulent. Le JSON contient des chaînes et
clés normalisées sans doublons ; les secrets sont masqués et non vides. Retirer
une clé supprime la valeur enregistrée. Les configs sont en clair : aucun token.
`configs edit` accepte `--config-file`, `secrets edit` accepte `--vault`/`--key-file`.

La sélection `--connector` porte sur les clés déclarées exactes, pas un préfixe.
Les inconnues et les autres connecteurs sont préservés ; l’édition globale sans
sélection permet de gérer les anciennes clés. `secrets edit` présente le catalogue
complet `required_secrets()`, même pour les services inactifs ; `secrets set` et
le démarrage utilisent toujours `required_secrets_for_configs`. Ne pas confondre
cette édition avec la collecte des seuls secrets actifs. Redémarrer après modification.

Si une intégration modifie directement les stores, `ConfigStore.update` et
`Vault.update` acceptent en 0.4.1 `remove` et `expected` (snapshot original).
Utiliser la comparaison sous verrou pour détecter un conflit avant toute mutation ;
une édition constitue une transaction atomique. Sans `expected`, la fusion reste
compatible. Ne pas réimplémenter le coffre ou l’éditeur dans le plugin.

## Recette : secrets conditionnels (yamcps 0.4.0)

Ajouter ces méthodes à la classe du plugin avec les imports `ConfigSpec`,
`ConnectorConfigs`, `SecretSpec` et `ConnectorSecrets` de la recette précédente.
Cette variante remplace ses méthodes de configuration et de secrets :

```python
def required_configs(self) -> list[ConfigSpec]:
    """Declare the explicit operating mode."""
    return [ConfigSpec("mode", "public ou private", default="public")]


def required_secrets(self) -> list[SecretSpec]:
    """Declare the complete credential catalogue."""
    return [SecretSpec("api-token", "Token du service météo")]


def required_secrets_for_configs(self, configs: ConnectorConfigs) -> list[SecretSpec]:
    """Select credentials from resolved settings before injection.

    Args:
        configs: Resolved plaintext settings.

    Returns:
        Credentials required by the selected mode.

    Raises:
        ValueError: The mode is unsupported.
    """
    mode = configs.require("mode")
    if mode not in {"public", "private"}:
        raise ValueError("Unsupported weather mode")
    return self.required_secrets() if mode == "private" else []


def configure(self, secrets: ConnectorSecrets) -> None:
    """Retain scoped credentials until configuration injection.

    Args:
        secrets: Connector-scoped credentials.
    """
    self.secrets = secrets


def configure_configs(self, configs: ConnectorConfigs) -> None:
    """Configure the selected operating mode.

    Args:
        configs: Resolved plaintext settings.
    """
    self.mode = configs.require("mode")
    self.token = self.secrets.require("api-token") if self.mode == "private" else None
```

Tester le mode public sans secret, le mode privé avec un token fictif, son absence,
et un mode invalide. Le hook ne dépend pas de `configure_configs()`, appelé après.
Le moteur refuse les sélections inconnues, dupliquées ou asynchrones. Le plugin
choisit les outils et skills à exposer dans `register()` et `skill_roots()`.
`yamcps secrets set --connector weather` utilise les configurations résolues ;
`--name` refuse un secret inactif. Désactiver le mode privé ne supprime pas son
secret du coffre. Redémarrer le serveur après changement, sans reconfiguration à chaud.

## Recette : RAG natif facultatif

Imports publics : `from yamcps import RagConfig, RagContext` et
`from yamcps.rag import Document, Index`. Ajouter ces méthodes DANS la classe :

```python
def rag_config(self) -> RagConfig:
    """Declare lazy lexical retrieval for this connector."""
    return RagConfig()


def configure_rag(self, context: RagContext) -> None:
    """Retain the context without loading an index or model.

    Args:
        context: Connector-scoped retrieval context.
    """
    self.rag = context
```

Les deux hooks sont synchrones et indissociables. `RagConfig(index_path=Path(...),
model_path=Path(...))` accepte des chemins locaux optionnels. Sans chemin d'index,
le contexte utilise `~/.local/share/yamcps/rag/weather.sqlite3` (ou la racine
`YAMCPS_RAG_DIR`). Le moteur injecte le contexte après secrets/configs, avant
skills/handlers, sans indexation, chargement de modèle ou création de fichier.
Ne pas accéder à `self.rag.index` dans les hooks, la factory ou `register()`.

L'ingestion est une commande ou un script séparé du serveur. Exemple complet
lexical, à enregistrer dans `ingest.py` à la racine du plugin autonome :

```python
from yamcps import RagConfig, RagContext
from yamcps.rag import Document

index = RagContext("weather", RagConfig()).index
index.sync(
    "weather-demo",
    [
        Document(
            corpus="weather-demo",
            document_id="guide",
            revision="1",
            text="Le connecteur répond ready quand il est disponible.",
            metadata={"status": "approved"},
        )
    ],
)
```

`python ingest.py` prépare ce corpus, sous le même compte et avec les mêmes chemins
et modèle que le serveur. `sync(corpus, documents, *, chunk_size=1200)` reçoit le
snapshot COMPLET des révisions à conserver ; celles absentes sont supprimées et
une liste vide efface ce corpus. Les autres corpus restent inchangés. N'utiliser
cet exemple que pour son corpus de démonstration, sans toucher à un corpus existant.
`Document` contient du texte déjà extrait : le plugin lit PDF/DOCX/API lui-même.

Pour consulter dans un handler async ajouté à `register`, utiliser `asyncio.to_thread`
pour les appels bloquants. Exemple, après `import asyncio` :

```python
@server.tool()
async def weather_search(query: str) -> list[dict[str, object]]:
    """Search the explicitly ingested demonstration corpus."""

    def search() -> list[dict[str, object]]:
        hits = self.rag.index.search(query, "weather-demo", limit=5)
        return [hit.model_dump() for hit in hits]

    return await asyncio.to_thread(search)
```

L'accès à `self.rag.index`, qui peut charger le modèle, reste ainsi dans le thread.
`search(query, corpus, *, filters=None, limit=5)` exige un corpus, une requête non
vide (≤4000 caractères), une limite de 1 à 20 ; les filtres sont des égalités de
métadonnées combinées par ET. Les résultats incluent texte, document, révision,
source_uri, passage_id, offsets et score de classement (pas une probabilité).
`get_document(corpus, document_id, revision)`, `get_passage(passage_id)` et
`status(corpus)` lisent l'index ; une base absente n'est pas créée par la lecture.
Les corpus ne sont pas des autorisations ; SQLite conserve le texte en clair.

Le mode lexical ne nécessite pas de modèle. Pour des embeddings locaux, installer
`yamcps[rag]` sur la machine d'exécution. Le téléchargement explicite nécessite
`yamcps[rag]` sur la machine connectée :

```sh
yamcps models download sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
```

Copier le dossier résultant sur la machine hors ligne avec les dépendances Python
compatibles, puis fournir son chemin à `RagConfig(model_path=Path(...))`. Télécharger
ne l'active pas. Pour des chemins configurables, déclarer les champs `index` et
`model` avec `ConfigSpec(..., default="")`, les mémoriser dans `configure_configs`
et construire `RagConfig` à partir de ces valeurs. Ne pas imposer d'exports.
Un changement de modèle/mode nécessite un nouvel index et une réingestion.
Aucun téléchargement ni chargement de code distant implicite n'est permis.

### Backend détenu par le plugin (yamcps 0.3)

`from yamcps.rag import RetrievalIndex` expose le contrat structurel : `sync`,
`search`, `get_document`, `get_passage` et `status`, avec les signatures décrites
ci-dessous (yamcps 0.3.0). Les types de résultat sont publics dans `yamcps.rag` :

| Méthode | Résultat et contraintes |
| --- | --- |
| `sync(corpus: str, documents: list[Document], *, chunk_size: int = 1200)` | `dict[str, int]` : compteurs `updated`, `unchanged`, `deleted` ; snapshot atomique, taille de passage de 64 à 16000 caractères |
| `search(query: str, corpus: str, *, filters: dict[str, str] \| None = None, limit: int = 5)` | `list[SearchHit]` ; mêmes bornes de requête, filtres ET et limite que l'index natif |
| `get_document(corpus: str, document_id: str, revision: str)` | `Document` ; `ValueError` si la révision est indisponible |
| `get_passage(passage_id: str)` | `Passage` ; `ValueError` si la citation est indisponible |
| `status(corpus: str)` | `dict[str, str \| int \| None]` : champs `corpus`, `mode`, `documents`, `passages`, `last_changed_at` |

Une factory synchrone reçoit le chemin résolu (`Path`) et retourne ce backend ;
un backend distant peut ignorer ce chemin. Elle est appelée au premier accès à
`context.index`, sous verrou, une seule fois après succès. Après un échec, l'accès
suivant peut réessayer. `index_factory` doit être un callable synchrone et ne peut
pas être combiné avec `model_path` : la factory possède le modèle. Les chemins de
`RagConfig` sont des `Path` ou `None`, pas des chaînes.

Exemple avec le backend SQLite natif et un espace de sources propre au plugin :

```python
from pathlib import Path

from yamcps import RagConfig
from yamcps.rag import Index, RetrievalIndex


def weather_index(path: Path) -> RetrievalIndex:
    """Construct the backend without opening storage or loading a model."""
    return Index(path, source_namespace="weather")


# À retourner depuis rag_config(), également pour le script d'ingestion :
config = RagConfig(index_factory=weather_index)
```

Les documents ingérés doivent alors déclarer `source_namespace="weather"`.
Les citations deviennent `weather://source/...` ; le défaut reste `docs`.
Un index et ses documents doivent utiliser le même espace de sources. Changer
cet espace impose un nouvel index et une réingestion. Les accès bloquants restent
à déporter dans un thread ; un backend personnalisé doit respecter le contrat
atomique de `sync`, les frontières de corpus, les filtres et les références de
citations. Il doit supporter les appels concurrents. Le contrat ne prévoit pas de
cycle de vie pour un client réseau persistant : borner ses ressources à chaque
opération. Les dépendances du backend appartiennent au plugin.

Une `source_uri` identifie une source ; elle ne crée pas de ressource MCP.
Si le client doit pouvoir la lire, enregistrer dans le plugin une ressource
correspondante avec `@server.resource(...)`, et résoudre les documents/passages
avec le même backend. Tester la résolution des citations, l'absence d'initialisation
au démarrage, les accès concurrents et le rollback d'un snapshot invalide.

## README uniformisé

Créer `README.md` à la racine du package avec ce modèle. Remplacer tous les champs
entre chevrons d'après le plugin réel. Conserver les titres et l'ordre des sections.
Les quatre tableaux restent présents ; si une catégorie est vide, remplacer ses
lignes par `Aucun` (`Aucune` pour les variables) et `—` dans les autres colonnes.

````markdown
# yamcps-<nom>

## Description

<Description courte du rôle et du périmètre du plugin.>

## Quickstart

Prérequis : <version Python, services et droits nécessaires au plugin.>

Depuis la racine du projet autonome du plugin, dans un environnement Python activé :

```sh
python -m pip install -e .
yamcps connectors list
# Garder uniquement les commandes de configuration utiles au plugin :
yamcps configs set --connector <id>
yamcps secrets set --connector <id>
yamcps serve --connector <id>
```

<Adapter l'installation si le plugin est fourni sous forme de wheel.
Retirer les commandes de configuration inutiles et ce commentaire. Si nécessaire,
insérer la préparation du corpus et l'ingestion avant le démarrage.>

<Exemple d'utilisation court avec un outil ou un skill réellement exposé.>

## Outils

| Outil | Description |
| --- | --- |
| `<id>_<outil>` | <Fonction et effets de l'outil MCP.> |

## Skills

| Skill | Description |
| --- | --- |
| [`<id>-<action>`](src/<module>/skills/<id>-<action>/SKILL.md) | <Description du skill exposé.> |

## Variable de configuration

| Variable | Nom du champ | Description | Obligatoire | Valeur par défaut |
| --- | --- | --- | --- | --- |
| `<clé YAMCPS_* exacte>` | `<nom du champ>` | <Paramètre non secret.> | <Oui ou Non> | <Défaut réel, chaîne vide autorisée ou Aucun> |

## Secret

| Secret | Nom du champ | Description | Obligatoire |
| --- | --- | --- | --- |
| `<clé YAMCPS_* exacte>` | `<nom du champ>` | <Rôle du secret conservé dans le vault, sans sa valeur.> | <Oui ou Non> |
````

Pour le projet minimal du début de ce squelette, le tableau
Outils contient seulement `weather_status` (« Indique la disponibilité locale,
sans contacter de service externe »). Le tableau Skills contient `weather-use`. Les sections Variable de configuration
et Secret contiennent une ligne d'absence ; retirer les commandes de configuration. Ajouter les champs `endpoint` ou les hooks RAG optionnels au code impose
de réexaminer le README ; ne pas les documenter comme actifs dans le plugin minimal.


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
