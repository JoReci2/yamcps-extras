---
name: extras-changelog
description: "Consulter ou actualiser l’historique du moteur yamcps et identifier les impacts de version sur ses plugins."
license: MIT
metadata:
  source: JoReci2/yamcps-extras
  effort: medium
---

# Historique du moteur yamcps

Lire ce skill et l’historique embarqué avant toute modification d’un projet de
plugin, y compris documentation, configuration et workflows. Relever les impacts
utiles à la tâche ; consulter l’historique ne demande ni de mettre à jour le moteur
ni de modifier ses notes de versions.

## Quand utiliser ce skill

- Identifier les changements du moteur qui affectent un plugin avant modification.
- Comparer ses contrats déclarés et installés avec une migration envisagée.
- Consulter une capacité introduite dans une version précise.
- Actualiser l’historique embarqué lorsque cette mise à jour est demandée.

## Quand ne pas utiliser ce skill

- Rédiger les notes de release du plugin : cet historique concerne le moteur,
  pas les releases de yamcps-extras ou du plugin développé.
- Implémenter ou modifier les contrats du plugin : **extras-develop-plugin**,
  `skill://extras-develop-plugin/SKILL.md`, après consultation des impacts.
- Écrire ou revoir son code et ses tests : **extras-python**,
  `skill://extras-python/SKILL.md`.
- Configurer sa CI/CD : **extras-configure-cicd**,
  `skill://extras-configure-cicd/SKILL.md`.
- Créer ou revoir des skills : **extras-skill-creator**,
  `skill://extras-skill-creator/SKILL.md`.
- Initialiser les consignes du client : **extras-configure-agents**,
  `skill://extras-configure-agents/SKILL.md`.

## Ressource et limites

Lire l’[historique versionné](references/versions.md) pour les versions concernées.
Depuis MCP, utiliser `resources/read` sur
`skill://extras-changelog/references/versions.md` ; cette URI n’est pas un chemin
local. Réutiliser une lecture déjà effectuée dans la tâche si elle reste à jour.
La consultation ne nécessite aucun clone du moteur ni accès réseau.

La version la plus récente documentée n’est pas une preuve de la dernière stable
disponible. Une entrée résume des changements utiles aux plugins ; elle ne remplace
pas le contrat de la version cible. Une version absente signifie que l’historique
est incomplet, pas que ses contrats sont identiques à ceux de la version précédente.

## Parcours 1 : consulter avant une modification

1. **Identifier la cible.** Relever la plage yamcps du manifeste, les capacités
   utilisées et la version visée si une migration est demandée. Vérifier la version
   installée avec `.venv/bin/python -m pip show yamcps` si l’exécution est disponible,
   dans l’environnement du projet selon **extras-python**. Ne pas installer de
   dépendance pour une simple consultation ; sans runtime, indiquer « non vérifiée ».
2. **Lire les entrées utiles.** Examiner la version installée et les changements
   intermédiaires jusqu’à la cible envisagée, y compris leurs prérequis. Distinguer
   introduction d’une capacité, compatibilité conservée et changement de contrat.
3. **Vérifier les inconnues.** Si une version ou information manque, consulter
   les sources officielles accessibles de cette version : release, documentation
   taguée ou contrat distribué. Sans accès, signaler précisément l’incertitude et
   suspendre seulement les changements dépendant du contrat non vérifié. Ne pas
   inventer une API, une date ou une note de release.
4. **Reprendre la tâche.** Résumer les impacts applicables et leurs sources,
   puis suivre le fichier de consignes pour sélectionner les skills métier utiles.
   Ne pas charger tous les guides par défaut ni recharger celui-ci à chaque renvoi.
   Une différence de version seule n’autorise pas une migration ou une installation.

## Parcours 2 : actualiser l’historique sur demande

1. **Délimiter la mise à jour.** Lire l’historique entier, les consignes et l’état
   Git avant édition. Identifier les versions manquantes ou les corrections demandées ;
   préserver les entrées et changements locaux sans rapport.
2. **Collecter les preuves.** Vérifier version, statut stable/préversion et date
   dans les sources officielles. Utiliser des liens tagués ou des références de
   release stables ; vérifier les signatures et commandes contre le contrat ciblé.
   Ne pas présenter une branche de développement comme une release publiée.
3. **Rédiger les impacts.** Ajouter l’entrée dans l’ordre décroissant des versions,
   avec capacités, compatibilité, changements incompatibles et actions utiles aux
   plugins. Distinguer les faits sourcés des points non vérifiés. Conserver les
   versions précédentes ; corriger une erreur historique avec sa preuve sans
   attribuer une capacité à la mauvaise release.
4. **Valider et corriger.** Comparer chaque affirmation ajoutée à sa source,
   vérifier liens, ordre des versions et cohérence avec les entrées voisines.
   En cas d’échec, revenir à l’étape 2 ou 3. Mettre à jour le sommaire et la version
   de référence seulement si les preuves l’exigent ; ne pas modifier les dépendances
   des plugins ni les autres skills sans demande correspondante.
5. **Rendre compte.** Donner les versions ajoutées/corrigées, les sources consultées,
   vérifications exécutées et limites. Sans édition locale, fournir le contenu à
   appliquer ; ne pas annoncer de fichier modifié ou de test fictif.

## Auto-contrôle

- [ ] Version déclarée, installée et cible distinguées ; absence d’accès signalée.
- [ ] Impacts limités à la tâche ; minimum de version et ordre des hooks non déduits
  d’un simple numéro de release.
- [ ] Historique du moteur distingué des releases du plugin et de la dernière stable.
- [ ] Pour une mise à jour : statut, dates et contrats sourcés, anciennes entrées
  conservées, sommaire et liens cohérents, incertitudes explicites.
- [ ] Aucun changement de dépendance, installation ou déploiement implicite ;
  contrôle documentaire distingué d’une preuve de fonctionnement du runtime.

## Règles

1. Consulter avant de modifier ; ne réécrire l’historique que sur demande.
2. Vérifier les contrats de la version cible plutôt qu’extrapoler depuis une autre.
3. Conserver les sources et les versions précédentes lors d’une actualisation.
4. Revenir aux consignes pour charger seulement les skills utiles à la tâche.
5. Rapporter les inconnues et les contrôles omis sans inventer de résultat.
