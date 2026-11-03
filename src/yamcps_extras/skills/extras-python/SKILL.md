---
name: extras-python
description: "Écrire, corriger et revoir le code Python des plugins yamcps, leurs tests unittest et leurs contrôles qualité."
license: MIT
metadata:
  source: JoReci2/yamcps-extras
  effort: medium
---

# Python pour les plugins yamcps

Appliquer les conventions de développement Python du projet, préserver les contrats
publics yamcps et livrer une modification avec des preuves adaptées à son périmètre.
Une revue seule produit des constats ; une demande de correction autorise les éditions.

## Quand utiliser ce skill

- Écrire, corriger ou refactorer le code Python d’un plugin yamcps.
- Revoir son typage, ses erreurs, sa journalisation ou ses handlers async.
- Écrire des tests, migrer une suite pytest vers unittest ou adapter les contrôles qualité.

## Quand ne pas utiliser ce skill

- Concevoir les hooks, contrats, entry points ou le packaging d’un connecteur :
  **extras-develop-plugin**, `skill://extras-develop-plugin/SKILL.md` ; compléter
  avec ce guide pour l’implémentation Python.
- Créer ou modifier les workflows de livraison : **extras-configure-cicd**,
  `skill://extras-configure-cicd/SKILL.md` ; ce guide fournit les contrôles Python.
- Modifier les instructions et déclencheurs d’un skill : **extras-skill-creator**,
  `skill://extras-skill-creator/SKILL.md`.
- Configurer les consignes du client : **extras-configure-agents**,
  `skill://extras-configure-agents/SKILL.md`.

## Ressources à lire selon la tâche

| Ressource | Condition de lecture |
| --- | --- |
| [Tests et contrôles](references/testing.md) | Avant de modifier les tests, migrer pytest ou exécuter les contrôles qualité et le build |
| [Sécurité](references/security.md) | Entrées non fiables, accès sensibles, réseau, secrets, dépendances ou demande de revue de sécurité |
| [Docstrings](references/docstrings.md) | Création ou modification d’une interface publique ; exemple Google et doctest |

Depuis MCP, lire les chemins de la table avec `resources/read`, par exemple
`skill://extras-python/references/testing.md`. Les URI ne sont pas des chemins locaux. Sans édition ou exécution
locale, fournir les changements proposés et signaler les vérifications non exécutées.

## Workflow

1. **Cadrer la tâche.** Lire les consignes du projet, relever l’état Git et les
   fichiers concernés. Identifier le comportement attendu et les scénarios à
   préserver. En revue seule, ne pas modifier le code.
2. **Vérifier les contrats.** Après vérification ou création du `.venv` ci-dessous, lire `skill://extras-changelog/SKILL.md` et son
   historique. Relever Python, la plage yamcps déclarée et la version installée
   avec `.venv/bin/python -m pip show yamcps`. Pour les interfaces du moteur,
   lire **extras-develop-plugin** et son asset avant d’implémenter.
3. **Préparer l’environnement.** Vérifier le `.venv` ci-dessous et les outils
   déclarés dans le projet. Mesurer les tests concernés avant un refactoring ou
   une migration ; conserver l’échec initial comme preuve s’il reproduit le défaut.
4. **Effectuer le travail autorisé.** Appliquer les conventions ci-dessous et
   lire les références utiles. Préserver les scénarios et API hors du périmètre
   demandé ; ajouter les tests de comportement ou de régression nécessaires.
5. **Vérifier puis corriger.** Exécuter d’abord les tests concernés, puis les
   contrôles requis par le projet et affectés par la modification selon la
   référence de tests. Si un contrôle échoue, en identifier la cause, revenir
   à l’étape 4 et relancer les vérifications concernées. Zéro test collecté ne
   prouve pas la réussite d’une suite.
6. **Rendre compte.** Donner les changements, résultats observés, contrôles omis
   et limites. En revue, localiser chaque constat avec sa preuve et sa correction
   proposée. Une commande proposée n’est pas un contrôle exécuté.

## Versions et conventions locales

Cible de ce guide : Python ≥3.12 et contrats yamcps 0.4.x, dont la journalisation
0.4.1 décrite dans l’historique embarqué. Vérifier le manifeste et le runtime cible
avant d’utiliser une API ; ces versions ne constituent pas une recherche de la
dernière stable. Ne pas mettre à jour une dépendance pour un simple refactoring.

