# Conventions et modèle de skill

## Structure

Dans Extras, placer le skill sous
`src/yamcps_extras/skills/<nom>/SKILL.md`. Dans un autre plugin, suivre son
arborescence et son espace de noms. Garder un nom en minuscules, chiffres et
tirets, sans tiret initial, final ou consécutif, identique au dossier.

Utiliser le frontmatter minimal reconnu par la collection : `name` et une
`description` non vide. Ne pas supposer que des métadonnées spécifiques à un
autre client pilotent le moteur yamcps. Vérifier le parseur cible avant d’ajouter
des champs optionnels. Les contraintes d’un client particulier ne sont pas des
contraintes universelles.

Rester sous 500 lignes dans le guide principal. N’ajouter que des ressources
utiles, directement liées et accompagnées de leur condition de lecture.
Pour une référence longue, ajouter un sommaire. Garder les explications propres
au domaine plutôt que répéter les capacités générales d’un agent.

## Modèle à adapter

Les valeurs entre chevrons sont des placeholders à remplacer avant livraison.

```markdown
---
name: <espace-de-noms>-<action>
description: "<Tâche précise, situations de déclenchement et résultat attendu.>"
---

# <Titre lisible>

## Entrées et résultat
<Entrées nécessaires, critères de réussite et exclusions.>

## Ressources
<Liens relatifs réels, URI MCP correspondantes et quand les lire.>

## Workflow
1. Lire les consignes et identifier le contexte.
2. Examiner les données et préserver les fichiers existants.
3. Effectuer le travail autorisé.
4. Vérifier le résultat ; revenir à l’étape 3 en cas d’échec.
5. Rendre compte des changements, preuves et limites.

## Auto-contrôle
- <Erreur fréquente du domaine à éviter.>
- <Vérification observable du livrable.>

## Règles
- <Contrainte nécessaire et spécifique au domaine.>
```

## Intégration dans un plugin

1. Ajouter le dossier à la liste réellement retournée par `skill_roots()`.
2. Ajouter sa destination aux consignes générées lorsque la tâche le justifie.
3. Mettre à jour README, guide de contribution et inventaires ou comptes codés
   en dur. Vérifier les liens entrants et sortants.
4. Étendre les assertions de catalogue existantes. Exercer la découverte, la
   lecture du guide et de ses ressources, et la résolution des URI de routage.
5. Construire wheel/sdist avec les commandes du dépôt ; inspecter les archives.
   Installer le wheel dans un environnement distinct et vérifier la lecture
   hors du répertoire des sources, sans `PYTHONPATH` pointant vers celles-ci.
6. Exécuter les contrôles applicables et examiner le diff final. Une installation
   locale de test ne vaut pas déploiement sur le serveur utilisateur.

Tous les fichiers sous une racine de skill sont publiés : exclure secrets,
symlinks, caches et fichiers de travail. Ne pas ajouter de script si un modèle
documentaire suffit. Si un script est nécessaire, déclarer ses dépendances,
expliquer s’il faut le lire ou l’exécuter, puis tester réellement son exécution.

## Cas de validation comportementale

| Cas | Critères |
| --- | --- |
| Nouveau skill de procédure métier | Entrées et sortie concrètes, pas de doublon, catalogue et routage mis à jour |
| Revue seule d’un skill aux références cassées | Constats avec chemins exacts, aucune édition, vérifications omises explicites |
| Description trop générale | Cas positifs et voisins négatifs distingués sans élargir le périmètre |
| Client limité à la lecture MCP | Contenu et étapes livrés sans prétendre écrire ou installer localement |

Adapter ces cas à la tâche réelle. Les considérer comme une grille de revue tant
qu’ils n’ont pas été exécutés par un agent dans le client cible.
