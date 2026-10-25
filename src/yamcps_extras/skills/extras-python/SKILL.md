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
- Suivre PEP 8 ; utiliser Ruff pour le formatage automatique et le lint, avec une
  longueur de ligne de 100 caractères. Mypy strict sur le code.
- Utiliser Radon pour analyser la complexité, Bandit pour les contrôles de sécurité
  du code et Safety pour les vulnérabilités des dépendances.
- Nommage : `snake_case` pour fonctions et variables, `PascalCase` pour classes,
  `UPPER_CASE` pour constantes et `lowercase` pour modules.
- Typer les interfaces publiques. Guides utilisateur en français selon le projet.
- Garder le plugin indépendant du dépôt moteur et des implémentations des autres
  plugins. Utiliser les imports publics yamcps et les entry points documentés.
- Aucun réseau, ingestion ou chargement de modèle à l'import, dans les factories,
  hooks ou `register()`. Garder le contexte RAG paresseux. Réserver stdout au
  transport MCP stdio ; logs sur stderr, sans credentials ni exceptions API brutes.
- Borner entrées et délais réseau ; fermer les clients. Sortir les opérations
  bloquantes des handlers async. Décrire les effets réels des outils MCP.

## Documentation

Documenter toutes les fonctions et méthodes publiques avec des docstrings en
anglais au format Google, avec `Args`, `Returns` et `Raises` lorsque pertinents.
Inclure des exemples d’utilisation lorsqu’ils clarifient le comportement.

```python
def example_function(param1: str, param2: int) -> bool:
    """Check whether text meets a minimum length.

    Args:
        param1: Text to check.
        param2: Minimum accepted length.

    Returns:
        Whether the text meets the minimum length.

    Raises:
        ValueError: If the minimum length is negative.

    Examples:
        >>> example_function("yamcps", 3)
        True
    """
    if param2 < 0:
        raise ValueError("Minimum length must be nonnegative")
    return len(param1) >= param2
```

## Sécurité — recommandations ANSSI

Appliquer les recommandations ANSSI pertinentes au périmètre du plugin et à son
exploitation. Identifier avec le responsable du projet les référentiels, versions
et exigences contractuelles applicables. Les règles Python ci-dessous constituent
une déclinaison pour yamcps des guides cités, pas un référentiel Python officiel
ANSSI. Un résultat Bandit ou Safety ne suffit pas à établir une conformité globale,
une certification ou une homologation.

### Conception et protection des données

- Identifier les données sensibles, frontières de confiance, accès métier et effets
  des outils MCP. Appliquer le moindre privilège aux comptes techniques, fichiers,
  services et permissions CI ; séparer développement, tests et production.
- Contrôler les autorisations côté service pour chaque opération sensible ; une
  annotation MCP, un corpus RAG ou un paramètre fourni par le modèle ne constitue
  pas un contrôle d’accès. Refuser par défaut une opération non autorisée.
- Valider types, tailles, formats et valeurs des entrées. Borner requêtes, réponses,
  délais et ressources consommées. Utiliser des requêtes SQL paramétrées, éviter
  `eval`/`exec` sur des données non fiables et les commandes shell interpolées.
  Refuser les chemins sortant des racines autorisées et la désérialisation non sûre.
- Pour les URL configurables, contrôler destinations et redirections selon les
  services autorisés afin de limiter les SSRF ; documenter les accès locaux requis.
- Utiliser le coffre yamcps pour les secrets, jamais des valeurs codées en dur ou
  une configuration en clair. Masquer tokens et données sensibles dans les logs,
  exceptions, réponses MCP et rapports de tests ; minimiser stockage et conservation.
- Vérifier certificats et noms d’hôte pour les connexions TLS ; ne pas désactiver
  leur validation. Utiliser les mécanismes cryptographiques éprouvés du moteur et
  des bibliothèques maintenues, sans concevoir de cryptographie propre au plugin.
- Conserver HTTP sur loopback par défaut. Pour un accès distant demandé, définir
  authentification, protection des flux et filtrage dans l’architecture de
  déploiement ; ne pas supposer que le plugin fournit ces protections.

### Dépendances, traçabilité et vérification

- Utiliser des sources de dépendances maîtrisées et des versions maintenues ;
  tracer les versions livrées et leurs dépendances, avec un inventaire ou SBOM
  selon le contexte. Analyser les changements et appliquer les correctifs de
  sécurité ; contrôler aussi la chaîne de construction et les artefacts livrés.
- Journaliser les événements de sécurité utiles (refus d’accès, erreurs de
  validation et opérations sensibles) avec un contexte permettant l’investigation,
  sans secret ni contenu métier sensible. Protéger accès, intégrité et rétention
  des journaux selon les responsabilités du plugin et de l’exploitant.
- Combiner revue humaine, Bandit, Safety et tests unittest des entrées malveillantes,
  refus d’autorisation, fuites de secrets et erreurs des services externes. Ajouter
  les tests dynamiques pertinents pour les interfaces réellement exposées.
- Consigner pour chaque exigence applicable : source/version, mesure implémentée,
  preuve de vérification et écart éventuel. Faire valider les dérogations par le
  responsable sécurité désigné et signaler les contrôles manquants. Ne déclarer
  une conformité que pour un périmètre évalué avec des preuves explicites.

Références ANSSI :

- [Guide d’hygiène informatique](https://messervices.cyber.gouv.fr/guides/guide-dhygiene-informatique) : socle de protection et suivi des mesures.
- [Guide de cybersécurité à l’usage des start-up du numérique](https://messervices.cyber.gouv.fr/documents-guides/guide_cybersecurite_start-up_numerique_FR_v1.pdf) : conception sécurisée, chaîne d’intégration, SAST, dépendances/SBOM et gestion des secrets.

## Tests et contrôles

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
- Exécuter toute la suite avec `python -m unittest discover -s tests -p 'test_*.py'`
  et comparer les scénarios et la couverture à l’état initial. Ne pas considérer
  un succès unittest comme suffisant si des fonctions pytest restent non collectées.

Adapter les commandes aux chemins et au module réels du plugin :

```sh
ruff format --check src tests
ruff check src tests
mypy src
radon cc src -s -a
bandit -r src
safety scan
coverage run --source=<module_plugin> -m unittest discover -s tests -p 'test_*.py'
coverage report --show-missing --fail-under=81
python -m build
```

Pour appliquer le formatage automatique, utiliser `ruff format src tests`, puis
les contrôles ci-dessus. Déclarer Ruff, mypy, Radon, Bandit, Safety et coverage
parmi les outils de développement du plugin s’ils ne sont pas déjà fournis.

Exécuter `safety scan` depuis la racine du plugin ; vérifier sa disponibilité et
les prérequis d’authentification de la version installée. Si l’accès au service ou
l’authentification manque, signaler le contrôle non exécuté sans le déclarer réussi.
Examiner les vulnérabilités et documenter les exceptions justifiées.
Référence : [commandes Safety](https://docs.safetycli.com/safety-docs/safety-cli/scanning-for-vulnerable-and-malicious-packages/available-commands-and-inputs).

Après migration, mesurer la couverture sur toute la suite unittest avec les
commandes ci-dessus. Exiger une couverture >80 % sans régression des scénarios
couverts ; examiner Radon sans inventer
un seuil bloquant et justifier les exceptions Bandit. Vérifier découverte par
entry point, lecture des skills et installation wheel hors du dépôt. Pour HTTP,
utiliser seulement un port loopback de test. Rapporter les contrôles exécutés et
les limites ; ne pas déclarer un contrôle réussi sans résultat.
