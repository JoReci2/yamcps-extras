# Contribuer à yamcps-extras

Python ≥ 3.12. Installer d'abord un moteur yamcps compatible depuis sa distribution,
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
wheels de toutes les dépendances, dont `hatchling` et `editables` pour le mode
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

Après validation et intégration sur `main`, mettre à jour `project.version`
dans `pyproject.toml`, puis créer un tag `v<version>` sur le commit correspondant.
La version est déclarée explicitement, elle n’est pas calculée depuis Git.
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
