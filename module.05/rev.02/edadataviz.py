#!/usr/bin/env python
# coding: utf-8

# <p style="text-align:center">
#     <a href="https://skills.network/?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDS0321ENSkillsNetwork26802033-2022-01-01" target="_blank">
#     <img src="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/assets/logos/SN_web_lightmode.png" width="200" alt="Skills Network Logo">
#     </a>
# </p>
# 

# # **SpaceX  Falcon 9 First Stage Landing Prediction**
# 

# ## Assignment: Exploring and Preparing Data
# 

# Estimated time needed: **70** minutes
# 

# In this assignment, we will predict if the Falcon 9 first stage will land successfully. SpaceX advertises Falcon 9 rocket launches on its website with a cost of 62 million dollars; other providers cost upward of 165 million dollars each, much of the savings is due to the fact that SpaceX can reuse the first stage.
# 
# In this lab, you will perform Exploratory Data Analysis and Feature Engineering.
# 

# Falcon 9 first stage will land successfully
# 

# ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/landing_1.gif)
# 

# Several examples of an unsuccessful landing are shown here:
# 

# ![](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DS0701EN-SkillsNetwork/api/Images/crash.gif)
# 

# Most unsuccessful landings are planned. Space X performs a controlled landing in the oceans.
# 

# ## Objectives
# 
# Perform exploratory Data Analysis and Feature Engineering using `Pandas` and `Matplotlib`
# 
# *   Exploratory Data Analysis
# *   Preparing Data  Feature Engineering
# 

# ### Import Libraries and Define Auxiliary Functions
# 

# We will import the following libraries the lab
# 

# In[1]:


# JupyterLite install step removed for local execution
# Requirements handled by environment (requirements.txt)


# In[2]:


# pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
#NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns


# ## Exploratory Data Analysis
# 

# First, let's read the SpaceX dataset into a Pandas dataframe and print its summary
# 

# In[3]:


import os

URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv'

# Prefer local files first to avoid network timeouts
candidates = [
    os.path.join('module.02', 'dataset_part_2.csv'),
    os.path.join('module.01', 'spacex_launches_clean.csv'),
    'dataset_part_2.csv'
]

df = None
for p in candidates:
    if os.path.exists(p):
        df = pd.read_csv(p)
        break

# If none of the local candidates exist, try remote as a last resort
if df is None:
    df = pd.read_csv(URL)

# Ensure Class column exists (derive from 'Outcome' if needed)
if 'Class' not in df.columns:
    # Treat any Outcome starting with 'True' as success (1), else 0
    df['Outcome'] = df['Outcome'].astype(str)
    df['Class'] = df['Outcome'].str.startswith('True').astype(int)

df.head(5)


# First, let's try to see how the `FlightNumber` (indicating the continuous launch attempts.) and `Payload` variables would affect the launch outcome.
# 
# We can plot out the <code>FlightNumber</code> vs. <code>PayloadMass</code>and overlay the outcome of the launch. We see that as the flight number increases, the first stage is more likely to land successfully. The payload mass also appears to be a factor; even with more massive payloads, the first stage often returns successfully.
# 

# In[4]:


sns.catplot(y="PayloadMass", x="FlightNumber", hue="Class", data=df, aspect = 5)
plt.xlabel("Flight Number",fontsize=20)
plt.ylabel("Pay load Mass (kg)",fontsize=20)
plt.show()


# Next, let's drill down to each site visualize its detailed launch records.
# 

# ### TASK 1: Visualize the relationship between Flight Number and Launch Site
# 

# Use the function <code>catplot</code> to plot <code>FlightNumber</code> vs <code>LaunchSite</code>, set the  parameter <code>x</code>  parameter to <code>FlightNumber</code>,set the  <code>y</code> to <code>Launch Site</code> and set the parameter <code>hue</code> to <code>'class'</code>
# 

# In[5]:


sns.catplot(y='LaunchSite', x='FlightNumber', hue='Class', data=df, aspect=1)
plt.ylabel('Launch Site', fontsize=15)
plt.xlabel('Flight Number', fontsize=15)
plt.show()


# Now try to explain the patterns you found in the Flight Number vs. Launch Site scatter point plots.
# 

# ### TASK 2: Visualize the relationship between Payload Mass and Launch Site
# 

# We also want to observe if there is any relationship between launch sites and their payload mass.
# 

# In[6]:


sns.catplot(y='LaunchSite', x='PayloadMass', hue='Class', data=df, aspect=1)
plt.ylabel('Launch Site', fontsize=15)
plt.xlabel('Payload Mass (kg)', fontsize=15)
plt.show()


# Now if you observe Payload Mass Vs. Launch Site scatter point chart you will find for the VAFB-SLC  launchsite there are no  rockets  launched for  heavypayload mass(greater than 10000).
# 

# ### TASK  3: Visualize the relationship between success rate of each orbit type
# 

# Next, we want to visually check if there are any relationship between success rate and orbit type.
# 

