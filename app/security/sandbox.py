import subprocess, uuid

IMAGE = "python:3.12-slim"
TIMEOUT_S = 10  # fixed here, not an argument: the model must not choose its own limit


def run_python(code: str) -> str:
    """Run untrusted Python in a throwaway container: no network, capped memory/CPU/processes,
    read-only filesystem. Returns stdout/stderr (truncated). The container dies with the call."""
    name = f"sbx-{uuid.uuid4().hex[:8]}"
    cmd = [
        "docker",
        "run",
        "--rm",
        "--name",
        name,
        "--network",
        "none",
        "--memory",
        "256m",
        "--cpus",
        "0.5",
        "--pids-limit",
        "64",
        "--read-only",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        IMAGE,
        "python",
        "-c",
        code,
    ]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_S)
        out = (p.stdout + p.stderr).strip()
        return (
            out[:2000]
            if p.returncode == 0
            else f"ERROR (exit {p.returncode}): {out[:1500]}"
        )
    except subprocess.TimeoutExpired:
        subprocess.run(["docker", "kill", name], capture_output=True)
        return f"ERROR: timed out after {TIMEOUT_S}s, container killed"
