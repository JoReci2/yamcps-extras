# Évolutions du moteur yamcps

Référence cible : **0.4.1 stable**, distribution PyPI. Cet historique synthétise
les changements utiles aux plugins ; il ne prétend pas reproduire chaque commit.
Les versions ci-dessous sont des releases du moteur, pas de yamcps-extras.

## 0.4.1 — logs et édition interactive (28 octobre 2026)

- Aucun nouveau hook de connecteur ; les contrats de 0.4.0 restent compatibles.
- `yamcps serve --verbose` active DEBUG pour la hiérarchie `yamcps`, sur stderr ;
  sinon INFO. Utiliser `logging.getLogger("yamcps.connectors.<id>")` sans handler,
  niveau personnalisé ni propagation désactivée. L’API Python laisse la
  configuration des logs à l’hôte ; les logs ne sont pas des notifications MCP.
- Ne journaliser ni secrets, valeurs de configuration, arguments/résultats d’outils,
  corps HTTP, en-têtes d’authentification ni exceptions brutes, même en DEBUG.
  Le moteur ne peut pas assainir les messages arbitraires d’un plugin.
- `configs list` affiche déclarations, descriptions, défauts et valeurs stockées,
  sans résolution de l’environnement, injection de config ou collecte de secrets.
  La sortie redirigée est un TSV avec en-tête ; `NO_COLOR` est respecté.
- `configs edit` et `secrets edit` ouvrent un éditeur JSON dans un terminal.
  `Ctrl+S` enregistre ; `Ctrl+Q`/`Ctrl+C` annulent. Chaînes et clés normalisées,
  sans doublons ; secrets non vides et masqués. Retirer une clé supprime sa valeur.
- Avec `--connector`, la portée est l’ensemble exact des clés déclarées ; les clés
  inconnues et celles des autres connecteurs sont préservées. Sans sélection,
  l’édition globale permet de gérer les anciennes clés sans importer les plugins.
  `secrets edit` utilise le catalogue complet `required_secrets()`, y compris les
  secrets inactifs ; `secrets set` et le démarrage gardent la sélection conditionnelle.
- `ConfigStore.update` et `Vault.update` acceptent `remove` et `expected` :
  suppressions groupées et comparaison du snapshot sous verrou avant mutation.
  Les éditions sont atomiques ; conflit, annulation ou validation invalide ne
  réécrivent pas le fichier. Sans `expected`, la fusion existante reste compatible.
- Utiliser un moteur ≥0.4.1 pour ces commandes et paramètres ; le minimum 0.4.0
  reste suffisant pour un plugin utilisant seulement les secrets conditionnels.
  Redémarrer le serveur après modification ; ne pas recréer ces éditeurs dans le plugin.

Sources : [release v0.4.1](https://github.com/JoReci2/yamcps/releases/tag/v0.4.1),
[contrat et logs](https://github.com/JoReci2/yamcps/blob/v0.4.1/CONTRIBUTING.md),
[commandes CLI](https://github.com/JoReci2/yamcps/blob/v0.4.1/README.md).

## 0.4.0 — secrets conditionnels

- Nouveau hook synchrone facultatif
  `required_secrets_for_configs(configs: ConnectorConfigs) -> Iterable[SecretSpec]`.
  Il sélectionne un sous-ensemble sans doublon du catalogue `required_secrets()`.
- Résolution des configs avant sélection et résolution des secrets ; injection
  toujours `configure(secrets)` puis `configure_configs(configs)`. Ne pas dépendre
  de cette dernière dans le hook de sélection. Sans hook, comportement précédent.
- Les déclarations invalides et hooks async sont refusés. Toutes les sélections
  précèdent les demandes de secrets ; aucun appel réseau dans ces hooks.
- `secrets set` respecte les secrets actifs selon les configs ; un `--name` inactif
  est refusé. Une désactivation ne supprime pas les valeurs du coffre.
- Les outils et skills actifs restent filtrés par le plugin ; redémarrage requis.
- Dépendance des plugins utilisant ce contrat : `yamcps>=0.4.0,<0.5`.

Sources : [distribution 0.4.0](https://pypi.org/project/yamcps/0.4.0/),
[contrat et exemple](https://github.com/JoReci2/yamcps/blob/v0.4.0/CONTRIBUTING.md),
[implémentation](https://github.com/JoReci2/yamcps/blob/v0.4.0/src/yamcps/server.py).

## 0.3.0 — backends RAG détenus par les plugins

- `RetrievalIndex` expose le contrat structurel du backend ;
  `RagConfig(index_factory=...)` permet une factory détenue par le plugin.
- Factory et accès à l’index restent paresseux. Ne pas ouvrir `context.index` au
  démarrage ; le plugin possède la configuration de son backend et de son modèle.
- `Index(source_namespace=...)` et `Document(source_namespace=...)` permettent des
  citations propres au plugin. Exposer explicitement les ressources de sources.
- Ne pas présenter ces capacités comme nouvelles en 0.4.0 ; elles restent utilisables.

Sources : [contrat 0.3.0](https://github.com/JoReci2/yamcps/blob/v0.3.0/CONTRIBUTING.md),
[changements 0.2.0 → 0.3.0](https://github.com/JoReci2/yamcps/compare/v0.2.0...v0.3.0).

## 0.2.0 — configuration et RAG intégrés

- Configurations non secrètes via `ConfigSpec`, `ConnectorConfigs`,
  `required_configs()` et `configure_configs()` ; stockage JSON et CLI dédiée.
- RAG intégré dans `yamcps.rag`, injection facultative via `RagConfig` et
  `RagContext` ; aucun package `yamcps_rag_core` séparé à utiliser.
- Téléchargement explicite de modèles par CLI ; aucun téléchargement automatique
  au démarrage. L’extra `rag` fournit les dépendances sémantiques facultatives.
- Extraction des plugins métier dans des distributions autonomes ; ne pas importer
  leurs implémentations depuis le moteur. Version de distribution dérivée des tags Git.

Sources : [contrat 0.2.0](https://github.com/JoReci2/yamcps/blob/v0.2.0/CONTRIBUTING.md),
[changements 0.1.0 → 0.2.0](https://github.com/JoReci2/yamcps/compare/v0.1.0...v0.2.0).

## 0.1.0 — socle initial

- Découverte par entry points `yamcps.connectors` ; connecteur minimal avec `id`
  et `register(server)`, capacités facultatives pour secrets et skills.
- Composition de plugins et transports MCP stdio/HTTP ; préserver stdout en stdio.
- Les contrats ultérieurs de configuration, RAG et secrets conditionnels ne doivent
  pas être supposés disponibles sur cette version.

Source : [sources versionnées 0.1.0](https://github.com/JoReci2/yamcps/tree/v0.1.0).
