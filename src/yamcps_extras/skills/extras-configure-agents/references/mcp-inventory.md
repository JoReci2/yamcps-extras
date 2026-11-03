# Inventaire des capacités MCP

Lire quand le projet utilise MCP ou que sa disponibilité doit être établie.
Ne pas exécuter les outils métier pour tester leur présence.

1. Inventorier les serveurs MCP réellement exposés au client et les plugins
   identifiables. Utiliser les capacités de découverte disponibles : `tools/list`,
   `resources/list`, `resources/templates/list` et, seulement si prise en charge,
   l'extension `skills/list` / `skills/get`. Avec un connecteur spécialisé du client,
   utiliser sa découverte équivalente plutôt qu'un appel brut indisponible.
2. Lire les descriptions, schémas, annotations et ressources de documentation
   utiles. Pour les skills, lire les `SKILL.md` pertinents. Dans yamcps, les
   préfixes d'outils/skills aident au regroupement ; les confirmer par la doc ou
   l'inventaire, sans considérer le préfixe comme une preuve suffisante.
3. Distinguer plugin installé, sélectionné dans le serveur, accessible dans cette
   session et retenu pour le projet. La configuration locale seule ne garantit
   pas qu'un plugin fonctionne. Pagination/inventaire partiel, extension absente,
   erreur d'accès ou plugin non identifiable doivent rester explicitement inconnus.
4. Classer chaque capacité : skills (guides à charger), outils (lecture ou
   mutation selon effets documentés), RAG (recherche de passages/citations).
   Un RAG peut être exposé comme outils ou ressources ; ne pas chercher un
   protocole RAG universel ni l'inférer de la seule présence de `yamcps.rag`.
   Ne pas appeler des outils métier pour les tester pendant cet inventaire.
5. Pour chaque plugin retenu, proposer son usage concret : déclencheur, compétence
   à charger, outil exact à appeler, corpus/filtre si connu, résultat attendu,
   limites et niveau d'accord nécessaire. Demander confirmation des usages non
   établis ; ne pas inventer de corpus, d'identifiants ou de droits.
6. Utiliser le tableau suivant dans le brouillon, une ligne par capacité utile
   (plusieurs lignes possibles pour un même plugin). Retirer les éléments non
   retenus après décision ; garder les informations indisponibles comme telles.

| Serveur / plugin | Capacité et nom exact | Quand et pour quoi l'utiliser | Sources / corpus | Limites / accord | État vérifié |
| --- | --- | --- | --- | --- | --- |
| `<serveur / plugin>` | `<skill, outil ou RAG + identifiant>` | `<déclencheur et résultat attendu>` | `<référence connue ou non applicable>` | `<lecture, mutation, restrictions>` | `<accessible, déclaré seulement ou accès non vérifié>` |

Pour un RAG, demander des passages sourcés (document, révision, référence et date
si disponibles), signaler les limites de fraîcheur et l'absence de résultat.
Une récupération documentaire ne prouve pas l'état actuel d'une infrastructure.
Pour les outils, borner les entrées et utiliser le moindre périmètre nécessaire ;
les annotations sont une indication, pas une autorisation de mutation.
Si aucun inventaire n'est accessible, indiquer cette limite et demander seulement
la liste expurgée des capacités nécessaires, sans réclamer tokens ou exports secrets.

