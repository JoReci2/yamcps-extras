# Contrat de rapport de revue, audit et amélioration

Rapporter preuves, constats exploitables et limites sans répéter les conclusions.
Le format et l’emplacement explicitement demandés par l’utilisateur priment.

## Quand produire le rapport

Ce skill est conditionnel : rapport de revue pour examen, audit et amélioration
d’un contenu existant. Une question, une explication ou une création nouvelle
n’impose pas un rapport d’audit ; fournir alors le bilan d’exécution du guide.

Pour trois constats ciblés au maximum, une restitution inline concise suffit :
priorité, emplacement, preuve et action. Dire directement lorsqu’aucun défaut
n’est confirmé. Pour un audit plus large, grouper par priorité et renvoyer au
rapport détaillé. Ne pas cumuler tableau récapitulatif et liste répétant les mêmes
constats ; pas de bordures décoratives, ANSI ou colonnes artificiellement remplies.

## Priorités

| Priorité | Sens | Application aux skills |
| --- | --- | --- |
| P0 | À corriger immédiatement : fonction, sécurité ou build cassé | Instruction dangereuse, contrat faux, référence indispensable cassée |
| P1 | Correction importante : exactitude ou conception | Version normative obsolète, section obligatoire absente, conflit de routage |
| P2 | Amélioration de moindre urgence | Vérification incomplète, scénario manquant, ordre ambigu |
| P3 | Backlog de clarté ou cohérence | Terminologie, relation manquante, détail de style |
| info | Information sans action nécessaire | Force confirmée, limite ou contrôle non applicable |

Évaluer le contexte et l’impact réel, pas un mot-clé seul. Séparer défaut observé
et recommandation. Donner la reproduction ou source suffisante pour vérifier le
constat et expliciter l’incertitude. Une commande proposée n’est pas une commande
exécutée ; une vérification omise n’est pas un succès.

## Rapport sauvegardé

Par défaut, sauvegarder les constats privés sous
`docs/local/audits/extras-skill-creator/<YYYY-MM-DD>-<slug>.md`, sauf instruction
contraire. Ajouter `-2`, `-3`, etc. en cas de collision. Ne pas versionner un rapport
privé implicitement. Sans écriture locale, restituer inline et indiquer la limite.
La revue reste sans édition des skills ; seul le rapport est créé si applicable.

Ouvrir avec skill, cible, mode, date, périmètre, branche et état de vérification.
Grouper par priorité, omettre les groupes vides et numéroter les constats une seule
fois sur tout le document. Exemple adaptable :

```markdown
# Revue du skill <nom>

- Mode : revue / amélioration / audit / optimisation / capitalisation.
- Cible, date, branche, périmètre : <valeurs observées>.
- Vérification : <exécutée, inspectée, omise et pourquoi>.
- Score : <critères satisfaits/applicables, ou non noté - rapport seul>.

## P1

- [ ] **#1 <Titre>**
  - Emplacement : <fichier et ligne, URI ou cible précise>.
  - Preuve : <comportement, impact, reproduction ou source>.
  - Action suggérée : <correction et méthode de vérification>.
  - Correction appliquée : à renseigner après correction vérifiée.

## État final

- Corrigés / ouverts : <comptes>.
- Comparaison avant/après et décisions : <mesures ou absence de baseline>.
- Limites et prochaine action : <faits>.
```

## Appliquer les constats

Un audit seul autorise le rapport, pas l’édition des skills. Si les corrections sont
demandées, traiter dans l’ordre de priorité à l’intérieur du périmètre.
Après une correction vérifiée, cocher `[x]` et remplacer le placeholder par le
changement et sa preuve ; ajouter le commit si utile. Garder ouverts les points
différés ou échoués avec leur raison. Mettre à jour comptes et état final.
Une recommandation n’est pas une correction terminée.

## Mesures sans score artificiel

Pour une édition, donner critères satisfaits/applicables avant et après, nombre de
cas réussis/exécutés et décisions conserver/rejeter. Définir la grille avant le
résultat ; marquer non mesuré si la baseline manque. Pour un audit seul, donner
contrôles structurels et constats par priorité plutôt qu’un score composite.
La qualité de routage, l’exécution des instructions et la découverte MCP sont des
axes distincts. Ne pas convertir un succès du lint en score comportemental.
