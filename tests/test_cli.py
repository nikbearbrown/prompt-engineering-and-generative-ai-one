"""Check the learner-facing CLI, including interactions that look correct."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "fixtures" / "candidates"


class ContractCLI(unittest.TestCase):
    def call(self, scenario, candidate):
        return subprocess.run(
            [sys.executable, "-B", str(ROOT / "validate.py"), scenario, str(candidate)],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )

    def raw(self, scenario, text):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / "candidate.json"
            f.write_text(text, encoding="utf-8")
            return self.call(scenario, f)

    def changed(self, **values):
        candidate = json.loads((CANDIDATES / "A-good.json").read_text())
        candidate.update(values)
        return self.raw("A", json.dumps(candidate))

    def test_five_state_and_boundary_fixtures(self):
        for case, state in zip("ABCDE", ("within_cap", "within_cap", "conflict",
                                        "insufficient_evidence", "over_cap")):
            with self.subTest(case=case):
                result = self.call(case, CANDIDATES / (case + "-good.json"))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("ACCEPT: " + state, result.stdout)
                self.assertIn("no action authorized", result.stdout)

    def test_stale_correct_arithmetic_is_rejected(self):
        p = self.call("A", CANDIDATES / "A-stale.json")
        self.assertEqual(p.returncode, 1)
        self.assertIn("state: expected within_cap", p.stdout)
        self.assertIn("disagrees with source-derived value", p.stdout)

    def test_right_numbers_wrong_provenance(self):
        p = self.call("A", CANDIDATES / "A-unsupported.json")
        self.assertEqual(p.returncode, 1)
        self.assertIn("evidence:", p.stdout)
        self.assertNotIn("state:", p.stdout)

    def test_null_numbers_for_conflict(self):
        p = self.call("C", CANDIDATES / "C-invented.json")
        self.assertEqual(p.returncode, 1)
        self.assertIn("must be null", p.stdout)

    def test_exact_cap_is_within_cap(self):
        q = json.loads((CANDIDATES / "B-good.json").read_text())
        q["state"] = "over_cap"
        p = self.raw("B", json.dumps(q))
        self.assertEqual(p.returncode, 1)
        self.assertIn("state: expected within_cap", p.stdout)

    def test_duplicate_same_value_is_not_a_conflict(self):
        q = json.loads((CANDIDATES / "B-good.json").read_text())
        q["state"] = "conflict"
        for k in ("seats", "unit_cents", "cap_cents", "total_cents"):
            q[k] = None
        self.assertIn("state: expected within_cap", self.raw("B", json.dumps(q)).stdout)

    def test_conflict_precedes_missingness(self):
        q = json.loads((CANDIDATES / "C-good.json").read_text())
        q["state"] = "insufficient_evidence"
        p = self.raw("C", json.dumps(q))
        self.assertEqual(p.returncode, 1)
        self.assertIn("state: expected conflict", p.stdout)

    def test_almost_correct_total(self):
        p = self.changed(total_cents=8549)
        self.assertEqual(p.returncode, 1)
        self.assertIn("total_cents:", p.stdout)

    def test_exact_integer_not_boolean_or_float(self):
        for v in (True, 18.0, -1, None):
            with self.subTest(value=v):
                p = self.changed(seats=v)
                self.assertEqual(p.returncode, 1)
                self.assertIn("must be a nonnegative integer", p.stdout)

    def test_evidence_duplicates(self):
        p = self.changed(evidence=["A-PRICE", "A-CAP", "A-NOW", "A-NOW"])
        self.assertEqual(p.returncode, 1)
        self.assertIn("repeated identifier", p.stdout)

    def test_malformed_and_nonportable_json(self):
        for s in ('{"state":"x", "state":"y"}', '{"seats":NaN}', 'not json', '{"seats":Infinity}'):
            with self.subTest(candidate=s):
                p = self.raw("A", s)
                self.assertEqual(p.returncode, 1)
                self.assertIn("malformed candidate JSON", p.stdout)

    def test_no_action_or_else_key(self):
        p = self.changed(approve_purchase=True)
        self.assertEqual(p.returncode, 1)
        self.assertIn("exactly the contract keys", p.stdout)

    def test_wrong_shape_and_state(self):
        self.assertEqual(self.raw("A", "[]").returncode, 1)
        self.assertEqual(self.changed(state=["within_cap"]).returncode, 1)

    def test_scenario_and_path_errors(self):
        self.assertEqual(self.call("UNKNOWN", CANDIDATES / "A-good.json").returncode, 2)
        self.assertEqual(self.call("A", CANDIDATES / "missing.json").returncode, 2)


if __name__ == "__main__":
    unittest.main()
