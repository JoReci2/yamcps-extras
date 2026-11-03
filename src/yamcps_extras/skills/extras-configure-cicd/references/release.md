# Livraison depuis le tag de version

Lire seulement pour une livraison demandée. Les contrôles de branches/PR ne
nécessitent ni publication ni image conteneur.


Pour toute construction de livraison (wheel/sdist et image conteneur si demandée),
le tag Git est la source de version. Accepter les versions finales et préversions,
par exemple `v0.1.0`, `v0.1.0dev1`, `v0.1.0.dev1`, `v0.1.0a1`, `v0.1.0b1`,
`v0.1.0rc1` et les post-releases comme `v0.1.0.post1`.

- Déclencher le build de livraison sur un tag `v*` ou une release associée à ce
  tag, puis valider réellement son format : le filtre `v*` seul ne suffit pas.
  Exiger le préfixe `v` suivi d’une version PEP 440 valide, sans epoch ni suffixe
  local, compatible avec la politique de version du projet. Ne pas limiter le
  validateur aux seules versions finales à trois composantes.
- Extraire le tag de l’événement CI et effectuer le checkout de sa référence
  exacte avec historique et tags. Vérifier que `HEAD` correspond au commit de
  `refs/tags/<tag>` (en déréférençant les tags annotés). Ne pas construire une
  livraison depuis la tête de la branche ou déduire sa version du dernier tag voisin.
- Pour Python, enlever uniquement le `v` initial, normaliser avec
  `packaging.version.Version` et comparer à la version des métadonnées du wheel
  et du sdist. `v0.1.0dev1` et `v0.1.0.dev1` correspondent à `0.1.0.dev1`.
  Avec hatch-vcs, laisser les métadonnées découler du checkout du tag ; refuser
  une version différente ou un suffixe local signalant un build intermédiaire.
- Si une image OCI/Docker est demandée, confirmer Dockerfile, contexte, registre
  et nom d’image. La construire depuis ce même checkout et les artefacts validés,
  puis lui donner **le tag Git exact**, préfixe `v` inclus :
  `<registre>/<image>:v0.1.0` ou `<registre>/<image>:v0.1.0dev1`.
  Vérifier que ce tag respecte aussi les contraintes du registre ; refuser un
  format incompatible plutôt que le transformer silencieusement. Ajouter les
  labels OCI `org.opencontainers.image.version` (tag Git) et
  `org.opencontainers.image.revision` (SHA du commit).
- Tester l’image construite ; transmettre cette même image par artefact ou digest
  au job de publication, sans reconstruction. Publier seulement si demandé.
  Ne pas utiliser le numéro de pipeline ou la branche comme version de livraison,
  ni attribuer `latest` à une préversion. Aucun alias `latest` sans besoin explicite.
- Les builds de contrôle sur branches/PR restent possibles, sans publication sous
  un tag de release. Ne pas ajouter une image à un plugin qui ne la demande pas.

Vérifier les scénarios : finale, développement avec/sans point, alpha/bêta/RC,
tag annoté, tag invalide ou absent, commit différent du tag, métadonnées Python
incohérentes et conservation du tag exact dans l’image. Les cas invalides doivent
échouer avant publication ; un build de branche ne doit pas devenir une release.


## Sources et vérification

Valider les versions Python avec [packaging.version.Version](https://packaging.pypa.io/en/stable/version.html).
Vérifier les règles du registre cible avant de reprendre un tag Git comme tag OCI.
Déclarer `packaging` parmi les dépendances du validateur s’il l’importe ; ne pas
supposer cet outil présent sur tous les runners. Les exemples de versions ne
constituent pas un validateur à recopier sous forme de liste fermée.
