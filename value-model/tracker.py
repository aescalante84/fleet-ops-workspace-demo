"""Fleet status + spend KPIs from the sample CSVs. Stdlib only.
Mirrors the Sheets logic: miles-to-service flags and an emergency-spend share.
Usage: python value-model/tracker.py
"""
import csv
import os

DUE_SOON_MI = 1000
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "sample-data")


def status(row):
    left = int(row["service_interval_mi"]) - (int(row["current_odometer"]) - int(row["last_service_odometer"]))
    if row["open_defect"]:
        return "DEFECT OPEN", left
    if left < 0:
        return "SERVICE OVERDUE", left
    if left <= DUE_SOON_MI:
        return "DUE SOON", left
    return "OK", left


def spend(rows):
    total = sum(int(r["cost"]) for r in rows)
    emergency = sum(int(r["cost"]) for r in rows if r["type"] == "emergency")
    planned = [r for r in rows if r["type"] == "planned"]
    on_time = sum(1 for r in planned if r["on_time"] == "yes")
    return {"total": total, "emergency": emergency,
            "emergency_share": round(emergency / total, 2),
            "pm_on_time_rate": round(on_time / len(planned), 2)}


def main():
    with open(os.path.join(ROOT, "vehicles.csv")) as fh:
        vehicles = list(csv.DictReader(fh))
    with open(os.path.join(ROOT, "service_log.csv")) as fh:
        log = list(csv.DictReader(fh))
    for v in vehicles:
        s, left = status(v)
        print(f'{v["unit"]:6s} {s:16s} {left:>6,} mi to service')
    print(spend(log))


if __name__ == "__main__":
    main()
