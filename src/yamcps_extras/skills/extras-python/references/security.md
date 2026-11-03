# Sécurité des plugins Python

Appliquer les recommandations ANSSI pertinentes au périmètre du plugin et à son
exploitation. Identifier avec le responsable du projet les référentiels, versions
et exigences contractuelles applicables. Les règles Python ci-dessous constituent
une déclinaison pour yamcps des guides cités, pas un référentiel Python officiel
ANSSI. Un résultat Bandit ne suffit pas à établir une conformité globale,
une certification ou une homologation.

### Conception et protection des données

- Identifier les données sensibles, frontières de confiance, accès métier et effets
  des outils MCP. Appliquer le moindre privilège aux comptes techniques, fichiers,
  services et permissions CI ; séparer développement, tests et production.
- Contrôler les autorisations côté service pour chaque opération sensible ; une
  annotation MCP, un corpus RAG ou un paramètre fourni par le modèle ne constitue
  pas un contrôle d’accès. Refuser par défaut une opération non autorisée.
- Valider types, tailles, formats et valeurs des entrées. Borner requêtes, réponses,
  délais et ressources consommées. Utiliser des requêtes SQL paramétrées, éviter
  `eval`/`exec` sur des données non fiables et les commandes shell interpolées.
  Refuser les chemins sortant des racines autorisées et la désérialisation non sûre.
- Pour les URL configurables, contrôler destinations et redirections selon les
  services autorisés afin de limiter les SSRF ; documenter les accès locaux requis.
- Utiliser le coffre yamcps pour les secrets, jamais des valeurs codées en dur ou
  une configuration en clair. Masquer tokens et données sensibles dans les logs,
  exceptions, réponses MCP et rapports de tests ; minimiser stockage et conservation.
- Vérifier certificats et noms d’hôte pour les connexions TLS ; ne pas désactiver
  leur validation. Utiliser les mécanismes cryptographiques éprouvés du moteur et
  des bibliothèques maintenues, sans concevoir de cryptographie propre au plugin.
- Conserver HTTP sur loopback par défaut. Pour un accès distant demandé, définir
  authentification, protection des flux et filtrage dans l’architecture de
  déploiement ; ne pas supposer que le plugin fournit ces protections.

### Dépendances, traçabilité et vérification

- Utiliser des sources de dépendances maîtrisées et des versions maintenues ;
  tracer les versions livrées et leurs dépendances, avec un inventaire ou SBOM
  selon le contexte. Analyser les changements et appliquer les correctifs de
  sécurité ; contrôler aussi la chaîne de construction et les artefacts livrés.
- Journaliser les événements de sécurité utiles (refus d’accès, erreurs de
  validation et opérations sensibles) avec un contexte permettant l’investigation,
  sans secret ni contenu métier sensible. Protéger accès, intégrité et rétention
  des journaux selon les responsabilités du plugin et de l’exploitant.
- Combiner revue humaine, Bandit et tests unittest des entrées malveillantes,
  refus d’autorisation, fuites de secrets et erreurs des services externes. Ajouter
  les tests dynamiques pertinents pour les interfaces réellement exposées.
- Consigner pour chaque exigence applicable : source/version, mesure implémentée,
  preuve de vérification et écart éventuel. Faire valider les dérogations par le
  responsable sécurité désigné et signaler les contrôles manquants. Ne déclarer
  une conformité que pour un périmètre évalué avec des preuves explicites.

Références ANSSI :

- [Guide d’hygiène informatique](https://messervices.cyber.gouv.fr/guides/guide-dhygiene-informatique) : socle de protection et suivi des mesures.
- [Guide de cybersécurité à l’usage des start-up du numérique](https://messervices.cyber.gouv.fr/documents-guides/guide_cybersecurite_start-up_numerique_FR_v1.pdf) : conception sécurisée, chaîne d’intégration, SAST, dépendances/SBOM et gestion des secrets.

