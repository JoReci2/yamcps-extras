# yamcps-extras

## Description

Deux skills de développement et leurs modèles, servis comme ressources MCP.
Aucun outil, prompt, appel réseau ou secret ajouté. Le serveur ne modifie pas les
fichiers du client. Voir [contributing.md](contributing.md) pour les contrôles et
[MIGRATION.md](MIGRATION.md) pour l'extraction du dépôt moteur.

## Quickstart

Python ≥ 3.12 et moteur yamcps compatible requis. Depuis ce dépôt, dans un
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

## Outils

| Outil | Description |
| --- | --- |
| Aucun | — |

## Skills

| Skill | Description |
| --- | --- |
| [extras-configure-agents](src/yamcps_extras/skills/extras-configure-agents/SKILL.md) | Découverte locale, questionnaire, usages MCP, validation et protection des consignes existantes |
| [extras-develop-plugin](src/yamcps_extras/skills/extras-develop-plugin/SKILL.md) | Contrat public, projet autonome, tests, packaging et README uniforme d'un plugin |

## Variable de configuration

| Variable | Nom du champ | Description | Obligatoire | Valeur par défaut |
| --- | --- | --- | --- | --- |
| Aucune | — | — | — | — |

## Secret

| Secret | Nom du champ | Description | Obligatoire |
| --- | --- | --- | --- |
| Aucun | — | — | — |
