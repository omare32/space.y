import os
import sqlite3
import datetime
from typing import List

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

API_CSV = os.path.join('module.01', 'spacex_launches_clean.csv')
SCRAPED_CSV = os.path.join('module.01', 'spacex_webscraping.csv')
OUT_DIR = os.path.join('module.02')
PLOTS_DIR = os.path.join(OUT_DIR, 'plots')
DB_PATH = os.path.join(OUT_DIR, 'spacex.db')
MERGED_CSV = os.path.join(OUT_DIR, 'spacex_launches_merged.csv')
SUMMARY_MD = os.path.join(OUT_DIR, 'spacex_eda_sql_summary.md')


def ensure_dirs():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(PLOTS_DIR, exist_ok=True)


def read_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    api_df = pd.read_csv(API_CSV)
    scraped_df = pd.read_csv(SCRAPED_CSV)
    # Parse dates
    api_df['Date'] = pd.to_datetime(api_df['Date'], errors='coerce').dt.date
    if 'Date' in scraped_df.columns:
        scraped_df['Date'] = pd.to_datetime(scraped_df['Date'], errors='coerce').dt.date
    # Clean numeric
    if 'Payload mass (kg)' in scraped_df.columns:
        scraped_df['Payload mass (kg)'] = pd.to_numeric(scraped_df['Payload mass (kg)'], errors='coerce')
    return api_df, scraped_df


def merge_data(api_df: pd.DataFrame, scraped_df: pd.DataFrame) -> pd.DataFrame:
    cols = ['Date', 'Orbit', 'Customer', 'Payload mass (kg)', 'Launch site', 'Version Booster']
    cols_avail = [c for c in cols if c in scraped_df.columns]
    scraped_sel = scraped_df[cols_avail].copy()

    merged = api_df.merge(scraped_sel, on=[c for c in ['Date', 'Orbit'] if c in scraped_sel.columns], how='left', suffixes=('', '_scraped'))

    # Compare payload mass
    if 'PayloadMass' in merged.columns and 'Payload mass (kg)' in merged.columns:
        merged['payload_diff_kg'] = pd.to_numeric(merged['PayloadMass'], errors='coerce') - pd.to_numeric(merged['Payload mass (kg)'], errors='coerce')
        merged['payload_within_50kg'] = merged['payload_diff_kg'].abs() <= 50
    else:
        merged['payload_diff_kg'] = np.nan
        merged['payload_within_50kg'] = np.nan

    # Success flag from Outcome
    if 'Outcome' in merged.columns:
        merged['LandingSuccess'] = merged['Outcome'].astype(str).str.startswith('True')
    else:
        merged['LandingSuccess'] = np.nan

    # Year for grouping
    merged['Year'] = pd.to_datetime(merged['Date'], errors='coerce').dt.year

    return merged


def save_sql_tables(merged: pd.DataFrame, api_df: pd.DataFrame, scraped_df: pd.DataFrame) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        api_df.to_sql('launches_api', conn, if_exists='replace', index=False)
        scraped_df.to_sql('launches_scraped', conn, if_exists='replace', index=False)
        merged.to_sql('launches_merged', conn, if_exists='replace', index=False)


def run_queries() -> dict[str, pd.DataFrame]:
    results: dict[str, pd.DataFrame] = {}
    with sqlite3.connect(DB_PATH) as conn:
        results['by_orbit'] = pd.read_sql_query(
            """
            SELECT Orbit, COUNT(*) AS launches
            FROM launches_merged
            GROUP BY Orbit
            ORDER BY launches DESC;
            """, conn)
        results['success_rate_by_site'] = pd.read_sql_query(
            """
            SELECT LaunchSite,
                   AVG(CASE WHEN Outcome LIKE 'True %' THEN 1.0 WHEN Outcome LIKE 'False %' THEN 0.0 ELSE NULL END) AS landing_success_rate,
                   COUNT(*) AS n
            FROM launches_merged
            GROUP BY LaunchSite
            HAVING n >= 3
            ORDER BY landing_success_rate DESC;
            """, conn)
        results['avg_payload_by_site'] = pd.read_sql_query(
            """
            SELECT LaunchSite, ROUND(AVG(PayloadMass),2) AS avg_payload_kg, COUNT(*) AS n
            FROM launches_merged
            GROUP BY LaunchSite
            ORDER BY avg_payload_kg DESC;
            """, conn)
        if 'Customer' in pd.read_sql_query("SELECT * FROM launches_merged LIMIT 1;", conn).columns:
            results['top_customers'] = pd.read_sql_query(
                """
                SELECT COALESCE(Customer, 'Unknown') AS Customer, COUNT(*) AS launches
                FROM launches_merged
                GROUP BY Customer
                ORDER BY launches DESC
                LIMIT 10;
                """, conn)
    return results


