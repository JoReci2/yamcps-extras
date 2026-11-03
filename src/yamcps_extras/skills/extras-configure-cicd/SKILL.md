---
name: extras-configure-cicd
description: "Configurer la CI/CD des plugins yamcps pour GitHub Actions, GitLab CI ou Jenkins : tests, build et livraison."
license: MIT
metadata:
  source: JoReci2/yamcps-extras
  effort: medium
---

# Configurer une CI/CD de plugin yamcps

Créer ou adapter les fichiers de pipeline du projet en préservant les contrôles
et les déclencheurs utiles. Par défaut, livrer qualité, tests et build ; publication,
image conteneur et déploiement restent conditionnels à la demande.
Une revue seule produit des constats sans modifier les workflows.

## Quand utiliser ce skill

- Créer ou modifier un pipeline GitHub Actions, GitLab CI ou Jenkins d’un plugin yamcps.
- Adapter ses runners, déclencheurs, contrôles Python et transferts d’artefacts.
- Préparer une livraison demandée depuis un tag, avec validation avant publication.
- Revoir permissions, secrets et séparation entre validation et publication.

## Quand ne pas utiliser ce skill

- Écrire ou corriger seulement le code et les tests Python : **extras-python**,
  `skill://extras-python/SKILL.md` ; compléter ici si leurs commandes CI changent.
- Concevoir le contrat, le packaging ou les hooks du plugin : **extras-develop-plugin**,
  `skill://extras-develop-plugin/SKILL.md` ; revenir ici pour leur automatisation.
- Refactorer les instructions d’un skill : **extras-skill-creator**,
  `skill://extras-skill-creator/SKILL.md`.
- Configurer les consignes du client : **extras-configure-agents**,
  `skill://extras-configure-agents/SKILL.md`.

## Ressources à lire selon le parcours

| Ressource | Condition de lecture |
| --- | --- |
| [GitHub Actions](references/github.md) | Plateforme GitHub Actions explicitement choisie |
| [GitLab CI](references/gitlab.md) | Plateforme GitLab CI explicitement choisie |
| [Jenkins](references/jenkins.md) | Plateforme Jenkins explicitement choisie |
| [Livraison par tag](references/release.md) | Construction ou publication de livraison demandée, image comprise si nécessaire |

Lire uniquement la plateforme choisie et les références utiles. Depuis MCP,
utiliser `resources/read`, par exemple
`skill://extras-configure-cicd/references/github.md`. Ces URI ne sont pas des
fichiers locaux ; sans écriture ou exécution, fournir les fichiers et commandes
à appliquer et marquer les contrôles non exécutés.

## Choix de plateforme et entrées

Demander explicitement **GitHub Actions, GitLab CI ou Jenkins** avant de générer
un workflow. Même si un workflow existe, proposer la plateforme observée et obtenir
ce choix. Une sélection explicite déjà donnée suffit ; ne pas reposer la question.
En attendant la réponse, inspecter le projet et préparer les constats sans générer.
Sans dialogue possible et sans choix, signaler précisément cette entrée manquante.

Relever les besoins non établis : branches, événements, OS et runner/agent,
contrôles, artefacts et registre cible. Pour une publication demandée, établir
déclencheur de release, version, environnement et authentification avant ce job.
Ne jamais demander la valeur d’un secret ; relever son identifiant de plateforme.

## Workflow

1. **Inspecter.** Lire les consignes, l’état Git, le manifeste, les scripts qualité
   et les workflows existants. Consulter `skill://extras-changelog/SKILL.md` et son
   historique ; réutiliser les ressources déjà lues et toujours à jour.
   Distinguer création, modification et revue seule.
2. **Fixer le parcours.** Obtenir le choix de plateforme selon la règle ci-dessus.
   Définir les déclencheurs, runners et sorties attendues ; préserver les comportements
   utiles existants. Ne pas ajouter de publication ou de déploiement implicitement.
3. **Vérifier les prérequis.** Lire la référence choisie et **extras-python** pour
   les commandes et l’environnement. Charger **extras-develop-plugin** seulement
   si packaging ou contrats moteur sont concernés. Relever versions Python/yamcps,
   extras dev et outils réellement déclarés ; vérifier les paramètres et versions
   des actions, images et plugins dans leurs sources officielles avant génération.
