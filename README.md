# Fleet Ops on Google Workspace: discovery, value model, and a 6-week pilot

A worked solutions-engineering engagement for a fictional regional delivery fleet (**Blue Ridge Delivery Co.**, 50 vehicles, three depots). It covers the whole arc: discover the problem, price it, demo a fix, and propose a pilot with a pre-agreed pass/fail bar.

**Author:** Alberto Escalante · [LinkedIn](https://www.linkedin.com/in/albertoantonioescalante/)
Everything here is synthetic. No real customer, driver, or vehicle data.

## The scenario in one paragraph
Schedules live on a whiteboard, so drivers phone the Ops Manager to confirm shifts. Service intervals slip, and a missed oil change becomes a roadside breakdown, a tow, and days without the van. Inspection and service records are on paper, so an audit means a scramble. The proposal is Calendar + Forms + Sheets + Drive on the phones drivers already carry, with no new hardware.

## What's in the repo
| Path | What it shows |
|---|---|
| [`case/customer-brief.md`](case/customer-brief.md) | The fictional customer, stakeholders, and what each cares about |
| [`discovery/agenda-30min.md`](discovery/agenda-30min.md) | A 30-minute meeting where the first 9 minutes are discovery |
| [`demo/talk-track.md`](demo/talk-track.md) | A "driver's day" demo narrative tied to each pain point |
| [`value-model/`](value-model) | Runnable ROI model (`model.py`), inputs with sources, and the fleet status logic (`tracker.py`) |
| [`value-model/assumptions.md`](value-model/assumptions.md) | Every input, its low/base/high values, and where it came from |
| [`pilot/pilot-plan.md`](pilot/pilot-plan.md) | Scope, measures, targets, and the "hit 4 of 5" decision rule |
| [`sample-data/`](sample-data) | Synthetic vehicle and service-log CSVs the tracker runs on |
| [`tests/`](tests) | 5 unit tests tying the model to the numbers in this README |

## Headline numbers (50 vehicles)
Run `python3 value-model/model.py`:

| Scenario | Annual value | Hard savings | Year-one cost | Value-to-cost |
|---|---|---|---|---|
| Low | $21,478 | $12,088 | $7,980 | 2.7x |
| **Base** | **$38,028** | **$21,216** | **$7,980** | **4.8x** |
| High | $64,793 | $31,633 | $7,980 | 8.1x |

Base-case payback on hard savings alone is about 4.5 months. Fines are not counted.

Design choices worth noting:
- **Hard dollars are separated from capacity.** Hard dollars are cash not spent (repairs, tows, downtime). Capacity is staff hours returned, valued at loaded labor cost. Finance can book the first; the second is a softer claim, and the model says so.
- **Savings are deliberately conservative.** The preventive-maintenance savings figure is half of the published range, because some PM is already being done.
- **Inputs are placeholders until discovery.** Every base value is replaced with the customer's actuals, then re-run.

## Run it
```bash
python3 value-model/model.py                   # all three scenarios
python3 value-model/model.py --scenario base
python3 value-model/tracker.py                 # fleet status + spend KPIs from sample-data/
python3 -m unittest discover -s tests          # stdlib only, no installs
```

## Honest limits
- **The data is synthetic and the benchmarks are not the customer's.** Published industry figures stand in for actuals. The pilot's first week exists to replace them with invoices.
- **The low case is a floor, not a forecast.** It stacks every input at its low value, which is unlikely to happen at once.
- **Heavy-truck benchmarks are an upper bound.** The breakdown-frequency figure comes from heavy-truck data, so a light-duty fleet may see fewer events. The 20% "avoidable" share is an assumption to check against 12 months of invoices.
- **Workspace is the records and team layer, not telematics.** When odometers entered by drivers become the bottleneck, a telematics platform is the right next layer. The proposal says so rather than overselling.
- **Pricing and plan limits change.** Licence prices and the user cap on Business plans were current when this was built. Re-check before reusing.
- **The Forms and Apps Script automation is not in this repo.** The repo covers the thinking and the numbers, and `tracker.py` reproduces the status logic.
