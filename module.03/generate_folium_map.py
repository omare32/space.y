from __future__ import annotations
import os
import sys
from typing import Optional

import pandas as pd
import folium
from folium.plugins import MarkerCluster

ROOT = os.path.dirname(__file__)
GEO_CSV = os.path.join(ROOT, "spacex_launch_geo.csv")
ALT_CSV = os.path.join(ROOT, "spacex_launch_dash.csv")
HTML_OUT = os.path.join(ROOT, "folium_map.html")
PNG_OUT = os.path.join(ROOT, "folium_map.png")


def load_geo_dataframe() -> pd.DataFrame:
    # Prefer the geo CSV with lat/lon if present
    path = GEO_CSV if os.path.exists(GEO_CSV) else ALT_CSV
    if not os.path.exists(path):
        raise FileNotFoundError("No local SpaceX geo CSV found in module.03")
    df = pd.read_csv(path)
    # Standardize columns: trim whitespace and map synonyms case-insensitively
    df = df.rename(columns={c: c.strip() for c in df.columns})
    lower_cols = {c.lower(): c for c in df.columns}
    name_map = {
        "launch site": "Launch Site",
        "latitude": "Latitude",
        "lat": "Latitude",
        "longitude": "Longitude",
        "long": "Longitude",
        "lon": "Longitude",
        "lng": "Longitude",
    }
    renames: dict[str, str] = {}
    for key_lower, target in name_map.items():
        if key_lower in lower_cols:
            renames[lower_cols[key_lower]] = target
    if renames:
        df = df.rename(columns=renames)
    required = {"Launch Site", "Latitude", "Longitude"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns for map: {missing}")
    df = df.dropna(subset=["Latitude", "Longitude"]).copy()
    return df


def build_map(df: pd.DataFrame) -> folium.Map:
    # Center map
    lat = float(df["Latitude"].mean())
    lon = float(df["Longitude"].mean())
    m = folium.Map(location=[lat, lon], zoom_start=4, tiles="cartodbpositron")

    # Cluster markers
    cluster = MarkerCluster().add_to(m)
    for _, row in df.iterrows():
        site = str(row["Launch Site"]) if "Launch Site" in df.columns else "Launch Site"
        folium.Marker(
            location=[float(row["Latitude"]), float(row["Longitude"])],
            popup=folium.Popup(site, max_width=250),
            icon=folium.Icon(color="blue", icon="rocket", prefix="fa"),
        ).add_to(cluster)

    # Add bounds
    sw = [float(df["Latitude"].min()) - 0.5, float(df["Longitude"].min()) - 0.5]
    ne = [float(df["Latitude"].max()) + 0.5, float(df["Longitude"].max()) + 0.5]
    m.fit_bounds([sw, ne])
    return m


def save_html(m: folium.Map, html_path: str = HTML_OUT) -> str:
    m.save(html_path)
    return html_path


def try_export_png(html_path: str = HTML_OUT, png_path: str = PNG_OUT, width: int = 1400, height: int = 900) -> bool:
    # Optional dependency: Selenium + webdriver-manager + a Chromium/Edge/Chrome
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        from selenium.webdriver.common.by import By
        from webdriver_manager.chrome import ChromeDriverManager  # type: ignore
    except Exception:
        # Selenium not available
        return False

    file_url = "file:///" + html_path.replace("\\", "/")

    opts = ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument(f"--window-size={width},{height}")
    opts.add_argument("--hide-scrollbars")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=opts)
    try:
        driver.get(file_url)
        # Give tiles a moment to load
        driver.implicitly_wait(5)
        # Screenshot the viewport
        driver.save_screenshot(png_path)
        return os.path.exists(png_path)
    finally:
        driver.quit()


def main():
    df = load_geo_dataframe()
    m = build_map(df)
    html = save_html(m)
    made_png = try_export_png(html)
    print(f"Saved Folium HTML to: {html}")
    if made_png:
        print(f"Saved Folium PNG to: {PNG_OUT}")
    else:
        print("PNG not created (Selenium not available). You can still open the HTML or provide a manual screenshot at module.03/folium_map.png.")


if __name__ == "__main__":
    main()
