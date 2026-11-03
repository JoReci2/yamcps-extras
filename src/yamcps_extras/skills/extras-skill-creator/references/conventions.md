# Conventions de création et de revue des skills

## Sommaire

1. Principes et budget de contexte
2. Frontmatter et cycle de vie
3. Structures par niveau d’effort
4. Style, exemples et modèles
5. Organisation des références
6. Relations et déclencheurs
7. Auto-contrôle des sorties
8. Pièges des skills de diagnostic
9. Fiabilité des workflows
10. Scripts et dépendances
11. Portabilité entre modèles et clients
12. Inventaire de la collection

## 1. Principes et budget de contexte

Le contexte est partagé entre la conversation, le catalogue, les ressources et les
résultats des outils. Pour chaque paragraphe, demander ce qu’il ajoute qu’un agent
compétent ne connaît pas : convention locale, piège réel, critère observable.
Préférer un petit exemple correct à une longue explication générique.

| Élément | Cible de conception | Interprétation |
| --- | --- | --- |
| Description | 80 à 120 caractères | Conseil de concision ; conserver les frontières utiles |
| Corps du SKILL.md | 150 à 250 lignes souhaitées ; moins de 500 | Budget de cette adaptation, pas preuve de qualité |
| Référence | Un sujet ou une variante | Chargement à la demande ; pas de remplissage |

Ajuster le degré de liberté **par étape** : heuristiques pour les choix multiples
valides, modèle paramétré pour un format préféré, script/commande exacte pour une
opération fragile. Demander ce qui casse si l’agent procède autrement. Pour un
montant, une suppression ou un contrat strict, la réponse doit être concrète.
Donner un défaut et une alternative conditionnelle, pas une liste équivalente.
Commencer assez souple puis resserrer sur les échecs observés.

Les diagnostics et la surveillance demandent davantage de précision : nommer les
commandes vérifiées et critères, plutôt que « vérifier que tout va bien ».
Un exact script erroné reste erroné : vérifier aussi ses chemins et sa cible.

## 2. Frontmatter et cycle de vie

