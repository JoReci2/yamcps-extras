---
name: extras-create-cicd
description: Créer ou adapter une CI/CD pour un plugin yamcps, en demandant le choix GitHub Actions, GitLab CI ou Jenkins ; contrôles Python, tests, build et livraison selon les besoins.
---

# Créer une CI/CD de plugin yamcps

Consulter d’abord `skill://extras-changelog/SKILL.md`, puis
`skill://extras-python/SKILL.md` pour les contrôles et
`skill://extras-develop-plugin/SKILL.md` pour packaging et contrat moteur.

## Choisir avant de générer

Demander explicitement : **quel type de CI : GitHub Actions, GitLab CI ou Jenkins ?**
Même si un workflow existe, proposer la plateforme observée et obtenir ce choix ;
ne pas générer de workflow tant que cette réponse manque. Une plateforme déjà
choisie explicitement dans la demande suffit, sans reposer la question.

Lire les consignes, le manifeste, les commandes qualité et les workflows existants.
Conserver leurs comportements utiles et préparer une modification ciblée.
Préciser les besoins non établis : contrôles souhaités, branches et déclencheurs,
runner/agent disponible, publication d’artefacts ou registre cible. La publication
et le déploiement sont optionnels ; sans demande, livrer qualité, tests et build.
Pour une publication demandée, préciser déclencheur de release, version, registre,
environnement et méthode d’authentification avant de produire ce job.

## Référence par plateforme

Lire uniquement la référence choisie, via lien relatif ou `resources/read` :

- [GitHub Actions](references/github.md) : `skill://extras-create-cicd/references/github.md`.
- [GitLab CI](references/gitlab.md) : `skill://extras-create-cicd/references/gitlab.md`.
- [Jenkins](references/jenkins.md) : `skill://extras-create-cicd/references/jenkins.md`.

## Construire depuis le tag de version

Pour toute construction de livraison (wheel/sdist et image conteneur si demandée),
le tag Git est la source de version. Accepter les versions finales et préversions,
par exemple `v0.1.0`, `v0.1.0dev1`, `v0.1.0.dev1`, `v0.1.0a1`, `v0.1.0b1`,
`v0.1.0rc1` et les post-releases comme `v0.1.0.post1`.

- Déclencher le build de livraison sur un tag `v*` ou une release associée à ce
  tag, puis valider réellement son format : le filtre `v*` seul ne suffit pas.
  Exiger le préfixe `v` suivi d’une version PEP 440 valide, sans epoch ni suffixe
  local, compatible avec la politique de version du projet. Ne pas limiter le
  validateur aux seules versions finales à trois composantes.
- Extraire le tag de l’événement CI et effectuer le checkout de sa référence
  exacte avec historique et tags. Vérifier que `HEAD` correspond au commit de
  `refs/tags/<tag>` (en déréférençant les tags annotés). Ne pas construire une
  livraison depuis la tête de la branche ou déduire sa version du dernier tag voisin.
- Pour Python, enlever uniquement le `v` initial, normaliser avec
  `packaging.version.Version` et comparer à la version des métadonnées du wheel
  et du sdist. `v0.1.0dev1` et `v0.1.0.dev1` correspondent à `0.1.0.dev1`.
  Avec hatch-vcs, laisser les métadonnées découler du checkout du tag ; refuser
  une version différente ou un suffixe local signalant un build intermédiaire.
- Si une image OCI/Docker est demandée, confirmer Dockerfile, contexte, registre
  et nom d’image. La construire depuis ce même checkout et les artefacts validés,
  puis lui donner **le tag Git exact**, préfixe `v` inclus :
  `<registre>/<image>:v0.1.0` ou `<registre>/<image>:v0.1.0dev1`.
  Vérifier que ce tag respecte aussi les contraintes du registre ; refuser un
  format incompatible plutôt que le transformer silencieusement. Ajouter les
  labels OCI `org.opencontainers.image.version` (tag Git) et
  `org.opencontainers.image.revision` (SHA du commit).
- Tester l’image construite ; transmettre cette même image par artefact ou digest
  au job de publication, sans reconstruction. Publier seulement si demandé.
  Ne pas utiliser le numéro de pipeline ou la branche comme version de livraison,
  ni attribuer `latest` à une préversion. Aucun alias `latest` sans besoin explicite.
- Les builds de contrôle sur branches/PR restent possibles, sans publication sous
  un tag de release. Ne pas ajouter une image à un plugin qui ne la demande pas.

Vérifier les scénarios : finale, développement avec/sans point, alpha/bêta/RC,
tag annoté, tag invalide ou absent, commit différent du tag, métadonnées Python
incohérentes et conservation du tag exact dans l’image. Les cas invalides doivent
échouer avant publication ; un build de branche ne doit pas devenir une release.

## Construire et vérifier

Utiliser Python ≥3.12, les dépendances dev déclarées et yamcps 0.4.0 stable.
Adapter les commandes du skill Python au plugin ; migrer les tests pytest
existants vers unittest selon ce guide, puis utiliser le runner standard dans la
CI. Collecter couverture et wheel/sdist.
Vérifier la lecture des skills depuis le wheel hors du dépôt. Simuler les API et
éviter modèles téléchargés, services réels et secrets dans les contrôles.

Pour une livraison, séparer construction et publication ; publier uniquement les
archives déjà validées, vérifier identité de distribution et version du tag selon
le versionnement réel. Ne pas copier le nom, le dépôt ou le vérificateur de release
d’un autre projet. Les builds hatch-vcs ont besoin de l’historique et des tags.
Limiter les permissions de publication au job concerné. Ne pas embarquer de secret,
ni exposer les credentials de publication aux contributions non fiables.

Vérifier syntaxe avec les outils disponibles, cohérence des chemins, déclencheurs,
transfert des artefacts et commandes dans un environnement local isolé. Vérifier les
versions et paramètres des intégrations dans leur documentation officielle avant
utilisation. Distinguer validation locale et exécution réelle du pipeline distant.
Livrer fichiers, prérequis de plateforme et résultats ; ne pas déclencher de
release, publication ou déploiement pour tester le workflow sans demande explicite.
