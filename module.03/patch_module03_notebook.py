import nbformat as nbf
from pathlib import Path
import shutil
from datetime import datetime

NB_REL = Path('module.03') / 'lab_jupyter_launch_site_location.ipynb'
NB_PATH = Path.cwd() / NB_REL
BACKUP_PATH = NB_PATH.with_suffix('.backup.ipynb')

LOADER_CODE = '''import os
import requests
import pandas as pd

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv'
LOCAL = 'spacex_launch_geo.csv'

def load_spacex_geo(url=URL, local=LOCAL):
    # try network; on failure, use local cache
    try:
        df = pd.read_csv(url)
        try:
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            with open(local, 'wb') as f:
                f.write(r.content)
        except Exception:
            pass
        return df
    except Exception:
        if os.path.exists(local):
            return pd.read_csv(local)
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(local, 'wb') as f:
            f.write(r.content)
        return pd.read_csv(local)

spacex_df = load_spacex_geo()
'''

SAFETY_MAP_CODE = '''# Safety: ensure launch_sites_df exists
if 'launch_sites_df' not in globals():
    spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
    launch_sites_df = (
        spacex_df.groupby(['Launch Site'], as_index=False).first()[['Launch Site', 'Lat', 'Long']]
    )

# Safety: ensure nasa_coordinate exists
if 'nasa_coordinate' not in globals():
    nasa_coordinate = [29.559684888503615, -95.0830971930759]

# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

# Add circle + label for each launch site
for _, row in launch_sites_df.iterrows():
    coord = [row['Lat'], row['Long']]
    name = row['Launch Site']

    circle = folium.Circle(coord, radius=1000, color='#d35400', fill=True)
    label = folium.map.Marker(
        coord,
        icon=DivIcon(
            icon_size=(20, 20),
            icon_anchor=(0, 0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % name,
        ),
    )

    site_map.add_child(circle)
    site_map.add_child(label)

site_map
'''

MARKER_COLOR_CODE = '''# Create marker_color column from class
spacex_df['marker_color'] = spacex_df['class'].map({1: 'green', 0: 'red'}).fillna('gray')
spacex_df[['Launch Site', 'Lat', 'Long', 'class', 'marker_color']].head()
'''

MARKER_CLUSTER_CODE = '''# Add marker_cluster to current site_map
site_map.add_child(marker_cluster)

# For each launch record add a color-coded marker
for _, record in spacex_df.iterrows():
    marker = folium.Marker(
        location=[record['Lat'], record['Long']],
        icon=folium.Icon(color=record['marker_color'])
    )
    marker_cluster.add_child(marker)

site_map
'''

COASTLINE_DISTANCE_CODE = '''# Choose a launch site (you can change this to a specific site by name)
launch_site_row = launch_sites_df.iloc[0]
launch_site_name = launch_site_row['Launch Site']
launch_site_lat = float(launch_site_row['Lat'])
launch_site_lon = float(launch_site_row['Long'])

# Example coastline coordinates near CCAFS SLC-40 (replace using MousePosition if desired)
coastline_lat = 28.56367
coastline_lon = -80.57163

# distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)
distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)
distance_coastline
'''

COASTLINE_MARKER_CODE = '''# Add a marker at the coastline point showing the distance
distance_marker = folium.Marker(
    [coastline_lat, coastline_lon],
    icon=DivIcon(
        icon_size=(20, 20),
        icon_anchor=(0, 0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),
    ),
)
site_map.add_child(distance_marker)
site_map
'''

POLYLINE_CODE = '''# Create a folium.PolyLine between launch site and coastline point
coordinates = [[launch_site_lat, launch_site_lon], [coastline_lat, coastline_lon]]
lines = folium.PolyLine(locations=coordinates, weight=2, color='blue')
site_map.add_child(lines)
site_map
'''


