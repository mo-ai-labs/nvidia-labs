from app.tools.registry import registry  # Day 4's tools
from app.security.sandbox import run_python
from app.security.audit import record

registry.register(run_python)  # one more tool: code execution, sandboxed

# Least privilege, decided by the END USER's role, never by what the model asks for.
TOOL_ROLES = {
    "get_alert": {"analyst", "investigator"},
    "search_policy": {"analyst", "investigator"},
    "calculator": {"analyst", "investigator"},
    "run_python": {"investigator"},
    "flag_alert": {"investigator"},
}


def secure_call(user: str, role: str):
    def call(name: str, raw_args: str) -> str:
        if role not in TOOL_ROLES.get(name, set()):
            record(user, name, raw_args, "DENIED")
            return f"ERROR: {user} ({role}) is not allowed to use {name}. Ask a human with the right role."
        try:
            out = registry.call(name, raw_args)
            record(user, name, raw_args, "ok")
            return out
        except Exception as e:
            record(user, name, raw_args, f"error: {type(e).__name__}")
            raise

    return call
