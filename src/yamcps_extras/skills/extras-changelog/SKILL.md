---
name: extras-changelog
description: Consulter les évolutions du moteur yamcps par version et leurs conséquences sur les plugins avant toute modification d’un projet de plugin yamcps.
---

# Historique du moteur yamcps

Lire ce skill et l’[historique versionné](references/versions.md) avant toute
modification du projet, y compris documentation, configuration et workflows.
La ressource est aussi disponible à
`skill://extras-changelog/references/versions.md` via `resources/read`.

1. Identifier la version installée et la plage déclarée dans le manifeste. Sans
   exécution possible, distinguer la version déclarée de la version vérifiée.
2. Lire les entrées correspondant à cette version et aux migrations envisagées.
   Relever seulement les impacts pertinents sur le changement demandé.
3. Renvoyer ensuite au fichier de consignes pour sélectionner les skills utiles
   à la tâche : `extras-develop-plugin` pour les contrats, `extras-python` pour le
   code, `extras-configure-cicd` pour les workflows. Ne pas tous les charger par
   défaut. Une entrée historique ne remplace pas le contrat de la version cible.
4. Si une version ou une information manque, vérifier les sources officielles
   accessibles, signaler l’incertitude et suspendre seulement les changements qui
   dépendent d’un contrat non vérifié. Ne pas inventer d’API ou de note de release.

Cet historique concerne le moteur, pas les releases du plugin développé. Il est
embarqué et ne requiert aucun clone du moteur. Lors d’une demande de mise à jour
de cet historique, conserver les versions précédentes et ajouter les changements
avec leurs sources et impacts pour les plugins ; distinguer une préversion d’une
stable. Sa lecture ne déclenche aucune écriture ni installation automatique.
