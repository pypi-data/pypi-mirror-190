# Appendix G Performance

Run an ASHRAE 90.1 Appendix G simulation and compute the Performance Cost Index (PCI)
as well as LEED energy points.

The recipe outputs a file called `appendix_g_summary.json`, which contains the PCI
improvement for the latest versions of ASHRAE 90.1 (2016, 2019, 2022) in the format below:

```json
{
  "eui": 306.852,
  "total_floor_area": 66129.6,
  "conditioned_floor_area": 66129.6,
  "total_energy": 20292008.333,
  "end_uses": {
    "heating": 30.924,
    "cooling": 84.342,
    "interior_lighting": 27.451,
    "interior_equipment": 164.115,
    "pumps": 0.019
  }
}
```

The recipe also outputs a file called `leed_v4_summary.json`, which contains the
ASHRAE 90.1-2016 PCI for both cost and carbon (GHG) emissions in the format below:

```json
{
  "eui": 306.852,
  "total_floor_area": 66129.6,
  "conditioned_floor_area": 66129.6,
  "total_energy": 20292008.333,
  "end_uses": {
    "heating": 30.924,
    "cooling": 84.342,
    "interior_lighting": 27.451,
    "interior_equipment": 164.115,
    "pumps": 0.019
  }
}
```
