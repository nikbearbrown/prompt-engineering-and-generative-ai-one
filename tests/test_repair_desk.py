import json
from pathlib import Path
import subprocess
import sys
import unittest

from lab.repair_desk import DATA, decision, eligible, panel, rank


class EvidenceLab(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        data = json.loads(DATA.read_text(encoding="utf-8"))
        cls.policies = data["policies"]
        cls.cases = {case["id"]: case for case in data["cases"]}

    def test_retriever_can_miss_what_corpus_has(self):
        result = panel(self.policies, self.cases["D1"], 1)
        self.assertEqual(result["word_overlap"], ["N-2"])
        self.assertEqual(result["rank_then_verify"], {"status": "insufficient", "citations": []})
        self.assertEqual(result["filter_then_verify"], {
            "status": "eligible", "limit_kg": 12, "citations": ["N-1"]
        })

    def test_date_boundary_discards_older_rule(self):
        result = panel(self.policies, self.cases["D2"], 1)
        self.assertEqual(result["word_overlap"], ["N-0"])
        self.assertEqual(result["rank_then_verify"]["status"], "insufficient")
        self.assertEqual(result["filter_then_verify"]["status"], "ineligible")
        self.assertEqual(panel(self.policies, self.cases["D3"], 1)["filter_then_verify"], {
            "status": "eligible", "limit_kg": 15, "citations": ["N-0"]
        })

    def test_conflict_does_not_disappear_because_both_rules_disallow_11(self):
        result = panel(self.policies, self.cases["D4"], 1)
        self.assertEqual(result["rank_then_verify"]["status"], "ineligible")
        self.assertEqual(result["filter_then_verify"], {
            "status": "conflict", "citations": ["S-1", "S-2"]
        })
        self.assertEqual(panel(self.policies, self.cases["D4"], 2)["rank_then_verify"]["status"], "conflict")

    def test_expiration_and_missing_desk(self):
        self.assertEqual(panel(self.policies, self.cases["D5"], 1)["filter_then_verify"], {
            "status": "eligible", "limit_kg": 8, "citations": ["S-1"]
        })
        result = panel(self.policies, self.cases["D6"], 5)
        self.assertEqual(result["scope_and_date_filter"], [])
        self.assertEqual(result["filter_then_verify"]["status"], "insufficient")

    def test_presentation_order_does_not_change_decision(self):
        case = self.cases["D4"]
        self.assertEqual(panel(self.policies, case, 3), panel(list(reversed(self.policies)), case, 3))
        with self.assertRaises(ValueError):
            rank(self.policies, case, 0)
        with self.assertRaises(ValueError):
            decision(self.policies, {**case, "mass_kg": True})

    def test_cli_actual_output_and_usage(self):
        root = Path(__file__).resolve().parents[1]
        command = [sys.executable, "-B", "lab/repair_desk.py"]
        good = subprocess.run(command + ["D4", "-k", "2"], cwd=root, env={}, text=True,
                              capture_output=True, check=True)
        self.assertEqual(json.loads(good.stdout)["rank_then_verify"]["status"], "conflict")
        bad = subprocess.run(command + ["D0"], cwd=root, env={}, text=True, capture_output=True)
        self.assertEqual(bad.returncode, 2)
        self.assertIn("unknown case", bad.stderr)


if __name__ == "__main__":
    unittest.main()
