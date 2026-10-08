import json, sys
from typing import Literal
from pydantic import BaseModel, Field
from app.tools.agent import client, MODEL
from app.tools.registry import get_alert, search_policy


class Verdict(BaseModel):
    alert_id: str
    typology: Literal["structuring", "high-risk wires", "expected activity", "unclear"]
    action: Literal[
        "escalate", "enhanced due diligence", "close with note", "needs human review"
    ]
    policy_ids: list[str] = Field(
        description="Policy ids that justify the action, e.g. POL-01"
    )
    rationale: str = Field(max_length=300)


def triage(alert_id: str) -> Verdict:
    alert = get_alert(alert_id)  # link 1: the facts
    policies = search_policy(
        json.loads(alert).get("pattern", alert_id)
    )  # link 2: rules picked from link 1's output
    prompt = (
        f"Alert: {alert}\nRelevant policies: {policies}\n"  # link 3: a prompt assembled from state
        "Classify the alert and choose the action the policies require. Use only these facts."
    )
    r = client.chat.completions.create(
        model=MODEL,
        temperature=1.0,
        top_p=0.95,
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
        extra_body={"guided_json": Verdict.model_json_schema()},
    )  # constrained decoding
    return Verdict.model_validate_json(r.choices[0].message.content)


if __name__ == "__main__":
    for a in sys.argv[1:] or ["A-1001", "A-1002", "A-1003"]:
        print(triage(a).model_dump_json(indent=2))
