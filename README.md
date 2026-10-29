# yamcps-extras

## Description

Cinq skills dédiés au développement de plugins yamcps et leurs références, servis comme ressources MCP.
Aucun outil, prompt, appel réseau ou secret ajouté. Le serveur ne modifie pas les
fichiers du client. Voir [contributing.md](contributing.md) pour les contrôles.

## Quickstart

Python ≥ 3.12 et yamcps ≥ 0.4.0, < 0.5 requis. Depuis ce dépôt, dans un
environnement activé :

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -e .
yamcps connectors list
yamcps serve --connector extras
```

L’installation de `yamcps-extras` installe automatiquement `yamcps[dev]`, y compris
les outils de développement du moteur. L’extra `yamcps-extras[dev]` ajoute les
outils de contribution propres à ce dépôt.

Commencer par `skill://extras-configure-agents/SKILL.md`, puis son modèle via
`resources/read`, pour créer le fichier de consignes reconnu par le client
(`AGENTS.md` par défaut, ou le nom existant pris en charge). Ce fichier devient
le point d’entrée des tâches suivantes : il route vers les quatre skills métier,
sans devoir relancer la configuration de l’agent à chaque demande.
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
Les skills utiles se cumulent selon la tâche ; une ressource déjà lue et toujours
à jour n’a pas besoin d’être rechargée dans la même tâche. Ces consignes sont
interprétées par le client agent : le plugin n’exécute pas le routage à sa place.
La création ou modification de workflow demande GitHub Actions, GitLab CI ou Jenkins ; la livraison
reste optionnelle. L’historique embarqué concerne le moteur, pas le changelog du plugin.

Le nom du skill CI/CD est désormais `extras-configure-cicd` (anciennement
`extras-create-cicd`). Mettre à jour les URI des fichiers de consignes déjà générés
et redémarrer le serveur après mise à jour du plugin ; l’ancienne URI n’est plus exposée.

## Outils

| Outil | Description |
| --- | --- |
| Aucun | — |

## Skills

| Skill | Description |
| --- | --- |
| [extras-configure-agents](src/yamcps_extras/skills/extras-configure-agents/SKILL.md) | Découverte locale, questionnaire, usages MCP, validation et protection des consignes existantes |
| [extras-develop-plugin](src/yamcps_extras/skills/extras-develop-plugin/SKILL.md) | Contrat public, projet autonome, tests, packaging et README uniforme d'un plugin |
| [extras-configure-cicd](src/yamcps_extras/skills/extras-configure-cicd/SKILL.md) | CI/CD de plugin pour GitHub Actions, GitLab CI ou Jenkins |
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
