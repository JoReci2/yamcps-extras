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

Pour une livraison, configurer la découverte des tags du job multibranche avec le
plugin SCM disponible. Restreindre le stage avec `when { buildingTag() }`, puis
valider `TAG_NAME` selon la section « Construire depuis le tag de version » du
skill. Ne pas utiliser `BUILD_NUMBER` ou `BRANCH_NAME` comme version. Vérifier le
checkout du commit du tag, y compris pour un tag annoté. Si une image est demandée,
son tag est exactement `TAG_NAME`, préfixe `v` inclus ; transmettre l’image validée
par artefact/digest entre agents, sans reconstruire lors de la publication.
