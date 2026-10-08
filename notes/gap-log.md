# NVIDIA labs gap log

Misses from bets and check questions, each backed by the doc that settles it.

| Date | Day | Miss | Correct answer | Source |
|---|---|---|---|---|
| 2026-10-08 | AAI d07 (W02 D04) | Called a poisoned policy record, and a customer's wire memo read later by the agent, **direct** injection | **Indirect**: the attacker wasn't in the chat. Their text sat in data the agent fetched (`search_policy`, wire records). Test: was the attacker in the conversation? | [OWASP LLM01: Types](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) |
| 2026-10-08 | AAI d07 (W02 D04) | Picked `flag_alert` as the "open-ended extension" | `run_python`: open-ended means it can do anything. `flag_alert` is narrow but has a side effect, so it's an **autonomy** problem (gate it), not a functionality one | [OWASP LLM06: mitigation 3, avoid open-ended extensions](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) |
| 2026-10-08 | AAI d07 (W02 D04) | Bet A: expected the analyst run to try `flag_alert`, get denied and still repeat the false positive | The analyst run ignored POL-99 entirely; the investigator run believed it and wrote "pre-cleared, false positive, flag it" into the **answer** but never called the tool. Same injection, different outcome per run (temperature 1.0). Role checks stop **actions**, not **words** | [OWASP LLM01: Prevention and Mitigation](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) |
| 2026-10-08 | AAI d07 (W02 D04) | Said the audit chain would stop a hijacked investigator's `flag_alert` | **Nothing** stops it: the role allows it, and an audit log records, it never blocks. Side-effect tools need human approval | [OWASP LLM06: Prevention and Mitigation](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) |
| 2026-10-08 | AAI d07 (W02 D04) | Said retrieval rails check the user's question | Retrieval rails check **retrieved chunks** (POL-99) before the model sees them; input rails check what the user types. Indirect injection arrives through retrieval | [NeMo Guardrails: rail types](https://docs.nvidia.com/nemo/guardrails/latest/user-guides/guardrails-process.html) |
