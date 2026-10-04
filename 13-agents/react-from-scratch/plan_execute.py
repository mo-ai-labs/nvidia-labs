"""NCP-AAI W1 D6 (AAI Day 2): plan -> validate -> human gate -> execute.

The planner only plans; check() is the automatic gate; input() is the human gate.
A rejected plan returns before execute() is ever called.
"""

import json, re, sys
from react_from_scratch import client, MODEL, run
from tools import SCHEMAS

ALLOWED = {s["function"]["name"] for s in SCHEMAS}
PLANNER = (
    "You are the PLANNER of a financial-crime investigation agent. Do not answer the question. "
    'Return ONLY JSON: {"goal": str, "steps": [{"n": int, "do": str, "tool": str}], "risks": str}. '
    f'Each step\'s tool is one of {sorted(ALLOWED)} or "none". At most 5 steps.'
)


def make_plan(question):
    text = (
        client.chat.completions.create(
            model=MODEL,
            temperature=1.0,
            top_p=0.95,
            messages=[
                {"role": "system", "content": PLANNER},
                {"role": "user", "content": question},
            ],
        )
        .choices[0]
        .message.content
    )
    return json.loads(
        text[text.find("{") : text.rfind("}") + 1]
    )  # tolerate prose around the JSON


def check(plan):  # automatic validation before any human sees it
    bad = [str(s["n"]) for s in plan["steps"] if s["tool"] not in ALLOWED | {"none"}]
    if bad:
        return f"unknown tool in step(s) {', '.join(bad)}"
    # AML rule (POL-05): a SAR is never filed by the agent; an investigator approves it first.
    if any(
        re.search(r"\b(file|filing|submit)\w*\b.*\bSARs?\b", s["do"], re.I)
        for s in plan["steps"]
    ):
        return "plan files a SAR: only a human investigator may approve that (POL-05)"
    return None


def execute(question, plan):
    notes, calls = [], 1  # 1 = the planner's call
    for s in plan["steps"]:  # each step is a small ReAct run
        r = run(
            f"Overall question: {question}\nDo only this step: {s['do']}\nFindings so far: {json.dumps(notes)}"
        )
        notes.append({"step": s["n"], "result": r["answer"]})
        calls += r["steps"]
    answer = (
        client.chat.completions.create(
            model=MODEL,
            temperature=1.0,
            top_p=0.95,
            messages=[
                {
                    "role": "user",
                    "content": f"Question: {question}\nFindings: {json.dumps(notes)}\n"
                    "Answer in two lines. Say so if the data doesn't contain the answer.",
                }
            ],
        )
        .choices[0]
        .message.content
    )
    return {"answer": answer, "llm_calls": calls + 1, "stopped": "answer"}


def solve(question, auto_approve=False):
    plan = make_plan(question)
    print(json.dumps(plan, indent=2))
    problem = check(plan)
    if problem:
        print("AUTO-REJECTED:", problem)
        return {"answer": None, "llm_calls": 1, "stopped": "rejected"}
    if not auto_approve and input("Approve this plan? [y/N] ").strip().lower() != "y":
        print("Rejected by human: nothing executed.")
        return {"answer": None, "llm_calls": 1, "stopped": "rejected"}
    return execute(question, plan)


if __name__ == "__main__":
    print(json.dumps(solve(" ".join(sys.argv[1:])), indent=2))
