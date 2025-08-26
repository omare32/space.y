# Module 01 — Data Wrangling Quiz Answers

Generated: 2025-08-26
Source summary: `module.01/spacex_data_wrangling_summary.md`

## Q1. How many launches came from CCAFS SLC 40?
- Answer: 55
- Source: Launches per Site (Q1) — `CCAFS SLC 40: 55`

## Q2. What was the success rate?
- Answer: 67%
- Source: Landing Outcome Label (Q4) — success rate reported as 0.6667 ≈ 67%

## Q3. How many launches went to geosynchronous orbit?
- Answer: 1
- Source: Orbits Counts (Q2) — `GEO: 1`
- Note: Geostationary Transfer Orbit (GTO) is 27; the question specifies "geosynchronous orbit" (GEO), not GTO.

## Q4. How many mission outcome was successfully landed to a drone ship?
- Answer: 41
- Source: Mission Outcome per Orbit (Q3) — sum of `True ASDS` across all orbits = 41
