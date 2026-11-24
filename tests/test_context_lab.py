import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

from lab.context_lab import DATA, evaluate, get_packet, plan, required_ids, score, visible_ids


class ContextPanel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = json.loads(DATA.read_text(encoding="utf-8"))["cases"]

    def test_matched_reordering_only(self):
        for case in self.cases:
            variants = [plan(case, pos) for pos in ("front", "middle", "end")]
            self.assertEqual(len({v["utf8_bytes"] for v in variants}), 1)
            self.assertEqual(len({v["sha256"] for v in variants}), 3)
            self.assertEqual(len({tuple(v["visible_record_ids"]) for v in variants}), 1)
            self.assertEqual([x["included_blocks"].index("AUTH") for x in variants], [0, 2, 4])
            for variant in variants:
                self.assertTrue(variant["complete_support_present"])
                self.assertEqual(hashlib.sha256(variant["text"].encode("utf-8")).hexdigest(), variant["sha256"])

    def test_absence_not_mislabeled_as_reordering(self):
        case = self.cases[1]
        blocks = get_packet(case, "absent")
        self.assertFalse(required_ids(case) & visible_ids(blocks))
        self.assertEqual(evaluate(case, blocks, case["candidates"]["absent"]),
                         "answer_without_complete_support")

    def test_middle_truncation_changes_the_experiment(self):
        for case in self.cases:
            self.assertTrue(plan(case, "front", 2)["complete_support_present"])
            self.assertFalse(plan(case, "middle", 2)["complete_support_present"])
            self.assertFalse(plan(case, "end", 2)["complete_support_present"])

    def test_answer_may_be_right_but_evidence_wrong(self):
        case = self.cases[1]
        self.assertEqual(case["candidates"]["middle"]["facts"], case["oracle"])
        self.assertEqual(evaluate(case, get_packet(case, "middle"), case["candidates"]["middle"]),
                         "wrong_evidence")

    def test_malformed_and_mismatched_states(self):
        case = self.cases[0]
        packet = get_packet(case, "front")
        candidate = copy.deepcopy(case["candidates"]["front"])
        candidate["evidence"].append(candidate["evidence"][0])
        self.assertEqual(evaluate(case, packet, candidate), "bad_shape")
        candidate["state"] = "insufficient"
        self.assertEqual(evaluate(case, packet, candidate), "bad_shape")
        self.assertEqual(evaluate(case, packet, {"state": "insufficient", "facts": {}, "evidence": []}),
                         "unjustified_abstention")

    def test_score_retains_paired_ids_and_distinguishes_control(self):
        ranks = score(self.cases)
        self.assertEqual([v["correct"] for v in ranks.values()], [3, 0, 2, 2])
        self.assertTrue(all(v["cases"] == 3 for v in ranks.values()))
        self.assertEqual(ranks["middle"]["status_counts"],
                         {"unjustified_abstention": 1, "wrong_evidence": 2})
        self.assertEqual(ranks["end"]["cases_by_id"]["C"], "wrong_facts")

    def test_cli_does_not_include_candidate_keys_in_plan(self):
        root = Path(__file__).resolve().parents[1]
        args = [sys.executable, "-B", "lab/context_lab.py", "plan", "A", "middle"]
        result = subprocess.run(args, cwd=root, env={}, check=True, capture_output=True, text=True)
        plan_output = json.loads(result.stdout)
        self.assertNotIn("candidates", plan_output)
        self.assertNotIn("oracle", plan_output)
        self.assertTrue(plan_output["complete_support_present"])

    def test_unknown_block_bound(self):
        for index in (-1, 6, True):
            with self.assertRaises(ValueError):
                plan(self.cases[0], "middle", index)


if __name__ == "__main__":
    unittest.main()
