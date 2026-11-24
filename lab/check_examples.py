"""Reproduce arithmetic and boundary examples in Chapters 2, 4 and 5.

This module makes no model calls, has no network functions and implements no writer.
"""
from fractions import Fraction
import json


def score_labels(expected, candidate):
    if not expected or expected.keys() != candidate.keys():
        raise ValueError("Both panels need the same nonempty set of IDs.")
    return sum(candidate[i] == expected[i] for i in expected)


def evaluate_proposal(inventory, proposal, *, review=None, transient_failures=0):
    """Return a status and synthetic trace, never an order or inventory write."""
    if review is not None and type(review) is not bool:
        raise ValueError("Review is True, False, or None.")
    if type(transient_failures) is not int or transient_failures < 0:
        raise ValueError("Transient failures must be a nonnegative integer.")
    if type(proposal) is not dict or set(proposal) != {"item", "quantity", "revision"}:
        return "invalid", ("invalid_shape",)
    item, quantity, revision = (proposal[k] for k in ("item", "quantity", "revision"))
    if type(item) is not str or type(quantity) is not int or quantity < 1 or type(revision) is not str:
        return "invalid", ("invalid_type",)

    events = []
    for attempt in range(2):
        if attempt < transient_failures:
            events.append("transient_read_failure")
            continue
        events.append("read")
        break
    else:
        return "unavailable", (*events, "stop")

    if item not in inventory:
        return "invalid", (*events, "unknown_item")
    count, target, current_revision = inventory[item]
    if revision != current_revision:
        return "stale", (*events, "revision_mismatch")
    if count >= 2 or quantity != target - count:
        return "invalid", (*events, "outside_policy")
    events.append("pending_review")
    if review is None:
        return "pending", tuple(events)
    if review is False:
        return "denied", (*events, "review_denied")
    return "approved_plan", (*events, "review_approved_plan_only")


def paired_summary(baseline, revision):
    if not baseline or baseline.keys() != revision.keys():
        raise ValueError("Both panels need the same nonempty set of IDs.")
    allowed = {"pass", "fail", "timeout"}
    if set(baseline.values()) - allowed or set(revision.values()) - allowed:
        raise ValueError("Outcomes must be pass, fail, or timeout.")
    n = len(baseline)
    a = sum(s == "pass" for s in baseline.values())
    b = sum(s == "pass" for s in revision.values())
    gains = sum(baseline[k] != "pass" and revision[k] == "pass" for k in baseline)
    losses = sum(baseline[k] == "pass" and revision[k] != "pass" for k in baseline)
    returned = sum(s != "timeout" for s in revision.values())
    return {
        "cases": n,
        "baseline_passes": a,
        "revision_passes": b,
        "gain": Fraction(b - a, n),
        "improved": gains,
        "regressed": losses,
        "discordant": gains + losses,
        "revision_coverage": Fraction(returned, n),
        "revision_returned_pass_rate": Fraction(b, returned) if returned else None
    }


def main():
    expected = dict(zip(("T1", "T2", "T3", "T4"), ("object", "record", "needs_review", "object")))
    direct = {**expected, "T2": "object", "T3": "record"}
    demonstrated = {**expected, "T3": "record"}
    labels = {"direct": score_labels(expected, direct),
              "demonstration": score_labels(expected, demonstrated), "cases": len(expected)}

    inv = {"hinge": (1, 4, "R17")}
    prop = {"item": "hinge", "quantity": 3, "revision": "R17"}
    runner = {
        "pending": evaluate_proposal(inv, prop),
        "reviewed": evaluate_proposal(inv, prop, review=True),
        "stale": evaluate_proposal(inv, {**prop, "revision": "R16"}),
        "unavailable": evaluate_proposal(inv, prop, transient_failures=2),
    }
    ids = ("E1", "E2", "E3", "E4", "E5", "E6")
    baseline = dict(zip(ids, ("pass", "fail", "pass", "fail", "fail", "pass")))
    revision = dict(zip(ids, ("pass", "pass", "timeout", "pass", "fail", "pass")))
    comparison = paired_summary(baseline, revision)
    print(json.dumps({"labels": labels, "runner": runner, "comparison": comparison}, indent=2, default=str))


if __name__ == "__main__":
    main()
