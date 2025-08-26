# Module 02 — EDA with SQL (SQLite) Quiz Answers

Generated: 2025-08-26

Artifacts produced by running `module.02/spacex_eda_sql.py`:
- SQLite DB: `module.02/spacex.db`
- Summary: `module.02/spacex_eda_sql_summary.md`
- Merged CSV: `module.02/spacex_launches_merged.csv`

Converted notebook (code-only): `module.02/jupyter-labs-eda-sql-coursera_sqllite.py`

## Q1. Have you loaded the SQL extension and establish a connection with the SQLite database?
- Answer: Yes
- Evidence:
  - In `jupyter-labs-eda-sql-coursera_sqllite.py`: `%load_ext sql` and `%sql sqlite:///my_data1.db`
  - In `spacex_eda_sql.py`: connection established via `sqlite3.connect(DB_PATH)` and used for queries and table creation.

## Q2. Have you loaded SpaceX dataset into SQLite Table?
- Answer: Yes
- Evidence:
  - In `jupyter-labs-eda-sql-coursera_sqllite.py`: `df.to_sql("SPACEXTBL", con, if_exists='replace', index=False, method="multi")` then `%sql create table SPACEXTABLE as select * from SPACEXTBL where Date is not null`.
  - In `spacex_eda_sql.py`: `save_sql_tables()` writes `launches_api`, `launches_scraped`, and `launches_merged` tables into `module.02/spacex.db`.

## Q3. Have you used SQL queries with the SQL magic commands in Python to perform EDA?
- Answer: Yes
- Evidence:
  - `jupyter-labs-eda-sql-coursera_sqllite.py` uses `%sql` statements (e.g., DROP/CREATE). 
  - Additionally, `spacex_eda_sql.py` performs EDA queries directly in SQLite (see sections "SQL — By Orbit", "SQL — Success Rate By Site" in `spacex_eda_sql_summary.md`).
