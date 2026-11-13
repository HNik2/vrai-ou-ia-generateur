# vrai-ou-ia-generateur

Génère, sur les machines gratuites de GitHub Actions, des images d'essai avec
le modèle libre **FLUX.1 [schnell]** (Black Forest Labs, licence Apache 2.0),
exécuté sur processeur par [stable-diffusion.cpp](https://github.com/leejet/stable-diffusion.cpp)
(licence MIT).

- `prompts.json` : la liste des consignes (`id`, `prompt`, `seed`).
- Modifier `prompts.json` et le pousser sur `main` lance le workflow
  « Générer » : les consignes sont réparties entre plusieurs machines, puis
  les images sont rangées sur la branche `sorties` avec `sorties/manifest.json`.
- Aucune clé, aucun secret : le dépôt ne contient que ce code.
