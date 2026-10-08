# nvidia-labs

One agent codebase for the NCP-AAI and NCP-GENL study plans: a financial-crime investigation agent built up day by day on
hosted NIM models.

> **Synthetic data only.** Every alert, customer, amount and policy in this repo is invented.

## Layout

| Path | What lives there |
|---|---|
| `app/` | The agent, one Python package. Each day adds a module: `reasoning/` (ReAct, plan-and-execute, prompt chain), `tools/` (registry, agent loop, verdict), `mcp/`, `security/`, … `data.py` holds the synthetic alerts and policies. |
| `app/a2a/` | The A2A agent card |
| `workflows/` | NeMo Agent Toolkit configs, one folder per workflow |
| `notes/` | Day notes: `dNN-<topic>.md` for AAI days, `gNN-<topic>.md` for GENL days, `d00-*` for the foundations week. Living docs (`term-map.md`, `gap-log.md`, readiness, cheatsheets) have no prefix. Diagrams in `notes/img/`. |

## Run it

```powershell
uv sync                      # installs app/ in editable mode, plus the shared deps
cd app/tools
uv run python agent.py "Alert A-1001: total the cash deposits and name the policy"
```

`app` is an installed package, so modules import each other as `from app.tools.registry import registry` from any
folder. Scripts run from their own folder, so the files they write land next to them. API keys come from the nearest
`.env` above the script.
