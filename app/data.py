import ast, json, operator, re

# Synthetic data only
ALERTS = {
    "A-1001": {
        "customer": "Northwind Trading",
        "pattern": "cash deposits",
        "amounts": [9500, 9400, 9600],
        "window_days": 7,
    },
    "A-1002": {
        "customer": "Blue Harbor Imports",
        "pattern": "wires to a high-risk jurisdiction",
        "amounts": [120000, 118500],
        "window_days": 30,
    },
    "A-1003": {
        "customer": "Maple Dental",
        "pattern": "equal payroll payments",
        "amounts": [4200, 4200, 4200],
        "window_days": 30,
    },
}
POLICIES = [  # synthetic internal policies
    (
        "POL-01",
        "Several cash deposits just under the 10,000 reporting threshold within a short window are a structuring red flag: escalate to an investigator.",
    ),
    (
        "POL-02",
        "Cash transactions over 10,000 in one business day require a currency transaction report.",
    ),
    (
        "POL-03",
        "Wires to or from a high-risk jurisdiction above 100,000 require enhanced due diligence within 5 business days.",
    ),
    (
        "POL-04",
        "Regular equal payroll payments to employees are expected activity: close the alert with a note naming the payroll pattern.",
    ),
    (
        "POL-05",
        "Any case recommending a SAR must be approved by a human investigator before filing.",
    ),
]

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        return _OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp):
        return _OPS[type(node.op)](_eval(node.operand))
    raise ValueError("only + - * / ** and numbers are allowed")


def calculator(expression: str) -> str:
    return str(_eval(ast.parse(expression, mode="eval").body))


def get_alert(alert_id: str) -> str:
    return json.dumps(
        ALERTS.get(alert_id.strip().upper(), {"error": f"no alert {alert_id}"})
    )


def search_policy(query: str) -> str:
    words = set(re.findall(r"[a-z0-9]+", query.lower()))
    scored = sorted(
        POLICIES,
        key=lambda p: -len(words & set(re.findall(r"[a-z0-9]+", p[1].lower()))),
    )
    return json.dumps([{"id": pid, "text": text} for pid, text in scored[:2]])


TOOLS = {
    "calculator": calculator,
    "get_alert": get_alert,
    "search_policy": search_policy,
}


def _fn(name, desc, arg, arg_desc):
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": desc,
            "parameters": {
                "type": "object",
                "properties": {arg: {"type": "string", "description": arg_desc}},
                "required": [arg],
            },
        },
    }


SCHEMAS = [
    _fn(
        "calculator",
        "Exact arithmetic. Use for any sum, ratio or comparison of amounts.",
        "expression",
        "e.g. '9500+9400+9600'",
    ),
    _fn(
        "get_alert",
        "Fetch a transaction-monitoring alert (customer, pattern, amounts, window) by id.",
        "alert_id",
        "e.g. A-1001",
    ),
    _fn(
        "search_policy",
        "Search internal AML policies. Returns the two best-matching policies with ids.",
        "query",
        "keywords, e.g. 'cash deposits threshold'",
    ),
]
