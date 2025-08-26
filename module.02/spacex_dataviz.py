import os
import io
import datetime
import requests
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

OUT_DIR = os.path.join('module.02')
PLOTS_DIR = os.path.join(OUT_DIR, 'plots')
SUMMARY_MD = os.path.join(OUT_DIR, 'spacex_eda_viz_summary.md')
REMOTE_URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv'
LOCAL_FALLBACK = os.path.join('module.01', 'spacex_launches_clean.csv')
DUMMIES_CSV = os.path.join(OUT_DIR, 'spacex_features_with_dummies.csv')


def ensure_dirs():
    os.makedirs(OUT_DIR, exist_ok=True)
    os.makedirs(PLOTS_DIR, exist_ok=True)


def load_dataset() -> pd.DataFrame:
    # Try remote dataset_part_2.csv first
    try:
        with requests.Session() as s:
            s.headers.update({'User-Agent': 'Mozilla/5.0'})
            r = s.get(REMOTE_URL, timeout=30)
            r.raise_for_status()
            df = pd.read_csv(io.BytesIO(r.content))
            source = REMOTE_URL
    except Exception:
        # Fallback to local cleaned dataset
        df = pd.read_csv(LOCAL_FALLBACK)
        source = LOCAL_FALLBACK
        # Create Class from Outcome if missing
        if 'Class' not in df.columns and 'Outcome' in df.columns:
            df['Class'] = df['Outcome'].astype(str).str.startswith('True').astype(int)
    # Normalize columns expected by notebook naming
    # Some datasets use 'LaunchSite' vs 'Launch Site', etc.
    if 'Launch Site' in df.columns and 'LaunchSite' not in df.columns:
        df['LaunchSite'] = df['Launch Site']
    if 'PayloadMass' not in df.columns and 'PayloadMass (kg)' in df.columns:
        df['PayloadMass'] = df['PayloadMass (kg)']
    return df, source


def plot_relationships(df: pd.DataFrame) -> list[str]:
    sns.set(style='whitegrid')
    paths: list[str] = []

    # Relationship 1: FlightNumber vs PayloadMass by Class
    fig, ax = plt.subplots(figsize=(9,5))
    sns.scatterplot(data=df, x='FlightNumber', y='PayloadMass', hue='Class', ax=ax)
    ax.set_title('Payload mass vs Flight number by landing success')
    ax.set_xlabel('FlightNumber')
    ax.set_ylabel('PayloadMass (kg)')
    p1 = os.path.join(PLOTS_DIR, 'viz_flight_vs_payload.png')
    fig.tight_layout(); fig.savefig(p1, dpi=150); plt.close(fig)
    paths.append(p1)

    # Relationship 2: Orbit vs PayloadMass by Class
    if 'Orbit' in df.columns:
        fig, ax = plt.subplots(figsize=(9,6))
        sns.stripplot(data=df, x='PayloadMass', y='Orbit', hue='Class', dodge=True, alpha=0.7, ax=ax)
        ax.set_title('Payload mass by Orbit and landing success')
        ax.set_xlabel('PayloadMass (kg)')
        ax.set_ylabel('Orbit')
        handles, labels = ax.get_legend_handles_labels()
        if len(labels) > 1:
            ax.legend(handles[:2], labels[:2], title='Class')
        p2 = os.path.join(PLOTS_DIR, 'viz_payload_vs_orbit.png')
        fig.tight_layout(); fig.savefig(p2, dpi=150); plt.close(fig)
        paths.append(p2)

    return paths


def plot_yearly_success_trend(df: pd.DataFrame) -> str:
    # Parse year
    if 'Date' in df.columns:
        years = pd.to_datetime(df['Date'], errors='coerce').dt.year
    else:
        years = pd.Series([np.nan]*len(df))
    rate_by_year = pd.DataFrame({'Year': years, 'Class': pd.to_numeric(df.get('Class', np.nan), errors='coerce')})
    rate_by_year = rate_by_year.dropna().groupby('Year')['Class'].mean().reset_index()

    fig, ax = plt.subplots(figsize=(9,4))
    sns.lineplot(data=rate_by_year, x='Year', y='Class', marker='o', ax=ax)
    ax.set_ylim(0, 1)
    ax.set_title('Launch success rate by year')
    ax.set_ylabel('Success rate')
    p = os.path.join(PLOTS_DIR, 'viz_success_trend_by_year.png')
    fig.tight_layout(); fig.savefig(p, dpi=150); plt.close(fig)
    return p


def build_dummies(df: pd.DataFrame) -> pd.DataFrame:
    # Select features as in the notebook
    cols = ['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']
    avail = [c for c in cols if c in df.columns]
    features = df[avail].copy()
    # Identify categoricals present
    cat_cols = [c for c in ['Orbit', 'LaunchSite', 'LandingPad', 'Serial'] if c in features.columns]
    dummies = pd.get_dummies(features, columns=cat_cols, drop_first=False, dtype=int)
    dummies.to_csv(DUMMIES_CSV, index=False)
    return dummies


def write_summary(df: pd.DataFrame, source: str, rel_plots: list[str], trend_plot: str, dummies: pd.DataFrame) -> None:
    lines: list[str] = []
    lines.append('# SpaceX EDA Visualization Summary')
    lines.append('')
    lines.append(f'Generated: {datetime.datetime.now().isoformat(timespec="seconds")}')
    lines.append(f'Dataset source: {source}')
    lines.append('')

    lines.append('## Relationship visualizations (Checkpoint Q1)')
    for p in rel_plots:
        rel = os.path.relpath(p, start=OUT_DIR)
        lines.append(f'![{os.path.basename(p)}](./{rel.replace("\\","/")})')
        lines.append('')

    lines.append('## Yearly launch success trend (Checkpoint Q2)')
    rel = os.path.relpath(trend_plot, start=OUT_DIR)
    lines.append(f'![{os.path.basename(trend_plot)}](./{rel.replace("\\","/")})')
    lines.append('')

    lines.append('## Dummy variables created (Checkpoint Q3)')
    lines.append(f'Dummies shape: {dummies.shape[0]} rows x {dummies.shape[1]} columns')
    lines.append('Head:')
    lines.append('```')
    lines.append(dummies.head().to_string(index=False))
    lines.append('```')
    lines.append(f'Saved to: {DUMMIES_CSV}')

    with open(SUMMARY_MD, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def main():
    ensure_dirs()
    df, source = load_dataset()
    rel_plots = plot_relationships(df)
    trend_plot = plot_yearly_success_trend(df)
    dummies = build_dummies(df)
    write_summary(df, source, rel_plots, trend_plot, dummies)
    print(f'Saved summary MD: {SUMMARY_MD}')
    print(f'Saved plots to: {PLOTS_DIR}')
    print(f'Saved dummies CSV: {DUMMIES_CSV}')


if __name__ == '__main__':
    main()
