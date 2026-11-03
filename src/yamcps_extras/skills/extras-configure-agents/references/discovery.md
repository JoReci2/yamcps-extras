# Découverte et questionnaire du projet

Lire avant de rédiger ou fusionner les consignes. Les faits déjà observés ou
confirmés ne nécessitent pas de nouvelle question. La découverte reste en lecture
seule et limitée aux sources autorisées.

## Découverte locale

Établir les faits disponibles avant de questionner l'utilisateur :

- Racine, branche et état du projet si Git est présent, structure utile et fichiers
  de consignes applicables ; ne pas exiger Git si le projet n'en utilise pas.
- README, manifestes (`pyproject.toml`, `package.json` ou équivalents), dépendances,
  documentation, configuration CI, tests et scripts de contribution présents.
- Finalité observable, langages et versions, architecture, conventions, commandes
  d'installation/build/test/qualité, contraintes de packaging et de livraison.
- Configuration MCP déclarée par le projet ou visible dans le client, noms de
  serveurs et plugins, ressources/skills et outils effectivement accessibles.
  Ne pas afficher les credentials des configurations et ne pas importer un plugin
  pour le découvrir : imports et factories peuvent exécuter du code.

Utiliser en priorité `rg --files` et `rg` si disponibles, avec des recherches ciblées.
Inspecter les fichiers de consignes nommés même s'ils ne figurent pas dans une
recherche par défaut. Confirmer que le projet développe un plugin yamcps, ou que
l’utilisateur souhaite en créer un, avant de générer ses consignes. Relever
seulement les capacités présentes
(configs, vault, RAG, skills) ; leur fonctionnement peut être obtenu depuis le
skill `extras-develop-plugin` s'il est exposé, sans exiger les sources du moteur.

Préparer un relevé court : fait, source consultée, incertitude éventuelle. Séparer
faits observés, propositions et décisions déjà confirmées ; une absence d'accès
ne prouve pas l'absence d'une fonctionnalité.

## Questionnaire du projet

Présenter d'abord les informations découvertes, puis demander uniquement ce qui
manque ou nécessite une décision. Regrouper les questions par thème et laisser
l'utilisateur corriger les déductions. Ne pas transformer le questionnaire en
liste obligatoire si les réponses sont déjà établies.

### Contexte général

Clarifier objectif du projet, utilisateurs, livrables, périmètre de travail de
l'agent et exclusions. Distinguer projet neuf, maintenance et migration.

### Environnement et méthode de travail

Confirmer les inconnues utiles : environnements local/test/production, accès
réseau ou hors ligne, langages/versions, contraintes d'installation, conventions
de code/documentation, tests attendus, couverture et workflow de branches/PR.
Reprendre le seuil >80 % et le runner unittest du skill Python ; relever les
écarts existants et les exceptions explicites du projet sans inventer de commande.
La création des consignes seule ne lance pas la migration de la suite.

### Sécurité, sources et autonomie

Préciser les données autorisées, chemins protégés, opérations permises et actions
soumises à accord. Identifier les référentiels faisant autorité et la conduite
à tenir en cas de contradiction ou d'information périmée. Ne pas décider à la
place de l'utilisateur qu'un corpus RAG prévaut sur une observation d'outil.

### Capacités MCP

Lire `references/mcp-inventory.md`, directement nommé dans le guide principal,
pour inventorier serveurs, skills, outils et RAG sans appeler les outils métier.
Reprendre uniquement les usages établis dans le tableau du modèle ; faire décider
les usages nouveaux ou les droits encore inconnus, sans demander de secret.

### Livraison et arbitrages restants

Confirmer nom/emplacement du fichier, langue, format du compte rendu, validations
requises et rôle de l'utilisateur dans les décisions encore ouvertes. Préférer
les conventions déjà observées pour les choix faciles à modifier.

