import re
import xml.etree.ElementTree as ET
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class VisualEvidence(unittest.TestCase):
    def test_chart_proportions_and_labels_match_equivalent_text(self):
        doc = ET.parse(ROOT / "assets" / "c24-r4.svg").getroot()
        bars = {
            (r.get("data-room"), r.get("data-week")):
                (int(r.get("data-items")), int(r.get("width")))
            for r in doc.iter()
            if r.get("data-items")
        }
        self.assertEqual(bars, {
            ("east", "1"): (8, 216), ("east", "4"): (14, 378),
            ("west", "1"): (12, 324), ("west", "4"): (16, 432),
        })
        chapter = (ROOT / "chapters" / "09-operate-multimodal-workflows.md").read_text()
        rows = re.findall(r"^(East|West), Week ([14]): +([#]+) +printed value (\d+)$",
                          chapter, re.M)
        self.assertEqual(len(rows), 4)
        for room, week, text_map, label in rows:
            self.assertEqual((len(text_map), 27 * int(label)), bars[(room.lower(), week)])
        self.assertIn("C24 R4. East: 8 items in Week 1 and 14 in Week 4.", chapter)
        self.assertIn("West: 12 items in Week 1 and 16 in Week 4.", chapter)

    def test_image_has_title_and_long_description(self):
        ns = {"s": "http://www.w3.org/2000/svg"}
        doc = ET.parse(ROOT / "assets" / "c24-r4.svg")
        self.assertIn("C24 R4", doc.find("s:title", ns).text)
        self.assertIn("not a cumulative total", doc.find("s:desc", ns).text)
        self.assertEqual(doc.getroot().get("aria-labelledby"), "chart-title chart-desc")


if __name__ == "__main__":
    unittest.main()
