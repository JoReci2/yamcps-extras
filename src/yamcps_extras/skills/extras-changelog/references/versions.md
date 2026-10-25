# Évolutions du moteur yamcps

Référence cible : **0.4.0 stable**, distribution PyPI. Cet historique synthétise
les changements utiles aux plugins ; il ne prétend pas reproduire chaque commit.
Les versions ci-dessous sont des releases du moteur, pas de yamcps-extras.

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
