"""Reorder fictional evidence blocks and independently score hand-authored responses."""
import argparse
import collections
import hashlib
import json
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "fixtures" / "context_panel.json"
POSITIONS = {"front": 0, "middle": 2, "end": 4, "absent": 2}


def get_packet(case, position, visible_blocks=5):
    """Return selected blocks, optionally simulating an explicit prefix-limited packer."""
    if position not in POSITIONS or type(visible_blocks) is not int or not 0 <= visible_blocks <= 5:
        raise ValueError("Give a known condition and 0 through 5 visible blocks.")
    blocks = list(case["fillers"])
    if len(blocks) != 4:
        raise ValueError("The panel requires exactly four filler blocks.")
    target = case["absent"] if position == "absent" else case["target"]
    blocks.insert(POSITIONS[position], target)
    return blocks[:visible_blocks]


def required_ids(case):
    return {record["id"] for record in case["target"]["records"]}


def visible_ids(blocks):
    return {record["id"] for block in blocks for record in block["records"]}


def serialize(case, blocks):
    """Render fixed boundaries and a stable question; byte count is not a token count."""
    result = [
        "Using only the listed case records, identify access and deadline.",
        "Return answer with the exact two supporting IDs, or insufficient with no facts or citations.",
        "Never use an archived, unrelated, or missing record as support.",
        "QUESTION: " + case["question"],
    ]
    for block in blocks:
        result.append("BLOCK " + block["id"])
        result.extend(record["id"] + ": " + record["text"] for record in block["records"])
        result.append("END BLOCK")
    return "\n".join(result) + "\n"


def plan(case, position, visible_blocks=5):
    packet = get_packet(case, position, visible_blocks)
    rendered = serialize(case, packet)
    payload = rendered.encode("utf-8")
    return {
        "case": case["id"],
        "position": position,
        "included_blocks": [block["id"] for block in packet],
        "visible_record_ids": sorted(visible_ids(packet)),
        "complete_support_present": required_ids(case) <= visible_ids(packet),
        "utf8_bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "text": rendered,
    }


def evaluate(case, blocks, candidate):
    complete = required_ids(case) <= visible_ids(blocks)
    if not isinstance(candidate, dict) or set(candidate) != {"state", "facts", "evidence"}:
        return "bad_shape"
    if candidate["state"] == "insufficient":
        if candidate["facts"] != {} or candidate["evidence"] != []:
            return "bad_shape"
        return "unjustified_abstention" if complete else "supported_abstention"
    if candidate["state"] != "answer" or not isinstance(candidate["facts"], dict):
        return "bad_shape"
    ids = candidate["evidence"]
    if (type(ids) is not list or any(type(x) is not str for x in ids)
            or len(set(ids)) != len(ids)):
        return "bad_shape"
    facts = candidate["facts"]
    if set(facts) != {"access", "deadline"} or any(type(v) is not str for v in facts.values()):
        return "bad_shape"
    if not complete:
        return "answer_without_complete_support"
    if set(ids) != required_ids(case):
        return "wrong_evidence"
    return "supported_answer" if facts == case["oracle"] else "wrong_facts"


def score(cases):
    results = {}
    for position in POSITIONS:
        rows = [
            evaluate(case, get_packet(case, position), case["candidates"][position])
            for case in cases
        ]
        counts = dict(sorted(collections.Counter(rows).items()))
        expected = "supported_abstention" if position == "absent" else "supported_answer"
        results[position] = {
            "correct": counts.get(expected, 0), "cases": len(rows),
            "status_counts": counts,
            "cases_by_id": {case["id"]: result for case, result in zip(cases, rows)},
        }
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    show = sub.add_parser("plan", help="Show an input packet without a candidate answer")
    show.add_argument("case", choices=("A", "B", "C"))
    show.add_argument("position", choices=tuple(POSITIONS))
    show.add_argument("--visible-blocks", type=int, default=5)
    sub.add_parser("score", help="Score the authored panel, not a live model")
    opts = p.parse_args()
    cases = json.loads(DATA.read_text(encoding="utf-8"))["cases"]
    if opts.command == "score":
        result = score(cases)
    else:
        case = next(row for row in cases if row["id"] == opts.case)
        try:
            result = plan(case, opts.position, opts.visible_blocks)
        except ValueError as e:
            p.error(str(e))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
