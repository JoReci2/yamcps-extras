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
- Livraison basée sur tag : pour un push de tag `v*`, lire `github.ref_name`
  après vérification de `github.ref_type == 'tag'` ; pour une release publiée,
  lire `github.event.release.tag_name`. Passer cette valeur par une variable
  d’environnement, valider puis checkout de `refs/tags/<tag>` avec historique.
  Appliquer la référence `references/release.md` nommée dans le skill : version
  Python normalisée et, si demandée, image portant le tag Git exact. Transférer
  l’image validée par artefact/digest au job de publication sans reconstruction.
- Vérifier versions et paramètres des actions officielles au moment de génération.
  Ne jamais exécuter du code de PR non fiable avec les credentials de publication.

Sources : [syntaxe GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax),
[Trusted Publishers PyPI](https://docs.pypi.org/trusted-publishers/).

Référence : [contextes GitHub](https://docs.github.com/en/actions/reference/workflows-and-actions/contexts).

## Validation avant livraison

Vérifier la syntaxe et les expressions avec actionlint s’il est disponible ;
sinon signaler cette validation omise. Confirmer les entrées des actions utilisées
dans leur documentation officielle. Une validation statique ne prouve pas que
le runner dispose des accès ni que les jobs distants ont réussi.

Créer le `.venv` dans chaque job/agent Python puis utiliser `.venv/bin/python`
(ou `.venv\Scripts\python.exe` sous Windows), sans activation implicite.

Validation : [actionlint](https://github.com/rhysd/actionlint). Source consultée le 3 novembre 2026 ; vérifier aussi
la version de la plateforme ou des plugins réellement disponibles sur la cible.
