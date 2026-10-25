# Jenkins

Cible : `Jenkinsfile` déclaratif, selon les conventions du dépôt.

- Confirmer agent/label, système, Python ≥3.12 et plugins Jenkins disponibles.
  Ne pas supposer Docker ou un plugin de publication installé.
- Prévoir checkout avec tags/historique pour hatch-vcs, environnement virtuel,
  installation dev, stages qualité/tests/build et archivage des distributions.
- Exécuter Ruff, mypy, Radon, Bandit et tests/couverture avec les commandes réelles.
  Publier les rapports avec les capacités présentes ; archiver les fichiers si
  aucun plugin de rapport n’est disponible. Nettoyer seulement l’espace du job.
- Si livraison demandée, stage distinct limité aux tags/branches retenus et
  environnement autorisé. Réutiliser les archives validées ; gérer leur transfert
  avec stash/unstash si les stages changent d’agent.
- Utiliser les identifiants Jenkins fournis via `withCredentials` si nécessaire,
  jamais des secrets dans le Jenkinsfile ou une interpolation Groovy. Confirmer
  les identifiants attendus sans demander leur valeur. Ne pas rendre les
  credentials accessibles aux builds de PR non fiables.

Sources : [Pipeline déclaratif](https://www.jenkins.io/doc/book/pipeline/syntax/),
[gestion des credentials](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#handling-credentials).
