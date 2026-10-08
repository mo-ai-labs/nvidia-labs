import inspect
from typing import Callable, get_type_hints
from pydantic import create_model

from app import data as day2  # Day 2's synthetic ALERTS, POLICIES and calculator


class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, fn: Callable):
        hints = get_type_hints(fn)
        hints.pop("return", None)
        fields = {
            name: (
                hints[name],
                ... if p.default is inspect.Parameter.empty else p.default,
            )
            for name, p in inspect.signature(fn).parameters.items()
        }
        self.tools[fn.__name__] = (fn, create_model(f"{fn.__name__}_args", **fields))
        return fn

    def schemas(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": inspect.getdoc(fn) or "",
                    "parameters": model.model_json_schema(),
                },
            }
            for name, (fn, model) in self.tools.items()
        ]

    def call(self, name: str, raw_args: str) -> str:
        fn, model = self.tools[name]
        args = model.model_validate_json(
            raw_args
        )  # ValidationError -> goes back to the model
        return fn(**args.model_dump())


registry = ToolRegistry()
_flags: dict[str, str] = {}  # stand-in for a case-management API


@registry.register
def get_alert(alert_id: str) -> str:
    """Fetch ONE transaction-monitoring alert by id: customer, pattern, amounts, window. Read-only.
    Unknown ids return an error, never a guess. Example: get_alert(alert_id="A-1001")"""
    return day2.get_alert(alert_id)


@registry.register
def search_policy(query: str) -> str:
    """Search internal AML policies by keywords; returns the 2 best matches with policy ids.
    Call it before deciding what an alert requires. Example: search_policy(query="cash deposits threshold")"""
    return day2.search_policy(query)


@registry.register
def calculator(expression: str) -> str:
    """Exact arithmetic on numbers only (+ - * / **). Use it for every sum or comparison of amounts.
    Example: calculator(expression="9500+9400+9600")"""
    return day2.calculator(expression)


@registry.register
def flag_alert(alert_id: str, reason: str, idempotency_key: str) -> str:
    """Flag an alert for analyst review. SIDE EFFECT. Reuse the same idempotency_key when
    retrying: the same key never creates a second flag."""
    if idempotency_key in _flags:
        return f"already flagged ({_flags[idempotency_key]})"
    _flags[idempotency_key] = f"{alert_id}: {reason}"
    return f"flagged {alert_id}"