# Let's create a `bar chart` for the sucess rate of each orbit
# 

# In[7]:


success_by_orbit = df.groupby('Orbit')['Class'].mean().sort_values(ascending=False)
plt.figure(figsize=(10,5))
sns.barplot(x=success_by_orbit.index, y=success_by_orbit.values, color='steelblue')
plt.ylabel('Success Rate')
plt.xlabel('Orbit')
plt.xticks(rotation=45)
plt.title('Success rate by Orbit')
plt.tight_layout()
plt.show()


# Analyze the plotted bar chart to identify which orbits have the highest success rates.
# 

# ### TASK  4: Visualize the relationship between FlightNumber and Orbit type
# 

# For each orbit, we want to see if there is any relationship between FlightNumber and Orbit type.
# 

# In[8]:


sns.catplot(y='Orbit', x='FlightNumber', hue='Class', data=df, aspect=2)
plt.ylabel('Orbit', fontsize=15)
plt.xlabel('Flight Number', fontsize=15)
plt.show()


# You can observe that in the LEO orbit, success seems to be related to the number of flights. Conversely, in the GTO orbit, there appears to be no relationship between flight number and success.
# 

# ### TASK  5: Visualize the relationship between Payload Mass and Orbit type
# 

# Similarly, we can plot the Payload Mass vs. Orbit scatter point charts to reveal the relationship between Payload Mass and Orbit type
# 

# In[9]:


sns.catplot(y='Orbit', x='PayloadMass', hue='Class', data=df, aspect=2)
plt.ylabel('Orbit', fontsize=15)
plt.xlabel('Payload Mass (kg)', fontsize=15)
plt.show()


# With heavy payloads the successful landing or positive landing rate are more for Polar,LEO and ISS.
# 
# However, for GTO, it's difficult to distinguish between successful and unsuccessful landings as both outcomes are present.
# 

# ### TASK  6: Visualize the launch success yearly trend
# 

# You can plot a line chart with x axis to be <code>Year</code> and y axis to be average success rate, to get the average launch success trend.
# 

# The function will help you get the year from the date:
# 

# In[10]:


# A function to Extract years from the date 
year = []
def Extract_year():
    for i in df["Date"]:
        year.append(str(i).split("-")[0])
    return year

Extract_year()
df['Date'] = year
df.head()


# In[11]:


yearly = df.groupby('Date')['Class'].mean().reset_index()
# Ensure year is numeric for ordering
yearly['Date'] = pd.to_numeric(yearly['Date'], errors='coerce')
plt.figure(figsize=(10,4))
sns.lineplot(data=yearly, x='Date', y='Class', marker='o')
plt.xlabel('Year')
plt.ylabel('Average Success Rate')
plt.title('Launch Success Trend by Year')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()


# you can observe that the sucess rate since 2013 kept increasing till 2020
# 

# ## Features Engineering
# 

# By now, you should obtain some preliminary insights about how each important variable would affect the success rate, we will select the features that will be used in success prediction in the future module.
# 

# In[12]:


features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 'GridFins',
               'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]
features.head()


# ### TASK  7: Create dummy variables to categorical columns
# 

# Use the function <code>get_dummies</code> and <code>features</code> dataframe to apply OneHotEncoder to the column <code>Orbits</code>, <code>LaunchSite</code>, <code>LandingPad</code>, and <code>Serial</code>. Assign the value to the variable <code>features_one_hot</code>, display the results using the method head. Your result dataframe must include all features including the encoded ones.
# 

# In[13]:


features_one_hot = pd.get_dummies(features, columns=['Orbit','LaunchSite','LandingPad','Serial'])
features_one_hot.head()


# ### TASK  8: Cast all numeric columns to `float64`
# 

# Now that our <code>features_one_hot</code> dataframe only contains numbers, cast the entire dataframe to variable type <code>float64</code>
# 

# In[14]:


features_one_hot = features_one_hot.astype('float64')
features_one_hot.head()
# Optional save:
# features_one_hot.to_csv('dataset_part_3.csv', index=False)


# We can now export it to a <b>CSV</b> for the next section,but to make the answers consistent, in the next lab we will provide data in a pre-selected date range.
# 

# <code>features_one_hot.to_csv('dataset_part\_3.csv', index=False)</code>
# 

# ## Authors
# 

# [Pratiksha Verma](https://www.linkedin.com/in/pratiksha-verma-6487561b1/)
# 

# <!--## Change Log-->
# 

# <!--
# | Date (YYYY-MM-DD) | Version | Changed By      | Change Description      |
# | ----------------- | ------- | -------------   | ----------------------- |
# | 2022-11-09        | 1.0     | Pratiksha Verma | Converted initial version to Jupyterlite|
# | 2024-07-18        | 1.2     | Anita Verma | Clarified instructions|
# -->
# 

# ### <h3 align="center"> IBM Corporation 2022. All rights reserved. <h3/>
# 