def main():
    if not NB_PATH.exists():
        raise FileNotFoundError(f"Notebook not found: {NB_PATH}")

    # Backup (do not overwrite an existing one)
    backup_target = BACKUP_PATH
    if BACKUP_PATH.exists():
        ts = datetime.now().strftime('%Y%m%d-%H%M%S')
        backup_target = NB_PATH.with_suffix(f'.backup.{ts}.ipynb')
    shutil.copyfile(NB_PATH, backup_target)

    nb = nbf.read(str(NB_PATH), as_version=4)

    skipped_piplite = False
    replaced_loader = False
    replaced_map = False
    replaced_marker_color = False
    replaced_cluster = False
    replaced_coast = False
    replaced_coast_marker = False
    replaced_polyline = False
    replaced_map_loop_only = False

    new_cells = []
    for cell in nb.cells:
        if cell.cell_type != 'code':
            new_cells.append(cell)
            continue
        src = cell.source or ''

        # Remove piplite cell
        if 'import piplite' in src or 'await piplite.install' in src:
            skipped_piplite = True
            continue

        # Replace JS fetch loader
        if 'from js import fetch' in src and 'spacex_df' in src:
            cell.source = LOADER_CODE
            replaced_loader = True
            new_cells.append(cell)
            continue

        # Replace Initial the map cell
        if 'site_map = folium.Map(location=nasa_coordinate, zoom_start=5)' in src and 'Initial the map' in src:
            cell.source = SAFETY_MAP_CODE
            replaced_map = True
            new_cells.append(cell)
            continue

        # Some course notebooks split the loop from the map init. If we find the loop-only cell,
        # neutralize it to just display the map to prevent NameErrors.
        if '# For each launch site, add a Circle object based on its coordinate' in src and 'launch_sites_df.iterrows()' in src:
            cell.source = (
                "try:\n"
                "    site_map\n"
                "except NameError:\n"
                "    print('Note: Run the initial map cell above to create site_map.')\n"
            )
            replaced_map_loop_only = True
            new_cells.append(cell)
            continue

        # If a previous patch left a cell with only `site_map`, make it safe too
        if src.strip() == 'site_map':
            cell.source = (
                "try:\n"
                "    site_map\n"
                "except NameError:\n"
                "    print('Note: Run the initial map cell above to create site_map.')\n"
            )
            replaced_map_loop_only = True
            new_cells.append(cell)
            continue

        # Marker color creation cell
        if 'Apply a function to check the value of `class` column' in src or 'marker_color value' in src:
            cell.source = MARKER_COLOR_CODE
            replaced_marker_color = True
            new_cells.append(cell)
            continue

        # Marker cluster loop cell
        if 'site_map.add_child(marker_cluster)' in src and 'marker_cluster.add_child(marker)' in src:
            # Only replace if there is a TODO inside
            if 'TODO' in src or 'marker = folium.Marker(...' in src:
                cell.source = MARKER_CLUSTER_CODE
                replaced_cluster = True
            new_cells.append(cell)
            continue

        # Coastline distance cell
        if '# find coordinate of the closet coastline' in src:
            cell.source = COASTLINE_DISTANCE_CODE
            replaced_coast = True
            new_cells.append(cell)
            continue

        # Coastline marker cell
        if '# Create and add a folium.Marker on your selected closest coastline point on the map' in src:
            cell.source = COASTLINE_MARKER_CODE
            replaced_coast_marker = True
            new_cells.append(cell)
            continue

        # Polyline cell
        if 'folium.PolyLine' in src and 'site_map.add_child(lines)' in src:
            cell.source = POLYLINE_CODE
            replaced_polyline = True
            new_cells.append(cell)
            continue

        new_cells.append(cell)

    nb.cells = new_cells

    nbf.write(nb, str(NB_PATH))

    print('Patched notebook:', NB_REL)
    print('Backup saved to:', backup_target)
    print('Changes:')
    print('  removed piplite cell      :', skipped_piplite)
    print('  replaced CSV loader       :', replaced_loader)
    print('  replaced initial map cell :', replaced_map)
    print('  added marker_color cell   :', replaced_marker_color)
    print('  filled marker cluster     :', replaced_cluster)
    print('  coastline distance calc   :', replaced_coast)
    print('  coastline marker          :', replaced_coast_marker)
    print('  polyline added            :', replaced_polyline)
    print('  map loop-only neutralized :', replaced_map_loop_only)


if __name__ == '__main__':
    main()
