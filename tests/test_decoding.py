import math
from pathlib import Path
import subprocess
import sys
import unittest

from lab.decoding import pick, probabilities


class DecodingLab(unittest.TestCase):
    def test_textbook_weights_and_draw(self):
        logits = (math.log(4), math.log(2), 0)
        plans = ((1, (4, 2, 1), 1), (0.5, (16, 4, 1), 0), (2, (2, math.sqrt(2), 1), 1))
        for temp, weights, expected_pick in plans:
            values = probabilities(logits, temp)
            for actual, weight in zip(values, weights):
                self.assertAlmostEqual(actual, weight / sum(weights))
            self.assertEqual(pick(values, 0.7), expected_pick)

    def test_shared_offset_and_exp_safety(self):
        a = probabilities((1001, 1000, 999), 1)
        b = probabilities((1, 0, -1), 1)
        self.assertEqual(a, b)
        self.assertAlmostEqual(sum(a), 1.0)
        self.assertEqual(pick((0.5, 0, 0.5), 0.5), 2)

    def test_bad_inputs(self):
        for scores, temp in (([], 1), ([float("nan")], 1), ([1], 0), ([1], float("inf"))):
            with self.assertRaises(ValueError):
                probabilities(scores, temp)
        for probs, draw in (((0.1, 0.2), 0.1), ((1,), 1), ((0.9, -0.1, 0.2), 0)):
            with self.assertRaises(ValueError):
                pick(probs, draw)

    def test_documented_run(self):
        root = Path(__file__).resolve().parents[1]
        result = subprocess.run([sys.executable, "-B", "lab/decoding.py"], cwd=root, env={},
                                check=True, text=True, capture_output=True)
        self.assertEqual([line[-1] for line in result.stdout.splitlines()], ["A", "B", "B"])


if __name__ == "__main__":
    unittest.main()
