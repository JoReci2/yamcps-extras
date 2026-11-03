---
name: extras-develop-plugin
description: "Créer ou faire évoluer un connecteur yamcps autonome : contrats, configuration, secrets, RAG et distribution."
license: MIT
metadata:
  source: JoReci2/yamcps-extras
  effort: high
---

# Développer un plugin yamcps autonome

Créer ou faire évoluer un plugin installable avec le moteur distribué, sans
nécessiter le clone de yamcps ni le code d’un autre plugin. Respecter les consignes
et l’architecture du projet existant ; pour une création, partir du projet minimal.
Une revue seule produit des constats, sans modifier le plugin.

## Quand utiliser ce skill

- Créer un connecteur métier ou un plugin ne servant que des skills.
- Ajouter ou modifier les hooks de configuration, secrets, RAG et catalogue.
- Vérifier découverte par entry point, composition MCP, packaging et installation.
- Aligner le README sur les capacités effectivement distribuées.

## Quand ne pas utiliser ce skill

- Corriger seulement le code, le typage ou les tests Python sans changer le contrat
  du plugin : **extras-python**, `skill://extras-python/SKILL.md`.
- Créer ou modifier un workflow CI/CD : **extras-configure-cicd**,
  `skill://extras-configure-cicd/SKILL.md`.
- Rédiger ou revoir les instructions d’un skill : **extras-skill-creator**,
  `skill://extras-skill-creator/SKILL.md` ; revenir ici pour sa distribution MCP.
- Configurer les consignes du client : **extras-configure-agents**,
  `skill://extras-configure-agents/SKILL.md`.

## Ressources et conditions de lecture

| Ressource | Quand la lire |
| --- | --- |
| [Contrats et nommage](references/contracts.md) | Avant de modifier les interfaces, versions, identifiants, hooks ou déclarations du plugin |
| [Projet minimal et recettes](assets/plugin-template.md) | Projet minimal pour une création ; recette concernée pour une évolution ; validation pour la livraison |
| [Contrat du README](references/readme.md) | Avant de créer ou adapter le README ; modèle copiable dans l’asset |

Depuis MCP, lire ces chemins avec `resources/read` sous le nom du skill, par
exemple `skill://extras-develop-plugin/assets/plugin-template.md`. Les liens
relatifs désignent les fichiers servis, pas une installation locale du plugin.
Les clients compatibles peuvent découvrir les fichiers via `skills/list` et
`skills/get`, puis lire leur contenu ; ne pas supposer ces méthodes universelles.

Le serveur fournit des instructions en lecture. Sans écriture ou exécution locale,
livrer les fichiers et commandes à appliquer, sans prétendre les avoir créés,
testés ou installés. Un client distant n’installe pas le plugin sur le serveur.

## Versions cibles et prérequis

Les recettes ciblent yamcps 0.4.1, Python ≥3.12 et `mcp>=2.3,<3`.
Pour une création avec ces recettes, déclarer `yamcps>=0.4.1,<0.5` ; un plugin
existant limité aux contrats 0.4.0 peut conserver son minimum. Les commandes
et paramètres propres à 0.4.1 exigent cette version sur la machine de l’opérateur.
Ces versions sont des cibles de compatibilité, pas une affirmation sur la dernière
stable. Vérifier le manifeste et les distributions installées avant de les utiliser.

Lire `skill://extras-changelog/SKILL.md` et son historique avant toute modification.
Appliquer le `.venv` obligatoire d’**extras-python** pour installations, scripts,
tests et builds : `.venv/bin/python` (Windows : `.venv\Scripts\python.exe`).
Réserver le Python système à sa création. Vérifier aussi la version sur le serveur
cible ; sans accès, demander cette vérification à son opérateur et signaler la limite.
Un wheel fourni par l’administrateur suffit ; sans capacité disponible, conserver
le contrat minimal plutôt qu’inventer une API ou un package RAG séparé.

## Workflow

1. **Cadrer.** Identifier création, évolution ou revue ; relever consignes, état
   Git et fichiers concernés. Définir opérations, entrées/sorties, accès métier,
   effets et scénarios à préserver. Sans information indispensable, suspendre
   seulement la partie dépendante ; retenir une hypothèse explicite pour un choix
   réversible. Ne pas renommer implicitement un plugin existant.
2. **Vérifier le contrat.** Lire la référence de contrats et relever versions
   déclarées/installées. Choisir seulement les capacités nécessaires : outils,
   prompts, ressources, configurations, secrets, RAG ou skills. Pour un changement
   existant, exécuter les tests concernés avant l’édition si possible.
3. **Préparer les fichiers.** Pour une création, copier les fichiers du projet
   minimal dans l’espace de travail autorisé et adapter ensemble distribution,
   module, identifiant, entry point, handlers, skills, clés et commandes.
   Pour une évolution, préserver les autres fichiers et préparer les migrations
   de noms/configurations avant tout retrait. Ne pas importer un autre plugin.
