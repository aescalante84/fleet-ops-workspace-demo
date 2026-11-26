import csv, json, os, sys, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "value-model"))
import model, tracker  # noqa: E402


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.cfg = json.load(open(os.path.join(HERE, "..", "value-model", "inputs.json")))

    def test_base_case(self):
        r = model.compute(self.cfg, "base")
        self.assertEqual(r["total_value"], 38028)
        self.assertEqual(r["hard_savings"], 21216)
        self.assertEqual(r["year_one_cost"], 7980)
        self.assertEqual(r["value_to_cost"], 4.8)
        self.assertEqual(r["payback_months_hard"], 4.5)

    def test_scenarios_are_ordered(self):
        v = [model.compute(self.cfg, s)["total_value"] for s in ("low", "base", "high")]
        self.assertEqual(v, sorted(v))

    def test_value_scales_with_fleet(self):
        self.cfg["fleet"]["vehicles"] = 100
        r = model.compute(self.cfg, "base")
        self.assertEqual(r["total_value"], 76056)      # value is per vehicle
        self.assertEqual(r["year_one_cost"], 14267)    # setup is built once, so cost grows slower
        self.assertEqual(r["value_to_cost"], 5.3)


class TrackerTests(unittest.TestCase):
    def row(self, left_used, defect=""):
        return {"service_interval_mi": "5000", "last_service_odometer": "0",
                "current_odometer": str(left_used), "open_defect": defect}

    def test_flags(self):
        self.assertEqual(tracker.status(self.row(5040))[0], "SERVICE OVERDUE")
        self.assertEqual(tracker.status(self.row(4500))[0], "DUE SOON")
        self.assertEqual(tracker.status(self.row(1000))[0], "OK")
        self.assertEqual(tracker.status(self.row(5040, "tires"))[0], "DEFECT OPEN")

    def test_sample_spend(self):
        with open(os.path.join(HERE, "..", "sample-data", "service_log.csv")) as fh:
            s = tracker.spend(list(csv.DictReader(fh)))
        self.assertEqual(s["total"], 9029)
        self.assertEqual(s["emergency"], 3525)
        self.assertEqual(s["emergency_share"], 0.39)


if __name__ == "__main__":
    unittest.main()
