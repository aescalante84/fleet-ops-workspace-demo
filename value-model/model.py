"""Value model for a fleet-ops pilot. Stdlib only.

Usage:  python value-model/model.py [--inputs value-model/inputs.json] [--scenario base]
Hard dollars = cash not spent. Capacity = staff hours returned, valued at loaded labor cost.
Fines are deliberately NOT counted.
"""
import argparse
import json
import os


def compute(cfg, scenario="base"):
    f, r, c, s = cfg["fleet"], cfg["rates"], cfg["cost"], cfg[scenario]
    # A. shift-call time recovered (manager + driver minutes both saved)
    scale = f["vehicles"] / f["baseline_vehicles"]
    drivers = f["vehicles"] * f["drivers_per_vehicle"]
    staff = round(f["vehicles"] * f["office_staff_per_vehicle"])
    call_hours = s["calls_per_day"] * scale * s["minutes_per_call"] / 60 * f["workdays"] * s["call_reduction"]
    shift_calls = call_hours * (r["manager_loaded_hr"] + r["driver_loaded_hr"])
    # B. preventive maintenance savings
    maint_spend = f["vehicles"] * f["miles_per_vehicle"] * s["maint_per_mile"]
    pm = maint_spend * s["pm_savings"]
    # C. breakdowns, tows, downtime avoided
    events = round(f["vehicles"] * f["miles_per_vehicle"] / cfg["unscheduled_event_every_miles"])  # ~39/yr, rounded as in the pilot deck
    avoided = events * s["avoided_share"]
    per_event = s["tow"] + s["days_out"] * s["cost_per_day_out"]
    breakdowns = avoided * per_event
    # D. audit prep time
    audit = s["audit_hrs_week"] * scale * 52 * s["audit_saved"] * r["manager_loaded_hr"]

    hard = pm + breakdowns
    capacity = shift_calls + audit
    total = hard + capacity

    licenses = (drivers * c["driver_license_mo"] + staff * c["staff_license_mo"]) * 12
    setup = c["setup_hours"] * r["manager_loaded_hr"] + c["training_hrs_per_driver"] * drivers * r["driver_loaded_hr"]
    year_one = licenses + setup
    return {
        "scenario": scenario,
        "A_shift_calls": round(shift_calls), "B_preventive_maintenance": round(pm),
        "C_breakdowns": round(breakdowns), "D_audit_prep": round(audit),
        "hard_savings": round(hard), "capacity_value": round(capacity), "total_value": round(total),
        "year_one_cost": round(year_one),
        "value_to_cost": round(total / year_one, 1),
        "payback_months_hard": round(year_one / (hard / 12), 1),
        "value_per_vehicle": round(total / f["vehicles"]),
        "hard_share": round(hard / total, 2),
    }


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", default=os.path.join(here, "inputs.json"))
    ap.add_argument("--scenario", choices=["low", "base", "high", "all"], default="all")
    a = ap.parse_args()
    cfg = json.load(open(a.inputs))
    names = ["low", "base", "high"] if a.scenario == "all" else [a.scenario]
    for n in names:
        res = compute(cfg, n)
        print(f"--- {n} ---")
        for k, v in res.items():
            if k != "scenario":
                print(f"{k:26s} {v:>10,}" if isinstance(v, int) else f"{k:26s} {v:>10}")


if __name__ == "__main__":
    main()
