# Module 01 — Course Checkpoints (SpaceX Falcon 9)

Generated: 2025-08-26T12:23:01+03:00

## Checklist

1. Request and parse the SpaceX launch data using GET request? — YES
   - Evidence: `requests.get` used in `safe_get_json()` within `module.01/spacex_data_collection.py` to call
     - `STATIC_JSON_URL` (static JSON dataset)
     - `SPACEX_PAST_URL` (live API fallback)
   - Parsed via `pd.json_normalize(launches)` in `main()`.

2. Filter the dataframe to only include Falcon 9 launches? — YES
   - Evidence: In `build_dataset()`, after assembling `out` DataFrame:
     - `out = out[out['BoosterVersion'] != 'Falcon 1'].copy()` (removes Falcon 1, keeping Falcon 9 family)

3. Replace None values in PayloadMass with the mean? — YES
   - Evidence: In `build_dataset()`:
     - Compute mean and impute: `out['PayloadMass'] = pd.to_numeric(out['PayloadMass'], errors='coerce').fillna(mean_mass)`

## Final results

- Clean dataset CSV: `module.01/spacex_launches_clean.csv`
  - Current rows: 90
- Collection summary Markdown: `module.01/spacex_data_collection_summary.md`

## How to reproduce

```bash
python module.01/spacex_data_collection.py
```

This will regenerate the CSV and summary under `module.01/`.