def make_plots(merged: pd.DataFrame) -> List[str]:
    saved: List[str] = []
    sns.set(style='whitegrid')

    # 1. Landing outcomes by year
    fig, ax = plt.subplots(figsize=(8,4))
    yearly = merged.groupby(['Year', 'LandingSuccess']).size().unstack(fill_value=0)
    yearly.plot(kind='bar', stacked=True, ax=ax)
    ax.set_title('Launch outcomes by year')
    ax.set_xlabel('Year')
    ax.set_ylabel('Count')
    p1 = os.path.join(PLOTS_DIR, 'outcomes_by_year.png')
    fig.tight_layout()
    fig.savefig(p1, dpi=150)
    plt.close(fig)
    saved.append(p1)

    # 2. Payload mass distribution
    fig, ax = plt.subplots(figsize=(8,4))
    sns.histplot(pd.to_numeric(merged['PayloadMass'], errors='coerce').dropna(), bins=30, kde=True, ax=ax)
    ax.set_title('Payload mass distribution (kg)')
    ax.set_xlabel('PayloadMass (kg)')
    p2 = os.path.join(PLOTS_DIR, 'payload_distribution.png')
    fig.tight_layout()
    fig.savefig(p2, dpi=150)
    plt.close(fig)
    saved.append(p2)

    # 3. Top launch sites
    fig, ax = plt.subplots(figsize=(8,4))
    sites = merged['LaunchSite'].value_counts().head(5)
    sns.barplot(x=sites.values, y=sites.index, ax=ax)
    ax.set_title('Top 5 Launch Sites by count')
    ax.set_xlabel('Launches')
    ax.set_ylabel('Launch Site')
    p3 = os.path.join(PLOTS_DIR, 'top_launch_sites.png')
    fig.tight_layout()
    fig.savefig(p3, dpi=150)
    plt.close(fig)
    saved.append(p3)

    return saved


def write_markdown(merged: pd.DataFrame, results: dict[str, pd.DataFrame], plot_paths: List[str]) -> None:
    lines: List[str] = []
    lines.append('# EDA and SQL Summary — SpaceX Falcon 9')
    lines.append('')
    lines.append(f"Generated: {datetime.datetime.now().isoformat(timespec='seconds')}")
    lines.append('')
    lines.append('## Dataset (merged) shape')
    lines.append(f"Rows: {merged.shape[0]}, Columns: {merged.shape[1]}")
    lines.append('')

    lines.append('## Head (first 5 rows)')
    lines.append('```')
    lines.append(merged.head().to_string(index=False))
    lines.append('```')
    lines.append('')

    lines.append('## Missing values by column')
    lines.append('```')
    lines.append(merged.isnull().sum().to_string())
    lines.append('```')
    lines.append('')

    # SQL results
    for title, df in results.items():
        lines.append(f"## SQL — {title.replace('_',' ').title()}")
        lines.append('```')
        lines.append(df.to_string(index=False))
        lines.append('```')
        lines.append('')

    # Plots
    lines.append('## Visualizations')
    for p in plot_paths:
        rel = os.path.relpath(p, start=OUT_DIR)
        lines.append(f"![{os.path.basename(p)}](./{rel.replace('\\','/')})")
        lines.append('')

    with open(SUMMARY_MD, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def main():
    ensure_dirs()
    api_df, scraped_df = read_data()
    merged = merge_data(api_df, scraped_df)
    merged.to_csv(MERGED_CSV, index=False)

    save_sql_tables(merged, api_df, scraped_df)
    results = run_queries()
    plots = make_plots(merged)
    write_markdown(merged, results, plots)

    print(f"Saved merged CSV: {MERGED_CSV}")
    print(f"Saved SQLite DB: {DB_PATH}")
    print(f"Saved summary MD: {SUMMARY_MD}")


if __name__ == '__main__':
    main()
