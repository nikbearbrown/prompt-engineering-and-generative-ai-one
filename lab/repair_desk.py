"""Read and inspect the synthetic repair-desk evidence panel. No model or service."""
import argparse
from datetime import date
import json
from pathlib import Path
import re

DATA = Path(__file__).resolve().parents[1] / "fixtures" / "repair_desk.json"


def words(value):
    return set(re.findall(r"[a-z0-9]+", value.lower()))


def eligible(record, case):
    """Only this desk, this policy type, and the half-open effective period."""
    day = date.fromisoformat(case["day"])
    start = date.fromisoformat(record["effective"])
    end = date.fromisoformat(record["expires"]) if record["expires"] else None
    return (record["desk"] == case["desk"] and record["kind"] == "dropoff"
            and start <= day and (end is None or day < end))


def rank(corpus, case, k):
    """Deliberately simple word-overlap baseline, stable ID as tiebreaker."""
    if type(k) is not int or k < 1:
        raise ValueError("k must be a positive integer")
    query = set(case["keywords"])
    scored = [(len(query & words(record["text"])), record) for record in corpus]
    scored.sort(key=lambda entry: (-entry[0], entry[1]["id"]))
    return [record for score, record in scored[:k] if score > 0]


def decision(passed_records, case):
    """Use only applicable records supplied; keep disagreement visible."""
    mass = case["mass_kg"]
    if type(mass) is not int or mass < 0:
        raise ValueError("mass_kg must be a nonnegative integer in this exercise")
    applicable = [record for record in passed_records if eligible(record, case)]
    ids = sorted(record["id"] for record in applicable)
    if not applicable:
        return {"status": "insufficient", "citations": []}
    limits = {record["limit_kg"] for record in applicable}
    if len(limits) != 1:
        return {"status": "conflict", "citations": ids}
    limit = limits.pop()
    return {"status": "eligible" if mass <= limit else "ineligible",
            "citations": ids, "limit_kg": limit}


def panel(corpus, case, k):
    ranked = rank(corpus, case, k)
    filtered = [record for record in corpus if eligible(record, case)]
    return {
        "case": case["id"],
        "word_overlap": [record["id"] for record in ranked],
        "rank_then_verify": decision(ranked, case),
        "scope_and_date_filter": sorted(record["id"] for record in filtered),
        "filter_then_verify": decision(filtered, case),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", help="Case ID D1 through D6")
    parser.add_argument("-k", type=int, default=1)
    args = parser.parse_args()
    if args.k < 1:
        parser.error("k must be positive")
    data = json.loads(DATA.read_text(encoding="utf-8"))
    for case in data["cases"]:
        if case["id"] == args.case:
            print(json.dumps(panel(data["policies"], case, args.k), indent=2))
            return
    parser.error("unknown case")


if __name__ == "__main__":
    main()