4. **Implémenter.** Charger **extras-python** pour le code et ses contrôles.
   Appliquer seulement les recettes utiles de l’asset selon la table ci-dessous.
   En revue seule, comparer le code aux contrats et localiser les constats.
5. **Documenter.** Appliquer la référence README et son modèle ; inventorier
   exclusivement les outils, skills, configurations et secrets implémentés.
   Préserver les informations utiles du README existant dans les sections prévues
   ou des guides liés. Charger **extras-configure-cicd** si la tâche inclut la CI.
6. **Valider et corriger.** Exécuter la procédure de validation de l’asset : entry
   point, tests unittest/MCP mémoire et stdio, contrôles Python, couverture >80 %,
   wheel/sdist et installation du wheel hors sources sans PYTHONPATH vers le projet.
   Tester HTTP sur loopback si ce transport est concerné, ainsi que collisions,
   erreurs et régressions pertinentes. En cas d’échec, identifier sa cause, revenir
   à l’étape 3 ou 4, puis relancer les contrôles affectés. Ne pas compter zéro test
   collecté comme un succès ; signaler tout contrôle impossible.
7. **Livrer.** Donner fichiers, artefacts construits et résultats observés,
   commandes d’installation et étapes restantes côté serveur. L’administrateur
   installe le wheel dans le runtime du serveur puis redémarre celui-ci dans le
   périmètre autorisé. Distinguer validation locale, installation distante et
   publication ; ne pas publier sur PyPI sans demande correspondante.

## Choisir les recettes de l’asset

| Besoin | Section à lire et contrainte décisive |
| --- | --- |
| Plugin minimal | Projet minimal complet ; `id` et `register()` synchrones, entry point sans argument |
| Skills seuls | Projet minimal complet ; retirer le handler, garder `register()` vide et adapter les tests |
| Configuration et secrets | Recette configurations et secrets ; champs locaux, clés normalisées par le moteur, vault distinct du fichier en clair |
| Secrets conditionnels | Recette 0.4.0 ; sélectionner depuis les configs résolues avant injection, sans dépendre de `configure_configs()` |
| Plusieurs services sélectionnables | Exemple ARR final ; valider la sélection et filtrer soi-même outils et racines de skills |
| Logs et administration | Recette 0.4.1 ; logger du connecteur sans handler ni niveau local, catalogue complet distinct des secrets actifs |
| RAG natif | Recette RAG ; index paresseux, ingestion séparée et snapshot complet potentiellement destructif |
| Backend RAG du plugin | Sous-section Backend détenu par le plugin ; factory synchrone, concurrence et atomicité, citations explicitement exposées |
| Livraison hors ligne | Installation/validation ; wheels et dépendances compatibles, build sans isolation si prérequis fournis |

## Auto-contrôle avant livraison

- [ ] Noms cohérents entre distribution, module, `id`, entry point, handlers,
  dossiers de skills, URI, clés et README ; migrations explicites si renommage.
- [ ] Hooks synchrones et ordre d’injection respecté ; secrets conditionnels
  uniques issus du catalogue complet, outils/skills filtrés par le plugin.
- [ ] Aucun réseau, ingestion ou chargement de modèle à l’import, dans la factory,
  les hooks ou `register()` ; aucun accès à `context.index` au démarrage.
- [ ] stdout réservé au MCP stdio ; logs stderr sans secrets, configuration,
  données métier ou exceptions API brutes ; handlers async sans appels bloquants.
- [ ] Effets des outils décrits fidèlement via `ToolAnnotations` ; autorisations
  contrôlées par le service, HTTP local par défaut sans accès distant implicite.
- [ ] Skills servis depuis le module installé : noms valides, racines sans symlink,
  références embarquées, aucun secret ni rapport privé dans les ressources.
- [ ] README conforme : titres et quatre tableaux présents, inventaire réel,
  commandes vérifiées, aucune installation PyPI annoncée sans publication réelle.
- [ ] Tests, archives et installation hors dépôt vérifiés selon le périmètre ;
  résultats et omissions consignés, aucune conformité déduite d’un lint seul.

## Règles

1. Utiliser les imports publics et le moteur distribué ; ne pas exiger son clone.
2. Respecter le projet existant et n’ajouter que les capacités demandées.
3. Conserver démarrage paresseux, confidentialité et intégrité du transport stdio.
4. Tester avec données fictives et services simulés, sans accès à la production.
5. Préserver les données et les anciennes configurations lors des migrations.
6. Distinguer ressources MCP, édition locale, installation serveur et publication.
7. Rapporter les résultats exécutés et les limites sans inventer de validation.
