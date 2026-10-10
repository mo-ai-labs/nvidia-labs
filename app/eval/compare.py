import json, sys

# python compare.py report-<old>.json report-<new>.json
old, new = (json.load(open(p)) for p in sys.argv[1:3])
print(
    f"{old['version']} {old['pass_rate']:.0%} -> {new['version']} {new['pass_rate']:.0%}"
)
before = {r["id"]: r["pass"] for r in old["rows"]}
broke = [r["id"] for r in new["rows"] if before.get(r["id"]) and not r["pass"]]
fixed = [r["id"] for r in new["rows"] if before.get(r["id"]) is False and r["pass"]]
print("PASS -> FAIL:", ", ".join(broke) or "none")
print("FAIL -> PASS:", ", ".join(fixed) or "none")
print(f"{len(broke)} task(s) flipped from PASS to FAIL")
