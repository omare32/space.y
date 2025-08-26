import os
import json
import time
import datetime
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import requests


STATIC_JSON_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json"
)
SPACEX_PAST_URL = "https://api.spacexdata.com/v4/launches/past"
SPACEX_API_BASE = "https://api.spacexdata.com/v4"

OUTPUT_CSV = os.path.join("module.01", "spacex_launches_clean.csv")
OUTPUT_MD = os.path.join("module.01", "spacex_data_collection_summary.md")
DATE_CUTOFF = datetime.date(2020, 11, 13)


def safe_get_json(url: str, timeout: int = 20) -> Optional[Any]:
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None


def fetch_launches() -> List[Dict[str, Any]]:
    # Prefer the static dataset for stability; fall back to live API if needed.
    data = safe_get_json(STATIC_JSON_URL)
    if isinstance(data, list) and data:
        return data
    live = safe_get_json(SPACEX_PAST_URL)
    if isinstance(live, list) and live:
        return live
    raise RuntimeError("Unable to fetch SpaceX launches from static or live API.")


class APICache:
    def __init__(self):
        self.rockets: Dict[str, Dict[str, Any]] = {}
        self.launchpads: Dict[str, Dict[str, Any]] = {}
        self.payloads: Dict[str, Dict[str, Any]] = {}
        self.cores: Dict[str, Dict[str, Any]] = {}

    def get(self, kind: str, _id: Optional[str]) -> Optional[Dict[str, Any]]:
        if not _id:
            return None
        store = getattr(self, kind)
        if _id in store:
            return store[_id]
        url = f"{SPACEX_API_BASE}/{kind}/{_id}"
        data = safe_get_json(url)
        if isinstance(data, dict):
            store[_id] = data
            # Be gentle with the API
            time.sleep(0.05)
            return data
        return None


def build_dataset(df: pd.DataFrame) -> pd.DataFrame:
    # Keep only relevant columns
    cols = ['rocket', 'payloads', 'launchpad', 'cores', 'flight_number', 'date_utc']
    df = df[[c for c in cols if c in df.columns]].copy()

    # Filter to single core and single payload
    df = df[df['cores'].map(lambda x: isinstance(x, list) and len(x) == 1)]
    df = df[df['payloads'].map(lambda x: isinstance(x, list) and len(x) == 1)]

    # Extract single items
    df['cores'] = df['cores'].map(lambda x: x[0] if isinstance(x, list) and x else x)
    df['payloads'] = df['payloads'].map(lambda x: x[0] if isinstance(x, list) and x else x)

    # Date
    df['date'] = pd.to_datetime(df['date_utc'], errors='coerce').dt.date
    df = df[df['date'] <= DATE_CUTOFF]
    df = df.reset_index(drop=True)

    cache = APICache()

    BoosterVersion: List[Optional[str]] = []
    PayloadMass: List[Optional[float]] = []
    Orbit: List[Optional[str]] = []
    LaunchSite: List[Optional[str]] = []
    Outcome: List[Optional[str]] = []
    Flights: List[Optional[int]] = []
    GridFins: List[Optional[bool]] = []
    Reused: List[Optional[bool]] = []
    Legs: List[Optional[bool]] = []
    LandingPad: List[Optional[str]] = []
    Block: List[Optional[int]] = []
    ReusedCount: List[Optional[int]] = []
    Serial: List[Optional[str]] = []
    Longitude: List[Optional[float]] = []
    Latitude: List[Optional[float]] = []

    for _, row in df.iterrows():
        # Rocket name
        rocket = cache.get('rockets', row.get('rocket'))
        BoosterVersion.append(rocket.get('name') if rocket else None)

        # Launch site, latitude/longitude
        lpad = cache.get('launchpads', row.get('launchpad'))
        if lpad:
            Longitude.append(lpad.get('longitude'))
            Latitude.append(lpad.get('latitude'))
            LaunchSite.append(lpad.get('name'))
        else:
            Longitude.append(None)
            Latitude.append(None)
            LaunchSite.append(None)

        # Payload mass and orbit
        payload = cache.get('payloads', row.get('payloads'))
        if payload:
            PayloadMass.append(payload.get('mass_kg'))
            Orbit.append(payload.get('orbit'))
        else:
            PayloadMass.append(None)
            Orbit.append(None)

        # Core info
        core_info = row.get('cores') or {}
        core_id = core_info.get('core') if isinstance(core_info, dict) else None
        core = cache.get('cores', core_id) if core_id else None
        Block.append(core.get('block') if core else None)
        ReusedCount.append(core.get('reuse_count') if core else None)
        Serial.append(core.get('serial') if core else None)

        # From the per-launch core object
        outcome = f"{core_info.get('landing_success')} {core_info.get('landing_type')}" if isinstance(core_info, dict) else None
        Outcome.append(outcome)
        Flights.append(core_info.get('flight') if isinstance(core_info, dict) else None)
        GridFins.append(core_info.get('gridfins') if isinstance(core_info, dict) else None)
        Reused.append(core_info.get('reused') if isinstance(core_info, dict) else None)
        Legs.append(core_info.get('legs') if isinstance(core_info, dict) else None)
        LandingPad.append(core_info.get('landpad') if isinstance(core_info, dict) else None)

    launch_dict = {
        'FlightNumber': list(df['flight_number']),
        'Date': list(df['date']),
        'BoosterVersion': BoosterVersion,
        'PayloadMass': PayloadMass,
        'Orbit': Orbit,
        'LaunchSite': LaunchSite,
        'Outcome': Outcome,
        'Flights': Flights,
        'GridFins': GridFins,
        'Reused': Reused,
        'Legs': Legs,
        'LandingPad': LandingPad,
        'Block': Block,
        'ReusedCount': ReusedCount,
        'Serial': Serial,
        'Longitude': Longitude,
        'Latitude': Latitude,
    }

    out = pd.DataFrame(launch_dict)

    # Keep Falcon 9 family; drop Falcon 1 entries
    out = out[out['BoosterVersion'] != 'Falcon 1'].copy()

    # Reindex FlightNumber sequentially
    out = out.reset_index(drop=True)
    out.loc[:, 'FlightNumber'] = np.arange(1, out.shape[0] + 1)

    # Impute PayloadMass with mean
    if 'PayloadMass' in out.columns:
        mean_mass = pd.to_numeric(out['PayloadMass'], errors='coerce').mean()
        out.loc[:, 'PayloadMass'] = pd.to_numeric(out['PayloadMass'], errors='coerce').fillna(mean_mass)

    return out


