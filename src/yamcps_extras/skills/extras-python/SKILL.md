---
name: extras-python
description: Appliquer les conventions Python des plugins yamcps 0.4.0 lors de la création, modification ou revue de leur code, tests et configuration qualité.
---

# Python pour les plugins yamcps

Avant toute modification, consulter `skill://extras-changelog/SKILL.md`.
Pour les interfaces du moteur et le projet autonome, lire
`skill://extras-develop-plugin/SKILL.md` et son asset. Ces URI sont des ressources
MCP à lire avec `resources/read`, pas des chemins locaux.

## Conventions

- Python ≥3.12 ; dépendance moteur `yamcps>=0.4.0,<0.5`. Respecter la configuration
  existante du plugin ; signaler les incompatibilités avant de changer ses règles.
- PEP 8, Ruff à 100 caractères ; snake_case pour fonctions et variables,
  PascalCase pour classes, UPPER_CASE pour constantes. Mypy strict sur le code.
- Typer les interfaces publiques ; docstrings Google en anglais avec Args,
  Returns et Raises si pertinents. Guides utilisateur en français selon le projet.
- Garder le plugin indépendant du dépôt moteur et des implémentations des autres
  plugins. Utiliser les imports publics yamcps et les entry points documentés.
- Aucun réseau, ingestion ou chargement de modèle à l'import, dans les factories,
  hooks ou `register()`. Garder le contexte RAG paresseux. Réserver stdout au
  transport MCP stdio ; logs sur stderr, sans credentials ni exceptions API brutes.
- Borner entrées et délais réseau ; fermer les clients. Sortir les opérations
  bloquantes des handlers async. Décrire les effets réels des outils MCP.

## Tests et contrôles

Écrire les nouveaux tests avec `unittest.TestCase` ou
`unittest.IsolatedAsyncioTestCase`, dans `test_*.py`. Préserver la suite pytest
existante : le runner unittest seul ne collecte pas ses fonctions. Simuler les
services externes, utiliser des répertoires temporaires et des secrets fictifs.
Tester les cas métier, erreurs et intégrations MCP utiles ; aucune production.

Adapter les commandes aux chemins et au module réels du plugin :

```sh
ruff format --check src tests
ruff check src tests
mypy src
radon cc src -s -a
bandit -r src
coverage run --source=<module_plugin> -m unittest discover -s tests -p 'test_*.py'
coverage report --show-missing --fail-under=81
python -m build
```

Si des tests pytest existent, mesurer la couverture sur la suite complète avec
`coverage run --source=<module_plugin> -m pytest -q` et exécuter aussi les nouveaux
tests avec unittest. Exiger une couverture >80 % ; examiner Radon sans inventer
un seuil bloquant et justifier les exceptions Bandit. Vérifier découverte par
entry point, lecture des skills et installation wheel hors du dépôt. Pour HTTP,
utiliser seulement un port loopback de test. Rapporter les contrôles exécutés et
les limites ; ne pas déclarer un contrôle réussi sans résultat.
