"""Mission 3 follow-up: hide the names too. Tools become t1..t4, descriptions "Tool."."""

from app.tools.agent import run
from app.tools.registry import registry

Q = "Is alert A-1002 something we must act on, and by when?"
real = registry.schemas()
alias = {f"t{i + 1}": s["function"]["name"] for i, s in enumerate(real)}
anon = [
    {
        "type": "function",
        "function": {
            "name": f"t{i + 1}",
            "description": "Tool.",
            # drop the "get_alert_args" title so the name doesn't leak through the schema
            "parameters": {
                k: v for k, v in s["function"]["parameters"].items() if k != "title"
            },
        },
    }
    for i, s in enumerate(real)
]
print(
    "The model sees:",
    [
        (s["function"]["name"], list(s["function"]["parameters"]["properties"]))
        for s in anon
    ],
)


def call(name, args):
    return registry.call(
        alias[name], args
    )  # unknown name -> KeyError -> agent shows it as ERROR


ok = 0
for i in range(5):
    r = run(Q, schemas=anon, call=call, verbose=False)
    used = {alias.get(t, t) for t in r["tools_used"]}
    good = {"get_alert", "search_policy"} <= used and "5" in (r["answer"] or "")
    ok += good
    print(
        f"anon run {i + 1}: tools={sorted(used)} steps={r['steps']} {'OK' if good else 'MISS'}"
    )
print(f"== anon: {ok}/5")
