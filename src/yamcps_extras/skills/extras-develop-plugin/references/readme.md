# Contrat du README des plugins

Conserver exactement ces titres, dans cet ordre, pour tout plugin créé ou modifié :

```markdown
# nom du plugin
## Description
## Quickstart
## Outils
## Skills
## Variable de configuration
## Secret
```

- Remplacer le titre principal par le nom de distribution réel (`yamcps-<nom>`).
  Écrire une description courte du rôle et du périmètre du plugin.
- Dans Quickstart, donner les prérequis, l'installation réellement disponible,
  les étapes de configuration nécessaires puis la commande de démarrage avec
  `--connector <id>`. Privilégier `yamcps configs set` pour les paramètres en clair
  et `yamcps secrets set` pour le vault ; aucun export ni secret en argument requis.
  Inclure l'ingestion préalable si nécessaire et un exemple d'utilisation court.
  Ne pas proposer une installation PyPI si le plugin n'y est pas publié.
- Dans Outils, fournir un tableau `Outil | Description` avec les noms MCP exacts
  des handlers enregistrés, leurs fonctions et leurs effets si pertinents.
- Dans Skills, fournir un tableau `Skill | Description` correspondant aux noms
  et descriptions des `SKILL.md` fournis par `skill_roots()`. Lier les fichiers
  locaux lorsque possible et expliquer leur lecture MCP dans Quickstart si utile.
- Dans Variable de configuration, fournir un tableau
  `Variable | Nom du champ | Description | Obligatoire | Valeur par défaut`.
  Relever les paramètres réellement consommés et les déclarations `ConfigSpec` ;
  vérifier les clés `YAMCPS_*` dans le code plutôt que les déduire approximativement.
  Distinguer une valeur vide autorisée de l'absence de défaut. Expliquer la commande
  de configuration dans Quickstart ; ces clés JSON ne nécessitent pas d'export.
- Dans Secret, fournir un tableau
  `Secret | Nom du champ | Description | Obligatoire` avec les clés exactes et les
  champs utilisés par `SecretSpec` / `ConnectorSecrets`. Décrire leur configuration
  via le vault dans Quickstart ; ne jamais inclure de valeur réelle ni de défaut
  contenant un identifiant sensible. Ne pas classer un secret comme config en clair.
- Garder les quatre tableaux même si une catégorie est vide : utiliser une ligne
  `Aucun` (ou `Aucune` pour les variables) et `—` dans les autres colonnes. Ne pas
  inventer de capacité, de paramètre ou de secret pour remplir une section.
- Préserver les informations utiles d'un README existant en les plaçant dans les
  sections correspondantes ou dans des guides liés ; garder ces six sections de
  niveau 2 et déplacer les détails longs vers la documentation spécialisée.
  Avant livraison, comparer les tableaux au code et vérifier commandes et liens.

