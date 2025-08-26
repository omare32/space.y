import os
import re
import datetime
from typing import List, Dict, Any

import requests
import pandas as pd
from bs4 import BeautifulSoup
import unicodedata

STATIC_URL = "https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
ALT_URL = "https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"
OUTPUT_CSV = os.path.join("module.01", "spacex_webscraping.csv")
OUTPUT_MD = os.path.join("module.01", "spacex_webscraping_summary.md")

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/127.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def date_time(table_cells):
    return [dt.strip() for dt in list(table_cells.strings)][0:2]


def booster_version(table_cells):
    out = ''.join([bv for i, bv in enumerate(table_cells.strings) if i % 2 == 0][0:-1])
    return out


def landing_status(table_cells):
    out = [i for i in table_cells.strings][0]
    return out


def get_mass(table_cells):
    mass = unicodedata.normalize("NFKD", table_cells.text).strip()
    if mass:
        idx = mass.find("kg")
        new_mass = mass[0:idx + 2] if idx != -1 else mass
    else:
        new_mass = "0"
    return new_mass


def extract_column_from_header(row):
    if row.br:
        row.br.extract()
    if row.a:
        row.a.extract()
    if row.sup:
        row.sup.extract()
    colunm_name = ' '.join(row.contents)
    if not (colunm_name.strip().isdigit()):
        colunm_name = colunm_name.strip()
        return colunm_name


def parse_numeric_mass_kg(text: str) -> float:
    # Convert strings like '15,600 kg (34,000 lb)' -> 15600.0
    if not isinstance(text, str):
        return float('nan')
    m = re.search(r"([0-9][0-9,\.]*)\s*kg", text)
    if not m:
        return float('nan')
    val = m.group(1).replace(',', '')
    try:
        return float(val)
    except Exception:
        return float('nan')


def build_dataframe(soup: BeautifulSoup) -> pd.DataFrame:
    # Try to infer headers from the third table as in the lab
    html_tables = soup.find_all('table')
    column_names: List[str] = []
    if len(html_tables) >= 3:
        first_launch_table = html_tables[2]
        for th in first_launch_table.find_all('th'):
            name = extract_column_from_header(th)
            if name:
                column_names.append(name)
    # Build base dict
    launch_dict: Dict[str, List[Any]] = {
        'Flight No.': [],
        'Launch site': [],
        'Payload': [],
        'Payload mass': [],
        'Orbit': [],
        'Customer': [],
        'Launch outcome': [],
        'Version Booster': [],
        'Booster landing': [],
        'Date': [],
        'Time': [],
    }

    extracted_row = 0
    for table_number, table in enumerate(soup.find_all('table', "wikitable plainrowheaders collapsible")):
        for rows in table.find_all("tr"):
            flight_number = None
            if rows.th and rows.th.string:
                s = rows.th.string.strip()
                if s.isdigit():
                    flight_number = s
            row = rows.find_all('td')
            if flight_number and row:
                extracted_row += 1
                # Flight No.
                launch_dict['Flight No.'].append(int(flight_number))
                # Date & Time
                dtlist = date_time(row[0]) if len(row) > 0 else [None, None]
                date = (dtlist[0] or '').strip(',') if dtlist else None
                time = dtlist[1] if len(dtlist) > 1 else None
                launch_dict['Date'].append(date)
                launch_dict['Time'].append(time)
                # Version Booster
                bv = booster_version(row[1]) if len(row) > 1 else ''
                if not bv and len(row) > 1 and row[1].a and row[1].a.string:
                    bv = row[1].a.string
                launch_dict['Version Booster'].append(bv)
                # Launch site
                site = row[2].a.get_text(strip=True) if len(row) > 2 and row[2].a else (row[2].get_text(strip=True) if len(row) > 2 else '')
                launch_dict['Launch site'].append(site)
                # Payload
                payload = row[3].get_text(strip=True) if len(row) > 3 else ''
                launch_dict['Payload'].append(payload)
                # Payload mass
                p_mass = get_mass(row[4]) if len(row) > 4 else ''
                launch_dict['Payload mass'].append(p_mass)
                # Orbit
                orbit = row[5].a.get_text(strip=True) if len(row) > 5 and row[5].a else (row[5].get_text(strip=True) if len(row) > 5 else '')
                launch_dict['Orbit'].append(orbit)
                # Customer
                customer = row[6].get_text(strip=True) if len(row) > 6 else ''
                launch_dict['Customer'].append(customer)
                # Launch outcome
                launch_outcome = (list(row[7].strings)[0].strip() if len(row) > 7 and list(row[7].strings) else '')
                launch_dict['Launch outcome'].append(launch_outcome)
                # Booster landing
                booster_land = landing_status(row[8]) if len(row) > 8 else ''
                launch_dict['Booster landing'].append(booster_land.strip() if isinstance(booster_land, str) else booster_land)

    df = pd.DataFrame({k: pd.Series(v) for k, v in launch_dict.items()})

    # Clean types
    if 'Flight No.' in df.columns:
        df['Flight No.'] = pd.to_numeric(df['Flight No.'], errors='coerce')
    if 'Payload mass' in df.columns:
        df['Payload mass (kg)'] = df['Payload mass'].apply(parse_numeric_mass_kg)
    # Parse date if possible
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date

    return df


def write_markdown_summary(df: pd.DataFrame, path: str) -> None:
    lines: List[str] = []
    lines.append("# SpaceX Web Scraping Summary")
    lines.append("")
    lines.append(f"Generated: {datetime.datetime.now().isoformat(timespec='seconds')}")
    lines.append("")
    lines.append("## Dataset Shape")
    lines.append(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    lines.append("")

    # Head
    lines.append("## Head (first 5 rows)")
    lines.append("```")
    lines.append(df.head().to_string(index=False))
    lines.append("```")
    lines.append("")

    # Missing
    lines.append("## Missing Values by Column")
    lines.append("```")
    lines.append(df.isnull().sum().to_string())
    lines.append("```")
    lines.append("")

    # Numeric describe
    numdesc = df.select_dtypes(include=['number']).describe()
    if not numdesc.empty:
        lines.append("## Numeric Columns Summary (describe)")
        lines.append("```")
        lines.append(numdesc.to_string())
        lines.append("```")
        lines.append("")

    # Value counts for categoricals
    for col in ['Orbit', 'Launch site', 'Launch outcome', 'Version Booster']:
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
    s = requests.Session()
    s.headers.update(HEADERS)
    resp = s.get(STATIC_URL, timeout=30)
    if resp.status_code == 403:
        # Fallback to alternate URL if the specific revision blocks scraping
        resp = s.get(ALT_URL, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'lxml')

    df = build_dataframe(soup)

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False)
    write_markdown_summary(df, OUTPUT_MD)

    print(f"Saved CSV to: {OUTPUT_CSV}")
    print(f"Saved Markdown summary to: {OUTPUT_MD}")
    print("Preview:")
    print(df.head().to_string(index=False))


if __name__ == '__main__':
    main()
