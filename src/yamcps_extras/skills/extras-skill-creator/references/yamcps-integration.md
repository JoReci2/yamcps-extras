# Distribuer un skill par yamcps

Cette référence s’applique seulement aux skills exposés par un plugin yamcps.
Pour un skill autonome ou une autre collection, suivre son intégration propre.
Le préfixe `extras-` est celui de cette collection, pas une exigence des skills
créés pour d’autres projets.

## Préparer

Lire `skill://extras-changelog/SKILL.md` et son historique avant modification du
plugin. Consulter `skill://extras-develop-plugin/SKILL.md` pour le contrat du plugin,
et `skill://extras-python/SKILL.md` pour le code et les tests Python.
Identifier la version déclarée et installée du moteur, la racine réelle des skills,
le catalogue et la politique de routage ; ne pas exiger le clone des sources moteur.

## Intégrer ensemble

1. Créer le dossier sous la collection réelle. Pour Extras :
   `src/yamcps_extras/skills/<nom>/SKILL.md`. Le moteur exige le préfixe
   `<identifiant-connecteur>-` et un nom identique au dossier : pour Extras,
   `extras-<nom>`. Un skill autonome sans ce préfixe nécessite un renommage
   et la mise à jour des liens avant distribution dans ce catalogue.
2. Faire retourner la racine par `skill_roots()` ; dans Extras, mettre à jour la
   liste `_SKILLS`. Le chemin est relatif au module installé, pas au cwd.
3. Ajouter ressources utiles dans `references/` et modèles dans `assets/`.
   Tous les fichiers de la racine seront publiés : aucun secret, symlink, cache,
   rapport privé ou fichier de travail. Préserver les licences applicables.
4. Mettre à jour README, guide de contribution, comptes codés en dur, modèles de
   consignes et liens entre skills. Router seulement les tâches qui le justifient.
5. Étendre les tests de catalogue existants et les assertions de routage. Ne pas
   introduire outil, prompt, configuration ou appel réseau dans un plugin documentaire
   pour contourner une limite du client.

## Vérifier la distribution et le runtime

- Parser le frontmatter avec le moteur installé. Le contrat inspecté pour
  yamcps 0.4.1 exige les noms/descriptions et conserve le mapping de frontmatter.
  Vérifier le comportement effectif sur toute autre version ciblée, sans supposer
  que `metadata.deprecated` retire automatiquement un skill du catalogue.
- Construire wheel et sdist avec l’environnement et les commandes du dépôt.
  Inspecter la présence des fichiers, y compris références et notices de licence.
- Reconstruire le wheel depuis le sdist sans accès à Git selon les règles du dépôt.
- Installer le wheel dans un environnement de test distinct ; lire les ressources
  hors des sources, sans `PYTHONPATH` pointant vers leur arbre.
- Vérifier découverte du connecteur, `skills/list`, `skills/get` si pris en charge,
  et `resources/read` pour le guide et chaque ressource liée. Résoudre les liens
  relatifs en URI `skill://<nom>/<chemin>` ; vérifier tailles et empreintes si exposées.
- Exercer les transports concernés : mémoire, stdio et HTTP loopback pour Extras.
  Préserver l’absence d’outils/prompts et vérifier la coexistence si nécessaire.
- Tester les anciennes URI prévues par une migration et les refus de chemins invalides.
  Ne pas interpréter une absence d’affichage dans le client comme une absence de
  ressource sans distinguer catalogue MCP et découverte native.

## Mise à jour du serveur

Le catalogue est chargé au démarrage. L’administrateur installe la nouvelle
version du plugin sur le serveur puis le redémarre dans le cadre autorisé.
Le MCP distant ne copie pas le dossier chez le client. Une installation locale
pour les tests n’est ni cette mise à jour ni une publication PyPI.
Pour un renommage, respecter la politique de transition, les consignes déjà
générées et les notices promises avant de retirer une URI.

## Rendre compte

Séparer fichiers modifiés, commandes réellement exécutées, résultats de catalogue,
archives inspectées et limites de découverte dans les clients non éprouvés.
Ne pas annoncer que tous les clients prennent en charge la sélection native des
skills à partir d’une seule lecture MCP réussie.
