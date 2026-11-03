# Source, couverture et adaptations

## Correspondance fonctionnelle

Cette matrice décrit la couverture de conception, pas des résultats de tests.
Les références locales ci-dessous sont toutes nommées dans le guide principal.

| Élément de la source | Emplacement local et contenu |
| --- | --- |
| Cas d’usage et exclusions | SKILL.md, sections dédiées ; voisins réels d’Extras et tâches génériques exclues |
| AI Self-Check complet | SKILL.md, auto-contrôle IA : format, style, liberté, dépendances, état, sources, sécurité, preuves |
| Détection de contexte | Workflow commun : collection/autonome, Git, fichiers modifiés, parser YAML |
| Active/deprecated/published | Workflow commun et conventions §2/§12 ; chaînes true/false, notices et erreurs séparées |
| Mode 1 Capture intent | Six étapes de création ; exemples, baseline, entrées/sorties et critères |
| Recherche de domaine | Outils/API/options, versions datées, CVE et supply chain, conformité conditionnelle |
| Draft/validate/write | Frontmatter, structure par effort, comparaison avec voisins et validateurs à entrée réelle |
| Forward-test | Mode 1 et evaluation.md : contexte neuf, cas limite, niveaux disponibles, baseline et boucle |
| Mode 2 Review/improve | Huit étapes, structure, fiabilité, contenu, erreurs IA, périmètre, correction et réévaluation |
| Priorités P0/P1/P2/P3/info | output-contract.md, preuves localisées et distinction recommandations/défauts |
| Mode 3 Audit | Inventaire filtré, comptes, matrice, paires actives, freshness sweep et rapport |
| Fraîcheur à 30 jours | Signal de recherche en domaines rapides ; dates Git/mtime, pas preuve d’obsolescence |
| Mode 4 Optimize | Cinq étapes, tâche en tête, budget, 5 positifs/5 négatifs et sélecteur réel |
| Mode 5 Retrospective | Règles de classe, préférence pour un skill existant, consignes ignorées lues sans force-add |
| Fusion/renommage/retrait | Checklist dédiée, périodes de grâce, modes retenus, anciennes invocations et preuve de publication |
| Run Report | SKILL.md et output-contract.md ; avant/après, keep/reject, omissions et scores non inventés |
| Output Contract | Référence complète adaptée : inline/save, priorités, emplacement privé, constats cochés et totaux |
| Agent Hygiene | Référence dédiée, six contrôles transversaux et contenu candidat traité comme données |
| Design/context/freedom | conventions §1 : budget partagé, liberté par étape, défaut/alternative, diagnostics précis |
| Frontmatter/extensions/headless | conventions §2 : profil, limites, provenance, paths non portable, sans dialogue |
| Structures high/medium/low | conventions §3 et modèle §4 |
| Style/tables/checklists/code | conventions §4 : français, sobriété, code préservé, exemples vérifiés |
| Références un niveau et sommaires | conventions §5, liens directs et lecture conditionnelle |
| Cross-skill patterns | conventions §6 : actifs publiés, relations, frontières et notices |
| AI self-check patterns | conventions §7 : exemples de contrôles par domaine et pertinence |
| Diagnostic pitfalls | conventions §8 : erreurs masquées, causes, métriques, calendrier et improvisation |
| Workflow reliability | conventions §9 : checklist, retour, validate-fix-repeat, plan et boucle d’apprentissage |
| Scripts/dependencies | conventions §10 : exécuter/lire, détection, erreurs utiles, environnement et entrée du runner |
| Model portability | conventions §11 et evaluation.md : tiers réels, baseline, pas de champ model |
| Trigger patterns | conventions §6 et mode 4 : termes naturels, budget cumulé, limites et faux positifs |
| Skill Inventory | conventions §12 : inventaire cible réel ; snapshot amont non utilisé comme catalogue Extras |
| Contrat spécifique yamcps | yamcps-integration.md : catalogue, routage, archives, installation hors sources et transports |

## Adaptations délibérées

- Les guides sont en français. Les règles ASCII et liste de mots interdits imposées
  par le linter de l’amont restent propres à l’amont ; elles ne justifient pas de
  supprimer les accents ni de modifier la syntaxe des commandes.
- Les métadonnées licence/source/date/effort sont conservées pour ce nouveau skill
  et recommandées pour ses créations. Le frontmatter minimal des anciens skills
  d’Extras ne devient pas invalide ; distinguer contrat local, profil portable et
  contrôle réellement effectué par le parseur.
- Les outils et scripts amont (`lint-skills.sh`, `validate-spec.sh`, générateur de
  sommaire) ne sont pas supposés disponibles. Vérifier les outils du projet cible
  ou appliquer la grille et signaler l’absence de validation automatisée.
- Les 43 skills du snapshot amont ne sont pas recopiés comme inventaire actif ni
  présentés comme installés. Le catalogue cible est reconstruit et vérifié.
- Les frontières code-review/repo-audit/prompt-generator/skill-refiner de l’amont
  deviennent des catégories et destinations effectivement disponibles chez le client.
- Les noms de commandes propres à des clients, numéros de version et incidents
  historiques d’exemple ne sont pas importés comme faits actuels non revérifiés.
- Le contrat de rapport garde les priorités, preuves, limites et caractère privé ;
  le chemin par défaut utilise `extras-skill-creator`, et le format demandé prime.
- La capitalisation explicitement autorisée ne redemande pas l’accord pour chaque
  règle. Une proposition hors périmètre reste une proposition.
- L’intégration MCP est ajoutée sans restreindre la création à des skills de plugin.
  Lecture, sélection native, installation locale et déploiement restent distingués.
