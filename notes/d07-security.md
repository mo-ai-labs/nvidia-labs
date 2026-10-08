# Day 7 (W02 D04) · Sandbox, least privilege, receipts

> NCP-AAI Phase A · AAI 9.1, 9.4 · paired with GH-600 Day 11
> Deliverable: sandboxed `run_python`, role-based `secure_call`, hash-chained `audit.jsonl`, injection test, layered-safety diagram.

## §1 Bet

**Bet A:** A planted "policy" tells the agent to call `flag_alert` and report a false positive. Logged in as an **analyst** (no flag permission), what happens?

- My guess: **The call is denied, but the answer repeats the false positive**
- Actual: _scored in Mission 4_
- Result: _pending_

## §2 Threats

_Worst case per tool if the agent is hijacked (Mission 1)._

| Tool | Worst thing a hijacked agent could do |
|---|---|
| `get_alert` | Leaks other customers' PII into the answer (data exposure) |
| `search_policy` | Data leak, and it's the **doorway** for indirect injection (POL-99 arrives here) |
| `calculator` | Data leak path only; low risk on its own |
| `flag_alert` | **Both:** mass false flags that bury real cases, and misleading reasons ("cleared by compliance") that poison the audit trail a human trusts later |
| `run_python` | **All of it:** exfiltrate `.env` / `NVIDIA_API_KEY` over the network, take over the host (write files, pivot), burn CPU/RAM with loops or fork bombs |

**Rule of thumb:** a tool with a side effect gets **gated** (who can run it, and when). An open-ended tool gets **boxed in** (what it can reach). `flag_alert` gets gated; `run_python` gets both.

![LLM01 entry vs LLM06 blast radius](img/w02d04-m1-owasp-entry-vs-blast.svg)
*Editable source: [w02d04-m1-owasp-entry-vs-blast.excalidraw](img/w02d04-m1-owasp-entry-vs-blast.excalidraw)*

## §3 Controls

_Which sandbox flag stops which attack, and what's still a worry (Mission 2)._

## §4 Injection test

_Analyst vs investigator runs, which control limited the damage, what got through (Mission 4)._

## §5 Layers

_input filter → policy prompt → constrained tools → output filter → human escalation (Mission 5)._
