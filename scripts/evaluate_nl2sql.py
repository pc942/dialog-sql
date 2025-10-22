
import argparse, re, yaml
from services.api.app.sql.compiler import NLCompiler

def normalize(sql: str) -> str:
    return re.sub(r"\s+", " ", sql.lower()).strip()

def main(data_path: str):
    with open(data_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    cases = data.get("cases", [])
    c = NLCompiler()
    ok = 0
    for i, case in enumerate(cases, 1):
        plan = c.compile(case["question"])
        sql = normalize(plan.sql)
        needed = case.get("must_contain", [])
        passed = all(k in sql for k in (s.lower() for s in needed))
        ok += int(passed)
        print(f"[{i}] {'PASS' if passed else 'FAIL'} :: {case['question']}")
        if not passed:
            print("SQL:", sql)
            print("Missing:", [k for k in needed if k not in sql])
    acc = ok / max(1, len(cases))
    print(f"Accuracy: {acc:.2%} ({ok}/{len(cases)})")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    args = ap.parse_args()
    main(args.data)
