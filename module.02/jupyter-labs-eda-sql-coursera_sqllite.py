# Auto-generated from jupyter-labs-eda-sql-coursera_sqllite.ipynb
# Conversion: code cells only. Markdown omitted.

# %% [code] - Cell 1
!pip install sqlalchemy==1.3.9

# %% [code] - Cell 2
!pip install ipython-sql
!pip install ipython-sql prettytable

# %% [code] - Cell 3
%load_ext sql

# %% [code] - Cell 4
import csv, sqlite3
import prettytable
prettytable.DEFAULT = 'DEFAULT'

con = sqlite3.connect("my_data1.db")
cur = con.cursor()

# %% [code] - Cell 5
!pip install -q pandas

# %% [code] - Cell 6
%sql sqlite:///my_data1.db

# %% [code] - Cell 7
import pandas as pd
df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/labs/module_2/data/Spacex.csv")
df.to_sql("SPACEXTBL", con, if_exists='replace', index=False,method="multi")

# %% [code] - Cell 8
#DROP THE TABLE IF EXISTS

%sql DROP TABLE IF EXISTS SPACEXTABLE;

# %% [code] - Cell 9
%sql create table SPACEXTABLE as select * from SPACEXTBL where Date is not null

# %% [code] - Cell 10


# %% [code] - Cell 11


# %% [code] - Cell 12


# %% [code] - Cell 13


# %% [code] - Cell 14


# %% [code] - Cell 15


# %% [code] - Cell 16


# %% [code] - Cell 17


# %% [code] - Cell 18


# %% [code] - Cell 19

