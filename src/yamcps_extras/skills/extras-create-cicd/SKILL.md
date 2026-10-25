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

## Construire et vérifier

Utiliser Python ≥3.12, les dépendances dev déclarées et yamcps 0.4.0 stable.
Adapter les commandes du skill Python au plugin ; conserver pytest s’il existe,
ainsi que unittest pour ses nouveaux tests. Collecter couverture et wheel/sdist.
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
