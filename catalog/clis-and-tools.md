# CLIs & outils agentiques

Les outils eux-mêmes (les « moteurs »), classés indépendamment du LLM sous-jacent.

---

### Claude Code
- **Lien** : `github.com/anthropics/claude-code` · `claude.ai/code`
- **Type** : CLI / extensions IDE agentiques
- **Compatibilité** : Anthropic (Claude)
- **Installation** : CLI, app desktop (Mac/Windows), web, extensions VS Code / JetBrains
- **À quoi ça sert** : agent de dev interactif ; supporte skills, agents, hooks, MCP, plugins.
- **Notes** : c'est mon CLI principal ; config dans `~/.claude`.

---

### Claude Code Usage Monitor (`claude-monitor`)
- **Lien** : `github.com/Maciek-roboblog/Claude-Code-Usage-Monitor` · Licence MIT
- **Type** : CLI de monitoring (package Python `claude-monitor`)
- **Compatibilité** : Claude Code (lit l'usage local de tokens)
- **Installation** : `uv tool install claude-monitor` (aussi `pipx`/`pip install claude-monitor`)
- **À quoi ça sert** : suivi temps réel des tokens/messages/coûts, prédictions et alertes de
  limites. Vues `realtime|daily|monthly|session`, options `--plan`, `--view`, `--once`,
  `--compact`, `--output rich|json|csv`, `--statusline`, `--warehouse` (historique persistant).
- **Installé le** : 2026-08-27 · **version** : 4.0.0 · via `uv` (isolé, dans `~/.local/bin`)
- **Alias** : `claude-monitor`, `claude-code-monitor`, `cmonitor`, `ccmonitor`, `ccm`.

---

<!-- Pistes à documenter (agnosticité) :
### Cursor            — IDE agentique, MCP, .cursorrules
### Aider             — github.com/Aider-AI/aider (CLI multi-LLM)
### Codex CLI         — github.com/openai/codex (CLI OpenAI)
### Gemini CLI        — github.com/google-gemini/gemini-cli
### Cline / Roo Code  — extensions VS Code agentiques
Gabarit :
### Nom
- **Lien** :
- **Type** : CLI / IDE / extension
- **Compatibilité** :
- **Installation** :
- **À quoi ça sert** :
- **Notes** :
-->
