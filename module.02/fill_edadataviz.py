import nbformat
from nbformat.v4 import new_code_cell
from pathlib import Path
import sys

NOTEBOOK_PATH = Path(__file__).resolve().parents[1] / "module.02" / "edadataviz.ipynb"

# Map placeholders to code we want to inject
REPLACEMENTS = {
    # TASK 1
    "# Plot a scatter point chart with x axis to be Flight Number and y axis to be the launch site, and hue to be the class value":
        "sns.catplot(y='LaunchSite', x='FlightNumber', hue='Class', data=df, aspect=1)\n"
        "plt.ylabel('Launch Site', fontsize=15)\n"
        "plt.xlabel('Flight Number', fontsize=15)\n"
        "plt.show()\n",
    # TASK 2
    "# Plot a scatter point chart with x axis to be Pay Load Mass (kg) and y axis to be the launch site, and hue to be the class value":
        "sns.catplot(y='LaunchSite', x='PayloadMass', hue='Class', data=df, aspect=1)\n"
        "plt.ylabel('Launch Site', fontsize=15)\n"
        "plt.xlabel('Pay load Mass (kg)', fontsize=15)\n"
        "plt.show()\n",
    # TASK 3
    "# HINT use groupby method on Orbit column and get the mean of Class column":
        "success_by_orbit = df.groupby('Orbit')['Class'].mean().sort_values(ascending=False)\n"
        "plt.figure(figsize=(10,5))\n"
        "sns.barplot(x=success_by_orbit.index, y=success_by_orbit.values, color='steelblue')\n"
        "plt.ylabel('Success Rate')\n"
        "plt.xlabel('Orbit')\n"
        "plt.xticks(rotation=45)\n"
        "plt.title('Success rate by Orbit')\n"
        "plt.tight_layout()\n"
        "plt.show()\n",
    # TASK 4
    "# Plot a scatter point chart with x axis to be FlightNumber and y axis to be the Orbit, and hue to be the class value":
        "sns.catplot(y='Orbit', x='FlightNumber', hue='Class', data=df, aspect=2)\n"
        "plt.ylabel('Orbit', fontsize=15)\n"
        "plt.xlabel('Flight Number', fontsize=15)\n"
        "plt.show()\n",
    # TASK 5
    "# Plot a scatter point chart with x axis to be Payload Mass and y axis to be the Orbit, and hue to be the class value":
        "sns.catplot(y='Orbit', x='PayloadMass', hue='Class', data=df, aspect=2)\n"
        "plt.ylabel('Orbit', fontsize=15)\n"
        "plt.xlabel('Payload Mass (kg)', fontsize=15)\n"
        "plt.show()\n",
    # TASK 6
    "# Plot a line chart with x axis to be the extracted year and y axis to be the success rate":
        "import pandas as pd\n"
        "yearly = df.groupby('Date')['Class'].mean().reset_index()\n"
        "# Ensure year is numeric for ordering\n"
        "yearly['Date'] = pd.to_numeric(yearly['Date'], errors='coerce')\n"
        "plt.figure(figsize=(10,4))\n"
        "sns.lineplot(data=yearly, x='Date', y='Class', marker='o')\n"
        "plt.xlabel('Year')\n"
        "plt.ylabel('Average Success Rate')\n"
        "plt.title('Launch Success Trend by Year')\n"
        "plt.grid(True, alpha=0.3)\n"
        "plt.tight_layout()\n"
        "plt.show()\n",
    # TASK 7
    "# HINT: Use get_dummies() function on the categorical columns":
        "features_one_hot = pd.get_dummies(features, columns=['Orbit','LaunchSite','LandingPad','Serial'])\n"
        "features_one_hot.head()\n",
    # TASK 8
    "# HINT: use astype function":
        "features_one_hot = features_one_hot.astype('float64')\n"
        "features_one_hot.head()\n",
}

# Replacement for JupyterLite-specific data loading cell
LITE_FETCH_SNIPPET = "from js import fetch"
LITE_INSTALL_SNIPPET = "import piplite"

DATA_LOAD_REPLACEMENT = (
    "import os\n"
    "URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv'\n"
    "try:\n"
    "    df = pd.read_csv(URL)\n"
    "except Exception as e:\n"
    "    candidates = [\n"
    "        os.path.join('module.02', 'dataset_part_2.csv'),\n"
    "        os.path.join('module.01', 'spacex_launches_clean.csv'),\n"
    "        'dataset_part_2.csv'\n"
    "    ]\n"
    "    for p in candidates:\n"
    "        if os.path.exists(p):\n"
    "            df = pd.read_csv(p)\n"
    "            break\n"
    "    else:\n"
    "        raise\n"
    "df.head(5)\n"
)


def patch_notebook(path: Path) -> bool:
    nb = nbformat.read(path, as_version=4)
    changed = False

    for cell in nb.cells:
        if cell.cell_type != 'code':
            continue
        src = cell.source or ''

        # Replace JupyterLite installs with a no-op comment
        if LITE_INSTALL_SNIPPET in src:
            cell.source = "# JupyterLite install step removed for local execution\n# Requirements handled by environment (requirements.txt)\n"
            changed = True
            continue

        # Replace JupyterLite fetch with robust pandas read_csv
        if LITE_FETCH_SNIPPET in src:
            # Keep imports that may be present earlier in notebook; here we only handle data loading.
            cell.source = DATA_LOAD_REPLACEMENT
            changed = True
            continue

        # Fill TASK placeholders
        for placeholder, replacement in REPLACEMENTS.items():
            if src.strip().startswith(placeholder):
                cell.source = replacement
                changed = True
                break

    if changed:
        nbformat.write(nb, path)
    return changed


def main():
    path = NOTEBOOK_PATH
    if not path.exists():
        print(f"Notebook not found: {path}")
        sys.exit(1)
    changed = patch_notebook(path)
    if changed:
        print(f"Patched notebook: {path}")
    else:
        print("No changes made (already patched?)")


if __name__ == "__main__":
    main()
