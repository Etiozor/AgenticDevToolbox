# Instructions / règles

Fichiers d'instructions portables, par écosystème. Même intention, noms différe
nstructions globales Claude Code. Copie vers `~/.claude/CLAUDE.md`
  sur une nouvelle machine. Contient le câblage du déclencheur `/graphify`.
- **`ponytail-AGENTS.md`** — ruleset « lazy senior dev mode » (MIT, DietrichGebert), version
  instruction-only pour plateformes sans plugin. Sur Claude Code, préférer l'installation via
  marketplace (voir [catalog/frameworks.md](../../catalog/frameworks.md)).

> Les infos volatiles/personnelles (email, date courante) sont injectées par l'environnement
> et **ne doivent pas** être stockées en dur ici.

## Modules (à la carte)

Blocs d'instructions indépendants dans [`modules/`](modules/), à ajouter au fichier de config
de n'importe quel LLM/CLI. Le script est idempotent (il n'ajoute pas un bloc déjà présent) :

```bash
scripts/add-instructions.sh                                   # liste les modules
scripts/add-instructions.sh rigueur-intellectuelle            # -> ~/.claude/CLAUDE.md
scripts/add-instructions.sh rigueur-intellectuelle AGENTS.md  # -> autre cible
```

- **`rigueur-intellectuelle`** — partenaire critique, pas complaisant : vérifie les prémisses,
  corrige les erreurs, indique le niveau de confiance.

Nouveau module = un fichier `modules/<nom>.md` dont la 1re ligne est un titre unique.
