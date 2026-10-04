"""NCP-AAI W1 D6 Mission 5: race ReAct vs plan-and-execute on the 5 questions.

Writes results.json (full answers + call counts) and trace.log (everything printed),
then prints a scoreboard. Plans are auto-approved so the race runs unattended.
"""

import json
import sys

from plan_execute import solve
from react_from_scratch import run


class Tee:  # print to the console and trace.log at the same time (no `tee` on Windows cmd)
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)

    def flush(self):
        for s in self.streams:
            s.flush()


def main():
    questions = json.load(open("questions.json", encoding="utf-8"))
    results = []
    with open("trace.log", "w", encoding="utf-8") as log:
        sys.stdout = Tee(sys.__stdout__, log)
        try:
            for q in questions:
                print(f"\n===== {q['id']} REACT: {q['question']}")
                react = run(q["question"])
                print(f"\n===== {q['id']} PLAN-AND-EXECUTE")
                pe = solve(q["question"], auto_approve=True)
                results.append(dict(q, react=react, plan_execute=pe))
                json.dump(
                    results, open("results.json", "w", encoding="utf-8"), indent=2
                )
        finally:
            sys.stdout = sys.__stdout__

    print("\n" + "=" * 100)
    print(f"{'Q':4} {'ReAct calls':>11} {'P&E calls':>10}   expected")
    for r in results:
        print(
            f"{r['id']:4} {r['react']['steps']:>11} {r['plan_execute']['llm_calls']:>10}   {r['expected']}"
        )
        print(f"     ReAct: {str(r['react']['answer'])[:160]!r}")
        print(f"     P&E  : {str(r['plan_execute']['answer'])[:160]!r}")
    total_r = sum(r["react"]["steps"] for r in results)
    total_p = sum(r["plan_execute"]["llm_calls"] for r in results)
    print(f"TOTAL {total_r:>10} {total_p:>10}")


if __name__ == "__main__":
    main()
