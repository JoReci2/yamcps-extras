# GitLab CI

Cible : `.gitlab-ci.yml`, ou fichiers inclus selon la structure existante.

- Choisir une image Python ≥3.12 et confirmer le type de runner. Structurer les
  étapes qualité/tests/build avec `rules` pour les branches et merge requests
  retenues ; éviter les pipelines doublonnés selon la configuration existante.
- Installer les dépendances dev réelles, exécuter Ruff, mypy, Radon, Bandit et
  tests/couverture. Conserver rapports et wheel/sdist avec `artifacts`.
- Pour hatch-vcs, désactiver la profondeur limitée (`GIT_DEPTH: "0"`) et vérifier
  la disponibilité des tags. Utiliser `needs`/artefacts pour transmettre les
  archives validées au job de livraison sans reconstruire.
- Si publication demandée, choisir PyPI ou registre GitLab avec l’utilisateur.
  Restreindre le job aux tags et environnements autorisés. Préférer une identité
  fédérée lorsque le registre la prend en charge ; sinon variables CI protégées
  et masquées. Ne pas inventer de support OIDC ni mettre un token dans le YAML.

Sources : [syntaxe GitLab CI](https://docs.gitlab.com/ci/yaml/),
[registre Python GitLab](https://docs.gitlab.com/user/packages/pypi_repository/),
[Trusted Publishers PyPI](https://docs.pypi.org/trusted-publishers/).

Pour une livraison, utiliser `rules: if: $CI_COMMIT_TAG` puis valider le tag `v*`
selon la référence `references/release.md` nommée dans le skill. La variable
`CI_COMMIT_TAG` est la source de version ; ne pas utiliser `CI_COMMIT_REF_SLUG`,
qui transforme la référence. Vérifier que le checkout correspond au tag et à
`CI_COMMIT_SHA`. Si une image est demandée, son tag est exactement
`$CI_COMMIT_TAG`, préfixe `v` inclus ; conserver son digest pour la publication.

Référence : [variables prédéfinies GitLab](https://docs.gitlab.com/ci/variables/predefined_variables/).

## Validation avant livraison

Utiliser CI Lint avec les includes et variables nécessaires lorsque l’instance
est accessible. Sans cet accès, signaler la limite : un parseur YAML local ne
résout pas les includes ni les règles du pipeline. Vérifier la disponibilité
des artefacts dans les jobs déclarant `needs`.

Créer le `.venv` dans chaque job/agent Python puis utiliser `.venv/bin/python`
(ou `.venv\Scripts\python.exe` sous Windows), sans activation implicite.

Validation : [CI Lint](https://docs.gitlab.com/ci/yaml/lint/). Source consultée le 3 novembre 2026 ; vérifier aussi
la version de la plateforme ou des plugins réellement disponibles sur la cible.
