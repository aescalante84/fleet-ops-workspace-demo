# Assumptions and sources

Base case unless noted. Replace with customer actuals from discovery.

| Input | Low / Base / High | Source or basis |
|---|---|---|
| Fleet | 50 vehicles, 50 drivers, 8 office staff, 30,000 mi/vehicle/yr | Assumption: replace with actuals |
| Loaded labor rate | Ops/compliance $42.34/hr; drivers $29.71/hr | BLS OEWS median wages x 1.40 benefits load (BLS ECEC, South) |
| Routine shift calls | 20 / 30 / 40 per day, 3-4 min each | Assumption: counted in pilot baseline week |
| Call reduction | 40 / 50 / 60% | Pilot target, measured against baseline |
| Maintenance spend | $0.10 / $0.13 / $0.15 per mile | Light-duty ranges; ATRI heavy-truck $0.215/mi as a ceiling |
| PM savings | 6 / 7.5 / 9% of spend | DOE FEMP: PM saves 12-18% vs. reactive; halved because some PM is already done |
| Unscheduled events | About 39/yr (1 per 38,249 mi); 15 / 20 / 25% avoidable | ATRI via Geotab (heavy trucks, an upper bound); avoidable share is an assumption to check against invoices |
| Cost per event | Tow $265 + 2 days x $130 / $290 / $448 | Published tow and rental-van rates; low end of the downtime range cited by FMCSA |
| Audit filing time | 2 / 3 / 4 hrs/week, half saved | Assumption: timed in the pilot |
| Licences | $7 per driver, $14 per office user, per month | Workspace list pricing, 1-year plan |
| Setup | 40 hrs, built once; 30 min training per driver | Assumption |
| Not counted | Fines up to $1,584/day, $15,846 per recordkeeping violation; insurance effects | 49 CFR 386 Appendix B (2025 levels) |

Figures are as cited when this was built. Verify before reusing.

## How the model scales
Value and licences are per vehicle or per driver, so return rises with fleet size, because setup is built once. At 100 vehicles the model gives $76K value on $14.3K year-one cost (5.3x). Past roughly 300 Workspace users the plan edition changes; past that, check the Enterprise or Frontline options.