def write_markdown_summary(df: pd.DataFrame, path: str) -> None:
    lines: List[str] = []
    lines.append("# SpaceX Data Collection Summary")
    lines.append("")
    lines.append(f"Generated: {datetime.datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("## Dataset Shape")
    lines.append(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    lines.append("")

    # Date range
    if 'Date' in df.columns:
        try:
            dmin = pd.to_datetime(df['Date']).min().date()
            dmax = pd.to_datetime(df['Date']).max().date()
            lines.append("## Date Range")
            lines.append(f"{dmin} to {dmax}")
            lines.append("")
        except Exception:
            pass

    # Head
    lines.append("## Head (first 5 rows)")
    lines.append("```")
    lines.append(df.head().to_string(index=False))
    lines.append("```")
    lines.append("")

    # Missing values
    lines.append("## Missing Values by Column")
    lines.append("```")
    lines.append(df.isnull().sum().to_string())
    lines.append("```")
    lines.append("")

    # Numeric summary
    numdesc = df.select_dtypes(include=[np.number]).describe()
    if not numdesc.empty:
        lines.append("## Numeric Columns Summary (describe)")
        lines.append("```")
        lines.append(numdesc.to_string())
        lines.append("```")
        lines.append("")

    # Value counts for key categoricals
    for col in ['Orbit', 'LaunchSite', 'Outcome', 'BoosterVersion']:
        if col in df.columns:
            lines.append(f"## Value Counts — {col}")
            vc = df[col].value_counts(dropna=False).head(10)
            lines.append("```")
            lines.append(vc.to_string())
            lines.append("```")
            lines.append("")

    with open(path, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines) + "\n")


def main():
    launches = fetch_launches()
    raw_df = pd.json_normalize(launches)
    clean_df = build_dataset(raw_df)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    clean_df.to_csv(OUTPUT_CSV, index=False)
    write_markdown_summary(clean_df, OUTPUT_MD)

    # Console summary
    print(f"Saved CSV to: {OUTPUT_CSV}")
    print(f"Saved Markdown summary to: {OUTPUT_MD}")
    print("Preview:")
    print(clean_df.head().to_string(index=False))


if __name__ == '__main__':
    main()
