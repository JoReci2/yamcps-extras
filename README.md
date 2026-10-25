# yamcps-extras

## Description

Cinq skills dédiés au développement de plugins yamcps et leurs références, servis comme ressources MCP.
Aucun outil, prompt, appel réseau ou secret ajouté. Le serveur ne modifie pas les
fichiers du client. Voir [contributing.md](contributing.md) pour les contrôles.

## Quickstart

Python ≥ 3.12 et yamcps ≥ 0.4.0, < 0.5 requis. Depuis ce dépôt, dans un
environnement activé :

```sh
python -m pip install -e .
yamcps connectors list
yamcps serve --connector extras
```

Lire `skill://extras-configure-agents/SKILL.md` ou
`skill://extras-develop-plugin/SKILL.md`, puis leurs assets via `resources/read`.
Les clients compatibles peuvent découvrir les guides par `skills/list` et
`skills/get` ; leur affichage dépend du client. Ils ne sont pas installés dans
son système de fichiers. Le client doit disposer de ses propres outils d'édition
et d'exécution. Redémarrer le serveur après modification d'un skill.

Le guide de configuration protège les fichiers existants et exige la validation
du contenu/diff avant écriture. Le guide de développement fournit le contrat et
un projet autonome complet sans accès au dépôt moteur. Les modèles sont servis
à `skill://extras-configure-agents/assets/AGENTS.template.md` et
`skill://extras-develop-plugin/assets/plugin-template.md`.

Le modèle `AGENTS.md` impose la consultation du changelog moteur avant toute
modification, puis charge les guides Python, développement ou CI/CD selon la tâche.
La création de workflow demande GitHub Actions, GitLab CI ou Jenkins ; la livraison
reste optionnelle. L’historique embarqué concerne le moteur, pas le changelog du plugin.

## Outils

| Outil | Description |
| --- | --- |
| Aucun | — |

## Skills

| Skill | Description |
| --- | --- |
| [extras-configure-agents](src/yamcps_extras/skills/extras-configure-agents/SKILL.md) | Découverte locale, questionnaire, usages MCP, validation et protection des consignes existantes |
| [extras-develop-plugin](src/yamcps_extras/skills/extras-develop-plugin/SKILL.md) | Contrat public, projet autonome, tests, packaging et README uniforme d'un plugin |
| [extras-create-cicd](src/yamcps_extras/skills/extras-create-cicd/SKILL.md) | CI/CD de plugin pour GitHub Actions, GitLab CI ou Jenkins |
| [extras-changelog](src/yamcps_extras/skills/extras-changelog/SKILL.md) | Historique du moteur par version, à consulter avant toute modification |
| [extras-python](src/yamcps_extras/skills/extras-python/SKILL.md) | Conventions Python, tests et qualité propres aux plugins yamcps |

## Variable de configuration

| Variable | Nom du champ | Description | Obligatoire | Valeur par défaut |
| --- | --- | --- | --- | --- |
| Aucune | — | — | — | — |

## Secret

| Secret | Nom du champ | Description | Obligatoire |
| --- | --- | --- | --- |
| Aucun | — | — | — |
