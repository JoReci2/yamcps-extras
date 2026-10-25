# GitHub Actions

Cible : `.github/workflows/<nom>.yaml`. Préserver les workflows existants.

- Qualité sur pull request et push vers les branches retenues. Déclarer
  `permissions: contents: read` ; aucune permission d’écriture globale.
- Checkout, setup Python ≥3.12, installation du plugin avec ses dépendances dev,
  puis commandes Ruff, mypy, Radon, Bandit, Safety, tests/couverture et build du projet.
- Pour hatch-vcs, récupérer historique et tags (`fetch-depth: 0`). Utiliser les
  actions de transfert d’artefacts pour conserver rapports et distributions.
- Si publication PyPI demandée, job distinct après validation sur release/tag
  retenu ; environnement protégé et Trusted Publisher PyPI. `id-token: write`
  uniquement pour ce job. Ne pas reconstruire les archives après validation.
- Livraison basée sur tag : pour un push de tag `v*`, lire `github.ref_name`
  après vérification de `github.ref_type == 'tag'` ; pour une release publiée,
  lire `github.event.release.tag_name`. Passer cette valeur par une variable
  d’environnement, valider puis checkout de `refs/tags/<tag>` avec historique.
  Appliquer la section « Construire depuis le tag de version » du skill : version
  Python normalisée et, si demandée, image portant le tag Git exact. Transférer
  l’image validée par artefact/digest au job de publication sans reconstruction.
- Vérifier versions et paramètres des actions officielles au moment de génération.
  Ne jamais exécuter du code de PR non fiable avec les credentials de publication.

Sources : [syntaxe GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax),
[Trusted Publishers PyPI](https://docs.pypi.org/trusted-publishers/).

Référence : [contextes GitHub](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts).
