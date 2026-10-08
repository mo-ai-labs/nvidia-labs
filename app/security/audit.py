import hashlib, json, re, time
from pathlib import Path

LOG = Path(__file__).with_name("audit.jsonl")
SECRET = re.compile(r"(nvapi-[A-Za-z0-9_-]+|ghp_[A-Za-z0-9]+)")


def _last_hash() -> str:
    if not LOG.exists() or LOG.stat().st_size == 0:
        return "genesis"
    return json.loads(LOG.read_text().strip().splitlines()[-1])["hash"]


def record(user: str, tool: str, args: str, status: str) -> None:
    """Append-only: each row carries the previous row's hash, so editing history breaks the chain."""
    row = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "user": user,
        "tool": tool,
        "args": SECRET.sub("[REDACTED]", args),
        "status": status,
        "prev_hash": _last_hash(),
    }
    row["hash"] = hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest()
    with LOG.open("a") as f:
        f.write(json.dumps(row) + "\n")


def verify() -> str:
    rows = LOG.read_text().splitlines() if LOG.exists() else []
    prev = "genesis"
    for i, line in enumerate(rows, 1):
        row = json.loads(line)
        h = row.pop("hash")
        if (
            row["prev_hash"] != prev
            or hashlib.sha256(json.dumps(row, sort_keys=True).encode()).hexdigest() != h
        ):
            return f"TAMPERED at row {i}"
        prev = h
    return f"chain OK ({len(rows)} rows)"  # also right for an empty or missing log
