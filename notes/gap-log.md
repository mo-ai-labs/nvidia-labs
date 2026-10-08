# NVIDIA labs gap log

Misses from bets and check questions, each backed by the doc that settles it.

| Date | Day | Miss | Correct answer | Source |
|---|---|---|---|---|
| 2026-10-08 | AAI d07 (W02 D04) | Called a poisoned policy record, and a customer's wire memo read later by the agent, **direct** injection | **Indirect**: the attacker wasn't in the chat. Their text sat in data the agent fetched (`search_policy`, wire records). Test: was the attacker in the conversation? | [OWASP LLM01: Types](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) |
| 2026-10-08 | AAI d07 (W02 D04) | Picked `flag_alert` as the "open-ended extension" | `run_python`: open-ended means it can do anything. `flag_alert` is narrow but has a side effect, so it's an **autonomy** problem (gate it), not a functionality one | [OWASP LLM06: mitigation 3, avoid open-ended extensions](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/) |
