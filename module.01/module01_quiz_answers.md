# Module 01 — Quiz Answers (SpaceX Data & Web Scraping)

Generated: 2025-08-26

## Q1. After GET + pd.json_normalize, what year is in the first row of column static_fire_date_utc?
- Answer: 2006
- Source: https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/API_call_spacex_api.json (first entry `static_fire_date_utc`: 2006-03-17T00:00:00.000Z)

## Q2. Using the API, how many Falcon 9 launches are there after removing Falcon 1 launches?
- Answer: 90
- Source: Cleaned dataset generated from `module.01/spacex_data_collection.py` (see `module.01/spacex_data_collection_summary.md`, Rows: 90)

## Q3. At the end of the API data collection, how many missing values are there for column LandingPad?
- Answer: 26
- Source: `module.01/spacex_data_collection_summary.md` → Missing Values by Column → LandingPad: 26

## Q4. After requesting the Falcon 9 Launch Wiki page and creating BeautifulSoup object, what is the output of `soup.title`?
- Answer: `<title>List of Falcon 9 and Falcon Heavy launches - Wikipedia</title>`
- Source: https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922

---
Notes:
- Q1 year taken from the first object's `static_fire_date_utc` in the static dataset.
- Q2 and Q3 derived from the pipeline in `module.01/spacex_data_collection.py` and its summary outputs.
- Q4 is the exact Tag output of `soup.title` (not `.text`).
