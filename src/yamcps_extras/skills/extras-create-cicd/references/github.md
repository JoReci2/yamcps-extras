# GitHub Actions

Cible : `.github/workflows/<nom>.yaml`. Préserver les workflows existants.

- Qualité sur pull request et push vers les branches retenues. Déclarer
  `permissions: contents: read` ; aucune permission d’écriture globale.
- Checkout, setup Python ≥3.12, installation du plugin avec ses dépendances dev,
  puis commandes Ruff, mypy, Radon, Bandit, tests/couverture et build du projet.
- Pour hatch-vcs, récupérer historique et tags (`fetch-depth: 0`). Utiliser les
  actions de transfert d’artefacts pour conserver rapports et distributions.
- Si publication PyPI demandée, job distinct après validation sur release/tag
  retenu ; environnement protégé et Trusted Publisher PyPI. `id-token: write`
  uniquement pour ce job. Ne pas reconstruire les archives après validation.
- Vérifier versions et paramètres des actions officielles au moment de génération.
  Ne jamais exécuter du code de PR non fiable avec les credentials de publication.

Sources : [syntaxe GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax),
[Trusted Publishers PyPI](https://docs.pypi.org/trusted-publishers/).