Profil de format vérifié le 2 novembre 2026 contre la
[spécification Agent Skills](https://agentskills.io/specification).
Les conseils de budget et les conventions de traçabilité restent distincts
des champs obligatoires de la spécification.

### Profil recommandé pour un nouveau skill maintenu

```yaml
---
name: mon-skill
description: "Créer et revoir des procédures de qualification avec leurs critères et preuves."
license: MIT
compatibility: "Édition locale requise. Optionnel : Git pour l’historique."
metadata:
  source: proprietaire/collection
  date_added: "2026-11-02"
  effort: high
---
```

Adapter la licence réelle, la source et la date ; ne pas recopier ces exemples
sans examen. Le minimum du parseur yamcps inspecté est `name`/`description` et un
nom de dossier cohérent et le préfixe de l’identifiant du connecteur. Licence et métadonnées sont des conventions de traçabilité
recommandées pour les nouveaux skills, pas une raison de déclarer tous les anciens
skills à frontmatter minimal invalides. Distinguer erreur de parser, écart au
contrat local obligatoire et amélioration conseillée.

| Champ | Valeurs et contrôle | Portée |
| --- | --- | --- |
| `name` | 1 à 64 caractères, minuscules/chiffres/tirets ; sans tiret initial/final/consécutif ; égal au dossier | Profil portable à vérifier sur la cible |
| `description` | Texte non vide ; 1024 caractères maximum du profil portable ; pas de XML | Déclenchement et budget du catalogue |
| `license` | Licence réelle ou référence à sa notice | Traçabilité de redistribution |
| `compatibility` | Texte de prérequis, 500 caractères maximum du profil portable | Ne donne pas de permission |
| `metadata.source` | `owner/repo`, ou `custom` pour un skill non publié | Provenance locale |
| `metadata.date_added` | Chaîne ISO entre guillemets | Création initiale, jamais date de chaque révision |
| `metadata.effort` | `low`, `medium`, `high` | Complexité qualitative, pas mesure de tokens |
| `metadata.internal` | Chaîne `"true"`/`"false"` si la collection la gère | Convention d’installateur, pas règle MCP universelle |
| `metadata.deprecated` | Chaîne `"true"`/`"false"` recommandée ; accepter aussi les booléens existants | Statut de notice de migration |
| `allowed-tools` | Syntaxe dépendante du client, à vérifier avant ajout | Extension expérimentale, pas une sandbox |

Citer les valeurs YAML contenant un deux-points. Vérifier le type des métadonnées
sur le client cible ; certains profils attendent des chaînes. Ne pas ajouter un
champ `model` pour choisir une famille ou un niveau de modèle.
Les restrictions de noms réservés propres à un fournisseur ne sont pas des règles
universelles ; les vérifier pour le client visé. Éviter ces noms en cas de besoin
réel de portabilité entre fournisseurs.

`paths:` et les autres extensions de routage de certains clients ne font pas
partie du profil portable de base. Ne pas les mettre dans la source générique
sans contrat explicite : certains importeurs rejettent les clés inconnues.
Garder les motifs dans la description/périmètre ou dans une copie spécifique au
client. Vérifier les affirmations de spécification contre la documentation du
client et son parseur, jamais d’après cette seule référence.

### Statut et publication

Parser d’abord le frontmatter. Classer `metadata.deprecated` comme notice si sa
valeur est le booléen `true` ou une chaîne dont `strip().casefold()` vaut `true`.
Une chaîne `"false"` n’est pas dépréciée. Une erreur YAML ou de structure doit être
rapportée séparément ; ne pas la convertir en statut actif silencieusement.

Publié = actifs publiés + notices publiées. Exclure les entrées privées selon
les règles de publication ; Git ignoré et catalogue MCP doivent être confrontés.
Une notice conserve les invocations historiques et le chemin de migration.
L’examiner selon la politique de transition, pas selon la profondeur attendue d’un
skill actif. Maintenir ses tests et notices jusqu’au terme exigé.

### Exécution sans dialogue

Ne pas supposer qu’un utilisateur répondra pendant une exécution automatisée.
Donner un défaut sûr aux choix réversibles et consigner l’hypothèse. Si une cible,
un accès ou une autorisation indispensable manque, arrêter la partie dépendante
avec une raison précise. Le mode sans dialogue ne crée aucune autorisation.
Ne pas citer de flag d’un client sans vérification de son aide/version.

## 3. Structures par niveau d’effort

| Effort | Usage | Structure |
| --- | --- | --- |
| `low` | Wrapper ciblé ou notice de transition | Aperçu, usages/exclusions, court workflow, règles nécessaires |
| `medium` | Un domaine avec procédure modérée | Même base, étapes détaillées et références utiles |
| `high` | Plusieurs modes ou tâches à étapes | Cas/exclusions, auto-contrôle, workflows, références, relations et règles |

Pour un skill de plateforme, ajouter un bloc de versions cibles avec date et
source de vérification. Auto-contrôle obligatoire pour les sorties générées de
code, configuration, manifestes, infrastructures ou fichiers structurés ; pour un
simple rapport analytique, choisir les contrôles pertinents plutôt que recopier
une checklist d’infrastructure. Référentiel de conformité et checklist de
production restent conditionnels au domaine.

Terminer le skill par une section explicite `Règles`. Une section courte est
suffisante si elle contient les contraintes réelles.
Ne pas inventer de règles pour satisfaire un nombre de rubriques.
Ne pas réécrire un miroir amont selon ces conventions sauf si le projet maintient
explicitement une adaptation ou un fork.

## 4. Style, exemples et modèles

- Écrire à l’impératif ou à l’infinitif, calmement, en expliquant les raisons utiles.
- Employer la langue du projet : le français et ses accents sont attendus ici.
  L’ASCII imposé par la collection amont est une convention locale non transposée.
- Garder une terminologie stable, un concept par terme, sans emphase artificielle,
  répétitions de mots-clés, commentaire bruyant ni paragraphe générique.
- Donner le comportement courant ; déplacer les anciennes méthodes dans une
  section historique. Une date de vérification n’est pas une branche de workflow
  « avant/après telle date ».
- Ne pas modifier les doubles tirets dans les commandes, flags, commentaires ou
  code au nom d’une règle typographique de prose.
- Utiliser des chemins relatifs à slashs et le nom exact des outils MCP découvert
  chez le client. Certains hôtes emploient `serveur:outil`, d’autres un autre
  identifiant ; ne pas inventer un nom supposé universel.
- Utiliser tables pour les comparaisons, checklists pour les séquences vérifiables,
  blocs de code avec langue pour les exemples. Pas de tableaux décoratifs.
- Vérifier API, flags, versions, modules d’infrastructure et endpoints cités.
  Ne pas remplacer une vérification par un souvenir vraisemblable.

### Modèle de base à adapter

Les valeurs entre chevrons sont des placeholders à remplacer avant livraison ;
ce modèle est un défaut à adapter, pas un format strict universel.

```markdown
---
name: <espace-de-noms>-<action>
description: "<Tâche, domaine distinctif et résultat attendu.>"
license: <licence-réelle>
metadata:
  source: <owner/repo-ou-custom>
  date_added: "<YYYY-MM-DD>"
  effort: <low-ou-medium-ou-high>
---

# <Titre>

## Quand utiliser
<Cas concrets.>

## Quand ne pas utiliser
<Tâches voisines et skills disponibles correspondants.>

## Auto-contrôle
<Erreurs fréquentes du domaine et contrôles de sortie.>

## Workflow
1. Identifier cible, consignes et état.
2. Recueillir les entrées et critères observables.
3. Effectuer le travail autorisé.
4. Valider ; en cas d’échec, corriger et revenir à l’étape 3.
5. Vérifier contre la demande puis rendre compte.

## Ressources
<Chaque lien réel et sa condition de lecture.>

## Skills associés
<Relations vers voisins vérifiés, si utiles.>

## Règles
<Seulement les contraintes nécessaires.>
```

## 5. Organisation des références

Déplacer exemples longs, variantes, checklists et détails conditionnels dans
`references/`. Placer les modèles à copier dans `assets/`. Utiliser des noms qui
expriment le contenu ; un fichier par sujet ou plateforme quand cela aide la lecture.
Nommer directement **chaque référence** dans SKILL.md avec le moment où la lire.
Éviter les chaînes de découverte ; les liens entre références restent possibles si
leurs cibles sont aussi nommées dans le guide principal.

Chaque référence commence par un titre ; ajouter un sommaire au-delà de 100 lignes
pour rendre visible la portée lors d’une lecture partielle. Employer un générateur
seulement si le projet en fournit réellement un et vérifier sa sortie. Une liste
maintenue manuellement est acceptable ici. Ne pas mentionner les scripts de lint
ou de génération de l’amont comme s’ils étaient installés dans Extras.

## 6. Relations et déclencheurs

Dans les exclusions, nommer le skill voisin réel et la tâche qu’il possède.
Dans les relations, expliquer la complémentarité plutôt que lister des noms.
Mettre les noms en gras si cela facilite le repérage et fournir les URI exactes
pour des ressources MCP réellement publiées.

Vérifier l’état actif, la publication et l’accessibilité, pas seulement l’existence.
Les notices peuvent être citées pour la migration mais ne sont pas des destinations
ordinaires de routage. Pour une collision réelle, préciser les frontières des deux
skills ; des mots de domaine partagés ne suffisent pas à imposer des exclusions.

Mettre tâche et domaine en tête de description pour supporter une troncature.
Utiliser une fois les termes distinctifs, des synonymes naturels et une exclusion
courte quand elle évite un mauvais choix. Éviter « nettoyage » sans objet, un mot
magique exact, les listes répétées `Triggers:` ou des capacités non implémentées.
Le plafond de longueur n’assure pas le chargement par le client : le catalogue
complet partage un budget. Tester demandes naturelles, alias et tâches voisines ;
les nombres de caractères ne prouvent pas la qualité de sélection.

## 7. Auto-contrôle des sorties

Cibler les erreurs récurrentes du domaine avant de rendre un livrable généré.
Un auto-contrôle qui répète « vérifier la qualité » ne donne aucun critère.

| Domaine | Exemples de contrôles à adapter et vérifier |
| --- | --- |
| Conteneurs | Utilisateur, images identifiables, secrets absents des couches |
| Orchestration | Namespace/cible, ressources, contexte de sécurité |
| CI/CD | Permissions explicites, références de dépendances, absence de secrets dans logs |
| Git | Identité/auteur, contenu indexé, absence de secrets, workflow du dépôt |
| Données | Contrôle des accès, sauvegarde/restauration, chiffrement selon besoin |
| Code | Validation aux frontières, propagation des erreurs, API réellement disponibles |
| Skills | Frontmatter, ressources, déclencheurs, périmètre et sortie vérifiable |

Ces exemples ne certifient aucune conformité et ne remplacent pas les contrats
réels des outils ou les exigences du projet.

## 8. Pièges des skills de diagnostic

### Échecs masqués

Ne pas utiliser `2>/dev/null` pour cacher une erreur dont la cause est nécessaire
au diagnostic. Un accès refusé n’est pas une ressource absente. Détection optionnelle
d’un outil et nettoyage peuvent accepter une sortie réduite si aucune preuve utile
n’est supprimée. Conserver le code retour et lire l’erreur avant de conclure.

| Signal | Ne pas conclure automatiquement | Vérification nécessaire |
| --- | --- | --- |
| Timeout distant | Ressource absente | Connexion, pare-feu, cible |
| Permission refusée | Fichier inexistant | Identité et droits effectifs |
| Sortie vide | Tout est sain | Code retour, stderr, filtre et cible |
| Commande introuvable | Fonctionnalité non prise en charge | Dépendance et environnement |

### Sens des métriques

Documenter ce que mesure la métrique et ce qu’elle ne mesure pas, son unité, la
fenêtre d’observation et le seuil justifié. Exemples à vérifier dans le domaine :
allocation d’un pool thin différente de l’usage du système de fichiers ; CPU d’un
autoscaler rapportée à la request différente d’une capacité CPU totale ; taille
virtuelle d’image différente de son occupation disque ; `df` différent de `du`.
Ne pas utiliser ces exemples comme documentation normative sans vérification.

### Fraîcheur liée au calendrier

Pour sauvegardes, rotations et tâches planifiées, lire le calendrier réel puis
comparer l’âge à la cadence prévue. Trois jours peuvent être en retard pour une
sauvegarde quotidienne et normaux pour une sauvegarde hebdomadaire.

### Improvisation des diagnostics

Définir la liste des commandes autorisées et critères. Une référence suffisamment
complète réduit l’improvisation. Si la procédure est fermée, exécuter uniquement
ses contrôles et signaler la couverture manquante comme proposition, sans lancer
une opération supplémentaire ni modifier la production pour « vérifier ».

## 9. Fiabilité des workflows

- Donner une checklist de progression pour un ordre nécessaire, pas pour une
  simple liste de conseils indépendants.
- Associer la sortie à un validateur réel ou une grille explicite ; répéter
  validation/correction jusqu’au succès ou au blocage clairement rapporté.
- Nommer l’étape de retour, plutôt que cocher une étape dont le contrôle échoue.
- Pour actions groupées, destructrices ou à fort impact : établir un plan
  structuré des changements, le vérifier, appliquer dans le périmètre autorisé,
  puis vérifier l’effet. Le plan n’accorde aucune permission manquante.
- Dire si un modèle est strict ou adaptable. Si le style importe, fournir deux
  ou trois paires entrée/sortie plutôt qu’une longue description abstraite.
- Router explicitement création et édition ; éviter un workflow implicite unique.
- Après un échec non couvert, proposer une règle réutilisable. La modifier si la
  capitalisation est demandée, sinon conserver la proposition dans le bilan.

## 10. Scripts et dépendances

Préférer un script pour une opération déterministe, répétitive ou fragile, pas
pour multiplier les fichiers. Dire s’il faut l’exécuter ou le lire. Tester son
exécution sur les entrées représentatives et négatives. Gérer erreurs attendues
avec un message utile et défaut sûr ; faire échouer clairement les vraies erreurs.
Expliquer seuils, retries et délais ; ne pas inventer de constantes.

Déclarer les prérequis et donner leur détection près de l’étape qui les emploie.
Installer seulement dans l’environnement autorisé du projet, jamais globalement
par défaut. Pour Python, utiliser le `.venv` requis par le projet et les conventions
**extras-python** si ce parcours est concerné. Sans installation possible,
indiquer le prérequis manquant au lieu d’improviser une commande différente.

Les scripts de l’amont ne sont pas embarqués ici. Si un validateur du dépôt attend
un parent de collection, le vérifier sur son aide/source. Zéro cible inspectée
n’est pas un contrôle réussi. Les fichiers de validation temporaires restent hors
des racines publiées.

## 11. Portabilité entre modèles et clients

Cibler les capacités nécessaires, pas un nom de modèle dans le frontmatter.
Consigner les familles/niveaux réellement éprouvés dans le rapport d’évaluation.
Petit modèle : la consigne suffit-elle ? Modèle plus capable : le détail améliore-t-il
le résultat ou ajoute-t-il des contraintes inutiles ? Comparer à une baseline.
Rendre plus explicite ou scriptée une étape oubliée ; couper une instruction qui
n’apporte rien. Ne pas simuler un autre modèle en lui demandant de « faire comme ».

Distinguer lecture MCP, découverte native de skills et installation de dossiers.
Un guide utile servi comme ressource n’est pas automatiquement ajouté au catalogue
natif du client. Vérifier réellement les mécanismes de sélection disponibles.

## 12. Inventaire de la collection

Reconstruire chaque inventaire depuis la collection cible et sa publication réelle.

| Champ à relever | Preuve |
| --- | --- |
| Nom, source, effort, date initiale | Frontmatter parsé ; absence indiquée |
| Actif ou notice | Valeur normalisée de `metadata.deprecated` |
| Publié ou privé | Règles Git/registre et catalogue réel |
| Dernière modification | Historique Git, sinon mtime avec limite signalée |
| Références et collisions | Fichiers résolus et comparaison sémantique des actifs |

La création locale peut précéder une publication publique. Ne pas réécrire
`date_added` pour l’aligner artificiellement sur le premier commit visible.
