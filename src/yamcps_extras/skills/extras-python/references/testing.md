# Tests, migration unittest et contrôles

Écrire des tests pour toute nouvelle fonctionnalité et des tests de régression
pour les corrections. Utiliser `unittest.TestCase` ou
`unittest.IsolatedAsyncioTestCase`, dans `test_*.py`. Si des tests pytest existent,
les remplacer par des tests unittest en préservant tous les scénarios, assertions,
cas paramétrés et comportements de nettoyage. Simuler les services externes,
utiliser des répertoires temporaires et des secrets fictifs.
Tester les cas métier, erreurs et intégrations MCP utiles ; aucune production.

Pour migrer une suite pytest :

- Relever les tests et cas paramétrés collectés, leurs résultats et la couverture
  avant migration afin de comparer les comportements couverts.
- Convertir les fonctions en méthodes de `unittest.TestCase` et les tests async en
  méthodes de `unittest.IsolatedAsyncioTestCase`. Remplacer les fixtures par
  `setUp`/`tearDown`, `asyncSetUp`/`asyncTearDown` et les mécanismes de nettoyage
  unittest ; utiliser `unittest.mock` et `tempfile` pour les substituts usuels.
- Convertir les assertions et `pytest.raises` en assertions unittest et
  `assertRaises` ; conserver les cas paramétrés avec `subTest` ou des méthodes
  distinctes. Préserver les conditions de skip et les échecs attendus.
- Mettre à jour commandes, documentation et CI pour utiliser le runner standard.
  Retirer pytest, pytest-asyncio et les autres extensions pytest devenues inutiles
  des dépendances et configurations après vérification de leurs usages.
- Exécuter toute la suite avec `.venv/bin/python -m unittest discover -s tests -p 'test_*.py'`
  et comparer les scénarios et la couverture à l’état initial. Ne pas considérer
  un succès unittest comme suffisant si des fonctions pytest restent non collectées.

Exécuter depuis la racine du projet. Adapter les chemins et remplacer la valeur
de `PLUGIN_MODULE` par le module importable réel du plugin :

```sh
PLUGIN_MODULE=nom_du_module
.venv/bin/python -m ruff format --check src tests
.venv/bin/python -m ruff check src tests
.venv/bin/python -m mypy src
.venv/bin/python -m radon cc src -s -a
.venv/bin/python -m bandit -r src
.venv/bin/python -m coverage run --source="$PLUGIN_MODULE" -m unittest discover -s tests -p 'test_*.py'
.venv/bin/python -m coverage report --show-missing --fail-under=81
.venv/bin/python -m build
```

Pour appliquer le formatage automatique, utiliser `.venv/bin/python -m ruff format src tests`, puis
les contrôles ci-dessus. Déclarer Ruff, mypy, Radon, Bandit et coverage
parmi les outils de développement du plugin s’ils ne sont pas déjà fournis.

Après migration, mesurer la couverture sur toute la suite unittest avec les
commandes ci-dessus. Exiger une couverture >80 % sans régression des scénarios
couverts ; examiner Radon sans inventer
un seuil bloquant et justifier les exceptions Bandit. Vérifier découverte par
entry point, lecture des skills et installation wheel hors du dépôt. Pour HTTP,
utiliser seulement un port loopback de test. Rapporter les contrôles exécutés et
les limites ; ne pas déclarer un contrôle réussi sans résultat.
