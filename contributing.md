# Contribuer à yamcps-extras

Python ≥ 3.12, yamcps ≥ 0.3, < 0.4. Installer d'abord le moteur depuis sa distribution,
son wheel ou, pour travailler sur les deux dépôts, `python -m pip install -e ../yamcps`.
Depuis la racine de ce dépôt dans un environnement activé :

```sh
python -m pip install -e '.[dev]'
ruff format --check src tests
ruff check src tests
mypy src
radon cc src -s -a
bandit -r src
coverage run --source=yamcps_extras -m pytest -q
coverage report --show-missing --fail-under=81
python -m unittest discover -s tests -p 'test_*.py'
python -m build
```

Les sources et les tests de ce dépôt ne nécessitent pas le dépôt source du moteur.
Le moteur est une dépendance Python installée. Sur poste hors ligne, fournir les
wheels de toutes les dépendances, dont `hatchling`, `hatch-vcs` et `editables` pour le mode
editable ; utiliser `--no-index --find-links /chemin/wheels` et construire avec
`python -m build --no-isolation` après installation des outils.

Suivre PEP 8 (100 caractères), typer les interfaces publiques, documenter en anglais
au format Google ; guides en français. Utiliser unittest pour les nouveaux tests,
conserver les tests existants et simuler les API. Garder stdout pour MCP stdio,
les secrets hors des logs, et aucun appel réseau à l'import ou à l'enregistrement.
Tester une installation wheel hors du dépôt, sans PYTHONPATH vers ses sources.
Conserver une couverture >80 %, examiner Radon/Bandit et signaler les limites.
Ne pas publier sur PyPI ni déclencher une release sans demande explicite.

Le test de coexistence Extras/Docs est optionnel sans `yamcps-docs` installé.
Installer le wheel de Docs pour vérifier aussi cette intégration croisée.

## Compatibilité yamcps 0.3.0

Le contrat du connecteur de skills (`id`, `register`, `skill_roots`) est conservé.
Le guide et son projet exemple ciblent désormais la série 0.3 ; la recette RAG
couvre aussi `RetrievalIndex`, `index_factory` et `source_namespace`.

Validation du 24 octobre 2026 : 11 tests réussis, un test optionnel Docs ignoré,
couverture du connecteur à 100 %, transports mémoire/stdio/HTTP local et wheel
installé testé hors du dépôt. Ruff, mypy, Bandit, Radon et build wheel/sdist passent.
Un test exécute directement la nouvelle recette de backend et vérifie sa
coexistence avec les ressources Extras et les citations `weather://source/...`.

L'index pip accessible ne proposait encore que les versions 0.1.0 et 0.2.0.
Le moteur testé a été construit localement avec la version 0.3.0 depuis le commit
`57ebae7`, dont les sources exécutables et le manifeste sont identiques au tag
[`v0.3.0`](https://github.com/JoReci2/yamcps/releases/tag/v0.3.0)
(`1f13e720ac46b3c0f2f5c442c2d875c6c5b5ee77`) : seuls README et CONTRIBUTING diffèrent.
Cela vérifie le code de la release, pas le wheel publié sur PyPI.

## Publication sur PyPI

Le workflow `.github/workflows/workflow.yaml` construit et publie uniquement
`yamcps-extras` à la publication d’une release GitHub. Il ne se déclenche pas
sur un push ou une pull request. Le commit doit appartenir à l’historique de
`main`. Les contrôles de développement restent exécutés en local.

Configurer le Trusted Publisher du projet PyPI `yamcps-extras` : propriétaire
GitHub `JoReci2`, dépôt `yamcps-extras`, workflow `workflow.yaml`, environnement
`pypi`. Créer aussi cet environnement dans les paramètres du dépôt GitHub.
L’authentification utilise OIDC, sans token PyPI ; seul le job de publication
reçoit la permission `id-token: write`.

Après validation et intégration sur `main`, créer un tag `v<version>` sur le
commit correspondant, par exemple `v0.1.0`. La version est calculée depuis Git
par `hatch-vcs`, comme pour yamcps : aucune modification de version dans
`pyproject.toml` n’est nécessaire. Les builds depuis Git nécessitent les tags et
l’historique complet. Entre deux tags ou avec des modifications locales, la
version de développement est refusée par le vérificateur de release. Le sdist
permet de reconstruire le wheel sans Git grâce à ses métadonnées.
Avant de pousser le tag et de publier la release, vérifier depuis son checkout
propre, avec un dossier de sortie vide :

```sh
python -m pip install build twine
python -m build --outdir dist/release .
python .github/workflows/verify_release.py dist/release --tag v0.1.0
python -m twine check --strict dist/release/*
```

Adapter le tag à la version choisie. La vérification exige exactement un wheel
et un sdist dont les métadonnées déclarent `yamcps-extras` et la version du tag.
Les deux archives validées sont transmises au job de publication. Les versions
PyPI sont immuables : augmenter la version pour chaque nouvelle publication.
La configuration du workflow ne déclenche aucune release ni publication.