4. **Construire la modification.** Séparer qualité/tests/build et publication.
   Appliquer le `.venv` et les règles d’artefacts ci-dessous. Pour une livraison,
   lire la référence de release et sélectionner le checkout exact du tag ; aucune
   reconstruction des archives ou images entre validation et publication.
5. **Valider et corriger.** Vérifier syntaxe avec le validateur disponible pour la
   plateforme, chemins, filtres, permissions et dépendances entre jobs. Exécuter
   localement les commandes adaptées dans un environnement isolé. Examiner au moins
   une contribution non fiable, un build de branche et, si concernée, une release
   valide et invalide. En cas d’échec, revenir à l’étape 4 et relancer les contrôles
   affectés ; ne pas traiter une simple lecture du YAML comme un pipeline réussi.
6. **Livrer.** Donner fichiers modifiés, prérequis du runner, identifiants attendus,
   résultats exécutés et contrôles omis. Séparer validation locale, validation de
   configuration par la plateforme et exécution réelle du pipeline distant.
   Ne pas déclencher release, publication ou déploiement pour tester sans demande.

## Environnement et contrôles Python

Dans chaque job Python généré, créer un `.venv` à la racine du checkout avec
`python -m venv .venv`, puis utiliser explicitement `.venv/bin/python`
(Windows : `.venv\Scripts\python.exe`) pour installations, tests et builds.
Ne pas compter sur une activation conservée entre étapes ni installer globalement.
Les exemples des références ciblent des runners POSIX ; adapter chemins et shell
si le runner est Windows. Recréer l’environnement sur chaque agent/job isolé,
ne pas transférer un `.venv` entre systèmes.

Utiliser Python ≥3.12 et les dépendances dev déclarées ; respecter la plage yamcps
du plugin plutôt qu’imposer une version stable fixe. Pour une matrice, vérifier
les versions réellement couvertes et compatibles avant de les annoncer.
Adapter les commandes Ruff, mypy, Radon, Bandit, unittest, couverture et build
d’**extras-python**. Si la migration pytest est nécessaire, suivre sa procédure
en préservant les scénarios ; ne pas changer seulement le runner en laissant des
tests non collectés. Collecter couverture et distributions wheel/sdist.

Vérifier la lecture des skills depuis le wheel installé hors dépôt, sans
PYTHONPATH vers les sources. Simuler les API ; aucun service de production,
modèle téléchargé ou secret réel dans les contrôles. Pour hatch-vcs, récupérer
historique et tags. Adapter identité de distribution et vérificateur de release
au projet ; ne pas copier ceux d’un autre dépôt.

## Artefacts et permissions

Transmettre les archives validées au job de publication ; utiliser des chemins
et dépendances explicites pour éviter un répertoire vide ou des fichiers obsolètes.
Limiter les permissions de publication à ce job et à son environnement autorisé.
Ne pas exposer les credentials ni une permission d’écriture aux contributions
non fiables. Passer les valeurs d’événements par des variables citées, sans les
interpoler directement comme du code shell. Ne pas embarquer de secret dans
YAML, logs, caches, rapports, distributions ou images.

## Auto-contrôle avant livraison

- [ ] Plateforme choisie explicitement, consignes et comportements existants préservés.
- [ ] Déclencheurs, runner, shell, chemins, versions et dépendances cohérents.
- [ ] Chaque job Python utilise son `.venv` et les commandes réelles du projet.
- [ ] Tests effectivement collectés, couverture et artefacts issus du même checkout.
- [ ] Wheel vérifié hors sources ; omissions et résultats de validation expliqués.
- [ ] Pour une release : tag valide, HEAD exact, versions wheel/sdist cohérentes,
  image portant le tag Git exact si demandée, publication sans reconstruction.
- [ ] Permissions minimales ; aucun credential accessible au code non fiable.
- [ ] Aucun déclenchement distant ni publication annoncé sans exécution autorisée.

## Règles

1. Obtenir le choix explicite de plateforme avant de générer le workflow.
2. Respecter le manifeste et les outils du projet, sans migration de version implicite.
3. Exécuter les commandes Python dans le `.venv` propre à chaque job.
4. Séparer build, validation et publication ; réutiliser les mêmes artefacts validés.
5. Préserver la confidentialité et limiter les droits au job qui en a besoin.
6. Distinguer fichier généré, configuration validée et pipeline réellement exécuté.
