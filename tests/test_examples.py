import copy
from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
import unittest

from lab.check_examples import evaluate_proposal, paired_summary, score_labels


class ExampleChecks(unittest.TestCase):
    def test_read_only_even_when_approved(self):
        state = {"hinge": (1, 4, "R17")}
        proposal = {"item": "hinge", "quantity": 3, "revision": "R17"}
        before = copy.deepcopy(state), copy.deepcopy(proposal)
        self.assertEqual(evaluate_proposal(state, proposal), ("pending", ("read", "pending_review")))
        self.assertEqual(evaluate_proposal(state, proposal, review=True),
                         ("approved_plan", ("read", "pending_review", "review_approved_plan_only")))
        self.assertEqual(evaluate_proposal(state, proposal, review=False)[0], "denied")
        self.assertEqual((state, proposal), before)

    def test_stale_does_not_get_a_retry(self):
        state = {"hinge": (1, 4, "R18")}
        proposal = {"item": "hinge", "quantity": 3, "revision": "R17"}
        self.assertEqual(evaluate_proposal(state, proposal, review=True),
                         ("stale", ("read", "revision_mismatch")))

    def test_retry_is_bounded_even_if_approved(self):
        state = {"hinge": (1, 4, "R17")}
        proposal = {"item": "hinge", "quantity": 3, "revision": "R17"}
        self.assertEqual(evaluate_proposal(state, proposal, transient_failures=1),
                         ("pending", ("transient_read_failure", "read", "pending_review")))
        for count in (2, 5):
            self.assertEqual(evaluate_proposal(state, proposal, review=True, transient_failures=count),
                             ("unavailable", ("transient_read_failure", "transient_read_failure", "stop")))
        self.assertEqual(state, {"hinge": (1, 4, "R17")})

    def test_policy_and_rejection_cannot_be_bypassed_by_approval(self):
        proposal = {"item": "hinge", "quantity": 3, "revision": "R17"}
        inputs = [
            ({"hinge": (2, 4, "R17")}, {**proposal, "quantity": 2}),
            ({"hinge": (1, 4, "R17")}, {**proposal, "quantity": True}),
            ({"hinge": (1, 4, "R17")}, {**proposal, "quantity": 2}),
            ({"hinge": (1, 4, "R17")}, {**proposal, "execute": True}),
            ({"hinge": (1, 4, "R17")}, {**proposal, "item": "unknown"}),
        ]
        for state, bad in inputs:
            self.assertEqual(evaluate_proposal(state, bad, review=True)[0], "invalid")

    def test_timeout_stays_in_denominator(self):
        a = {"old": "pass", "new": "fail", "timeout": "pass"}
        b = {"old": "pass", "new": "pass", "timeout": "timeout"}
        result = paired_summary(a, b)
        self.assertEqual(result["gain"], 0)
        self.assertEqual(result["discordant"], 2)
        self.assertEqual(result["revision_coverage"], Fraction(2, 3))
        self.assertEqual(result["revision_returned_pass_rate"], 1)
        self.assertIsNone(paired_summary({"item": "pass"}, {"item": "timeout"})["revision_returned_pass_rate"])

    def test_malformed_panels_fail_instead_of_disappearing(self):
        with self.assertRaises(ValueError):
            paired_summary({"A": "pass", "B": "pass"}, {"A": "pass"})
        with self.assertRaises(ValueError):
            paired_summary({"A": "pass"}, {"A": "absent"})
        with self.assertRaises(ValueError):
            score_labels({"A": "object"}, {"B": "object"})
        self.assertEqual(score_labels({"A": "object"}, {"A": "object."}), 0)

    def test_documented_cli_numbers(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run([sys.executable, "-B", "lab/check_examples.py"], cwd=root,
                                env={}, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        self.assertEqual(data["labels"], {"direct": 2, "demonstration": 3, "cases": 4})
        self.assertEqual(data["runner"]["reviewed"][0], "approved_plan")
        self.assertEqual(data["comparison"], {
            "cases": 6, "baseline_passes": 3, "revision_passes": 4, "gain": "1/6",
            "improved": 2, "regressed": 1, "discordant": 3, "revision_coverage": "5/6",
            "revision_returned_pass_rate": "4/5",
        })


if __name__ == "__main__":
    unittest.main()
