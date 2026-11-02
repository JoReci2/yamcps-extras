# Évaluer un skill et ses déclencheurs

## Baseline et critères

Avant de rédiger, choisir deux ou trois tâches réalistes, dont un cas limite.
Définir pour chacune : entrées brutes, résultat observable, erreurs éliminatoires,
périmètre et méthode de mesure. Exécuter sans skill dans un contexte neuf si
possible ; sinon utiliser les échecs observés de la conversation en les distinguant
d’un essai contrôlé. Sans baseline disponible, écrire « baseline non mesurée ».

Une grille simple peut compter les critères satisfaits sur les critères applicables.
Définir les critères **avant** l’observation ; ne pas inventer un pourcentage global
pour agréger lint, style et comportement. Pour une amélioration, conserver les
mêmes tâches et critères avant/après. Une grille modifiée rend la comparaison
partielle ; le dire.

## Essais en contexte neuf (forward-testing)

Utiliser ce protocole pour les skills à effort élevé et les workflows scriptés ou
à plusieurs étapes ; le répéter après réorganisation importante ou ajout de
références. Pour un changement de description, tester aussi le routage.

1. Préparer la requête comme celle d’un véritable utilisateur et fournir seulement
   les artefacts nécessaires avec le skill à utiliser. Ne pas révéler le diagnostic,
   les réponses attendues ou les corrections recherchées à l’agent évalué.
2. Utiliser un contexte neuf ou un sous-agent si disponible et autorisé. Il doit
   résoudre la tâche, pas réciter une checklist en prétendant l’avoir suivie.
3. Exécuter les cas de la baseline avec le skill. Relever les fichiers émis, étapes
   manquées, commandes inventées, références lues ou oubliées et violations de périmètre.
4. Tester les niveaux de modèle réellement disponibles et visés : le plus petit
   utile pour la suffisance des consignes, le plus capable pour leur coût et leur
   possible effet négatif. Ne pas prétendre tester un modèle indisponible.
5. Comparer aux critères et au résultat sans skill. Clarifier ou script-er une étape
   oubliée ; retirer une instruction qui dégrade un résultat correct sans elle.
6. Nettoyer les artefacts entre essais pour éviter la contamination. Revenir à la
   rédaction après un échec puis rejouer les cas concernés avec un contexte neuf.

Un essai réussi seulement avec les réponses attendues exposées ne valide pas le
skill. Corriger le protocole ou les instructions plutôt que relâcher les critères.
Le test ne doit ni contacter la production ni publier pour prouver une procédure.
Si les accès, outils, ressources ou autorisations manquent, omettre la partie
concernée avec la raison et la prochaine vérification concrète.

## Cas de référence à adapter

| Tâche | Critères observables |
| --- | --- |
| Créer un skill de procédure métier | Entrées/sortie, exclusions, modèle, critères et emplacement réels ; pas de doublon ni de restriction implicite à yamcps |
| Revoir un skill avec références cassées | Constats localisés, lecture des références accessibles, aucune édition des skills |
| Auditer une collection mêlant actifs, notices et fichiers privés | Statuts parsés, comptes distincts, erreurs YAML séparées et routage vers actifs publiés |
| Optimiser une description générique | Cinq cas positifs et cinq négatifs, frontières avec voisins et limites du test manuel |
| Capitaliser une conversation | Règle de classe réutilisable, préférence pour le skill existant, pas de journal privé exporté |
| Client limité à la lecture MCP | Contenu et étapes livrés, aucune prétention d’écriture ou d’installation |
| Fusionner deux skills | Modes utiles préservés, notices et délai de migration respectés, inventaires/routage/tests cohérents |

## Essais de routage

Définir cinq requêtes qui doivent déclencher le skill et cinq requêtes voisines qui
ne doivent pas le sélectionner. Pour chacune, consigner texte, décision attendue,
skill mieux adapté le cas échéant, résultat observé et raison.
Inclure synonymes, demande sans nom explicite, demande au périmètre ambigu et
invocation historique d’une notice, cette dernière dans un lot distinct.

Le jugement manuel est une vérification heuristique ; le routage dépend du client
et de son catalogue chargé. Si possible, exécuter les requêtes dans le client cible
avec la collection active et enregistrer la sélection. Une réussite de `skills/get`
ne prouve pas une sélection automatique correcte.

## Rapport de validation

Séparer les axes et le type de preuve :

| Axe | Preuve |
| --- | --- |
| Structure | Parser réel, liens, noms, références, budget |
| Comportement | Artefacts ou actions observés sur les tâches contrôlées |
| Routage | Sélection dans le client ou grille manuelle explicitement étiquetée |
| Distribution | Ressources dans les archives installées et catalogue servi |

Consigner baseline, modèles/capacités réellement utilisés, critères satisfaits et
applicables, cas réussis et exécutés, omissions, décisions conserver/rejeter et
prochaine action. Une commande documentée reste distincte d’une commande exécutée.