## Environnement de développement obligatoire

Utiliser exclusivement le `.venv` à la racine du projet pour les installations,
les scripts, les tests, les contrôles qualité et les builds. Réutiliser cet
environnement s’il existe ; vérifier son interpréteur avant toute installation.
Sinon, le créer avec un interpréteur Python ≥3.12 disponible :

```sh
python3 -m venv .venv
.venv/bin/python -c "import sys; from pathlib import Path; assert sys.prefix != sys.base_prefix and Path(sys.prefix).resolve() == Path('.venv').resolve()"
```

Vérifier la version avec `.venv/bin/python --version`. Installer les dépendances
requises avec `.venv/bin/python -m pip install -e '.[dev]'` si le projet déclare
cet extra ; sinon utiliser sa procédure de développement documentée.

Seule la création du `.venv` utilise le Python système. Appeler ensuite son
interpréteur explicitement, sans dépendre de l’activation du shell ou du PATH.
Sous Windows, remplacer `.venv/bin/python` par `.venv\Scripts\python.exe`.
Depuis un autre répertoire, utiliser le chemin absolu de cet interpréteur.
Ne jamais installer globalement, utiliser `pip --user`, `sudo pip` ou contourner
un `.venv` absent/invalide avec le Python système. Si sa création ou l’installation
échoue, signaler le blocage ; hors ligne, installer les wheels disponibles dans
ce même environnement avec `--no-index --find-links /chemin/wheels`.
Garder `.venv/` hors de Git et des distributions.

## Conventions

- Python ≥3.12 ; dépendance moteur `yamcps>=0.4.0,<0.5`. Respecter la configuration
  existante du plugin ; signaler les incompatibilités avant de changer ses règles.
- Suivre PEP 8 ; utiliser Ruff pour le formatage automatique et le lint, avec une
  longueur de ligne de 100 caractères. Mypy strict sur le code.
- Utiliser Radon pour analyser la complexité, Bandit pour les contrôles de sécurité
  du code. Examiner les dépendances, leurs versions et les correctifs de sécurité.
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

## Journalisation (moteur 0.4.1)

Utiliser `logging.getLogger("yamcps.connectors.<id>")`, sans handler ni changement
local de niveau ou de propagation. La CLI écrit sur stderr, en INFO ou DEBUG avec
`serve --verbose` ; l’hôte configure les logs pour l’API Python. Ne journaliser
ni valeurs de configuration, secrets, arguments/résultats d’outils, corps HTTP,
en-têtes d’authentification ni exceptions brutes, même en DEBUG. Le moteur ne
nettoie pas les traces arbitraires d’un plugin. Tester les traces ajoutées avec des
valeurs fictives et vérifier l’absence de fuite et le fonctionnement MCP stdio.
Voir la recette d’administration de `extras-develop-plugin` pour les nouvelles CLI.

## Auto-contrôle avant livraison

- [ ] Interpréteur et outils exécutés depuis le `.venv` du projet ; versions et
  dépendances compatibles avec le manifeste, sans installation globale.
- [ ] Imports publics, typage et docstrings vérifiés pour les interfaces modifiées.
- [ ] Aucun accès réseau, modèle ou index RAG chargé au démarrage ; stdout reste
  réservé au transport MCP stdio et les traces ne révèlent pas de données sensibles.
- [ ] Scénarios métier, erreurs et nettoyage préservés ; tests de régression exécutés
  quand nécessaires, aucune perte de cas lors d’une migration unittest.
- [ ] Contrôles requis exécutés sur les chemins réels ; couverture >80 % lorsqu’elle
  est mesurée, écarts et contrôles non applicables expliqués.
- [ ] Pour un changement de distribution ou de contrat MCP : découverte par entry
  point, ressources et installation wheel hors dépôt vérifiées selon la référence.

## Règles

1. Respecter les consignes et la configuration existantes ; signaler les conflits
   avant de changer les règles du projet.
2. Exécuter installations, scripts, tests et builds exclusivement dans le `.venv`.
3. Préserver les contrats publics yamcps, le démarrage paresseux et le transport stdio.
4. Utiliser des services simulés, fichiers temporaires et secrets fictifs en test.
5. Appliquer les exigences de sécurité au périmètre réel ; ne pas déclarer de
   conformité ou de contrôle réussi sans preuve.
