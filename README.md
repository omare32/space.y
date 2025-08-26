# Space.y — Applied Data Science Capstone

This repository contains work for the SpaceX Falcon 9 first stage landing prediction capstone.

## Overview
You will collect data from APIs and other sources, wrangle it, explore it with SQL and visualization, and build predictive models. The final deliverable is a presentation telling the story of your analysis.

## Repo structure
- `module.01/`
  - `jupyter-labs-spacex-data-collection-api.ipynb` — original notebook.
  - `convert_ipynb_to_py.py` — converter to extract code cells from the notebook.
  - `jupyter-labs-spacex-data-collection-api.py` — auto-generated Python script from the notebook (code cells only).
- `requirements.txt` — Python dependencies.
- `.gitignore`

## Environment setup
1. Install Python 3.9+.
2. Create a virtual environment (recommended):
   - PowerShell:
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Working with Module 1
- To regenerate the Python script from the notebook:
  ```bash
  python module.01/convert_ipynb_to_py.py
  ```
- The generated script `module.01/jupyter-labs-spacex-data-collection-api.py` mirrors code cells from the notebook. Some cells in the original lab may be intentionally left for learners to complete; those appear as comments or placeholders in the script as well.

## GitHub
Remote repo: https://github.com/omare32/space.y

Initial commit steps (PowerShell):
```powershell
git init
git add .
git commit -m "Initial commit: module.01 converter + generated .py, requirements, .gitignore, README"
git branch -M main
git remote add origin https://github.com/omare32/space.y.git
git push -u origin main
```
