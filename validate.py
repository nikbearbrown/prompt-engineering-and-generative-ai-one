"""Offline checker for a single fictional teaching contract; no model or tools."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
FIELDS = ("seats", "unit_cents", "cap_cents")
NUMERIC = (*FIELDS, "total_cents")
STATES = {"within_cap", "over_cap", "conflict", "insufficient_evidence"}
OUT_KEYS = {"state", "evidence", *NUMERIC}


def unique_object(pairs):
    out = {}
    for key, val in pairs:
        if key in out:
            raise ValueError(f"duplicate JSON member {key!r}")
        out[key] = val
    return out


def invalid_constant(value):
    raise ValueError(f"non-JSON constant {value}")


def load_json(path):
    with path.open(encoding="utf-8") as f:
        return json.load(f, object_pairs_hook=unique_object, parse_constant=invalid_constant)


def oracle(records):
    buckets = {key: set() for key in FIELDS}
    ids, seen = [], set()
    if not isinstance(records, list):
        raise ValueError("fixture records must be an array")
    for r in records:
        if not isinstance(r, dict) or set(r) != {"id", "field", "value", "authority"}:
            raise ValueError("malformed fixture record")
        rid, field, value, authority = (r[k] for k in ("id", "field", "value", "authority"))
        if not isinstance(rid, str) or not rid or rid in seen:
            raise ValueError("missing or repeated record ID in fixture")
        seen.add(rid)
        if not isinstance(field, str) or field not in FIELDS:
            raise ValueError("unknown fixture field")
        if not isinstance(authority, str) or authority not in {"current", "archived", "informal"}:
            raise ValueError("unknown fixture authority")
        if type(value) is not int or value < 0:
            raise ValueError("fixture requires nonnegative integer values")
        if authority == "current":
            ids.append(rid)
            buckets[field].add(value)
    out = dict.fromkeys(NUMERIC)
    out["evidence"] = ids
    if any(len(v) > 1 for v in buckets.values()):
        out["state"] = "conflict"
    elif any(not v for v in buckets.values()):
        out["state"] = "insufficient_evidence"
    else:
        out.update((key, next(iter(values))) for key, values in buckets.items())
        out["total_cents"] = out["seats"] * out["unit_cents"]
        out["state"] = "within_cap" if out["total_cents"] <= out["cap_cents"] else "over_cap"
    return out


def review(candidate, expected):
    if not isinstance(candidate, dict) or candidate.keys() != OUT_KEYS:
        return ["candidate must be an object with exactly the contract keys"]
    errors = []
    state = candidate["state"]
    if not isinstance(state, str) or state not in STATES:
        return ["unknown decision state"]
    if state != expected["state"]:
        errors.append(f"state: expected {expected['state']}")
    for k in NUMERIC:
        v = candidate[k]
        if state in {"conflict", "insufficient_evidence"}:
            if v is not None:
                errors.append(f"{k}: must be null for unresolved evidence")
        elif type(v) is not int or v < 0:
            errors.append(f"{k}: must be a nonnegative integer")
        if type(v) is type(expected[k]) and v != expected[k]:
            errors.append(f"{k}: disagrees with source-derived value")
    ids = candidate["evidence"]
    if not isinstance(ids, list) or any(not isinstance(i, str) for i in ids):
        errors.append("evidence: expected an array of identifier strings")
    elif len(set(ids)) != len(ids):
        errors.append("evidence: repeated identifier")
    elif set(ids) != set(expected["evidence"]):
        errors.append("evidence: cite all and only the current records for the decision")
    return errors


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("scenario")
    p.add_argument("candidate", type=Path)
    args = p.parse_args(argv)
    try:
        scenarios = load_json(ROOT / "fixtures" / "scenarios.json")
        if not isinstance(scenarios, dict) or args.scenario not in scenarios:
            raise ValueError("unknown scenario")
        expected = oracle(scenarios[args.scenario])
    except (OSError, ValueError, RecursionError) as e:
        print(f"INPUT ERROR: scenario: {e}", file=sys.stderr)
        return 2
    try:
        candidate = load_json(args.candidate)
    except OSError as e:
        print(f"INPUT ERROR: candidate: {e}", file=sys.stderr)
        return 2
    except (ValueError, RecursionError) as e:
        print(f"REJECT: malformed candidate JSON: {e}")
        return 1
    errors = review(candidate, expected)
    if errors:
        print("REJECT: " + "; ".join(errors))
        return 1
    print(f"ACCEPT: {expected['state']} (fictional planning exercise, no action authorized)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
