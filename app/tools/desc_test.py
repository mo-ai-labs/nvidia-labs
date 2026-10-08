from app.tools.agent import run
from app.tools.registry import registry

Q = "Is alert A-1002 something we must act on, and by when?"
precise = registry.schemas()
vague = [
    {"type": "function", "function": {**s["function"], "description": "Tool."}}
    for s in precise
]

for name, schemas in [("vague", vague), ("precise", precise)]:
    ok = 0
    for i in range(5):
        r = run(Q, schemas=schemas, verbose=False)
        used = set(r["tools_used"])
        good = {"get_alert", "search_policy"} <= used and "5" in (r["answer"] or "")
        ok += good
        print(
            f"{name} run {i + 1}: tools={sorted(used)} steps={r['steps']} {'OK' if good else 'MISS'}"
        )
    print(f"== {name}: {ok}/5 used both tools and gave the 5-business-day deadline\n")
