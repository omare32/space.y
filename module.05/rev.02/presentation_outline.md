# Presentation Outline

## 1. Title Slide
- Title: SpaceX Falcon 9 First Stage Landing Prediction
- Subtitle: A Data Science Capstone Project
- Author: [Your Name]

## 2. Executive Summary
- Brief overview of the project, its objectives, and key findings.
- Mention the successful development of a machine learning model to predict Falcon 9 first stage landings.

## 3. Introduction
- Background on SpaceX and the importance of reusable rockets.
- Project goal: To predict the success of Falcon 9 first stage landings to determine launch costs.
- Data sources: SpaceX API, Wikipedia, and other publicly available data.

## 4. Data Collection & Wrangling
- Methodology for collecting data from the SpaceX API and web scraping from Wikipedia.
- Data cleaning and preprocessing steps, including handling missing values and creating new features.

## 5. Exploratory Data Analysis (EDA) with Visualization
- **Flight Number vs. Payload Mass:** Show the relationship between flight number and payload mass, and how it affects the landing outcome.
- **Flight Number vs. Launch Site:** Visualize the relationship between flight number and launch site.
- **Payload Mass vs. Launch Site:** Show the relationship between payload mass and launch site.
- **Success Rate by Orbit:** Bar chart showing the success rate for each orbit type.
- **Flight Number vs. Orbit Type:** Scatter plot showing the relationship between flight number and orbit type.
- **Payload Mass vs. Orbit Type:** Scatter plot showing the relationship between payload mass and orbit type.
- **Launch Success Trend by Year:** Line chart showing the trend of launch success over the years.

## 6. EDA with SQL
- **Unique Launch Sites:** List of unique launch sites.
- **Launch Sites Starting with CCA:** 5 records of launch sites starting with 'CCA'.
- **Total Payload Mass for NASA (CRS):** Total payload mass for NASA's CRS missions.
- **Average Payload Mass for F9 v1.1:** Average payload mass for the F9 v1.1 booster.
- **First Successful Ground Pad Landing:** Date of the first successful ground pad landing.
- **Boosters with Success on Drone Ship:** List of boosters with successful drone ship landings and specific payload mass.
- **Mission Outcomes:** Total number of successful and failed missions.
- **Booster Versions with Maximum Payload Mass:** List of booster versions that carried the maximum payload mass.
- **Failed Drone Ship Landings in 2015:** Details of failed drone ship landings in 2015.
- **Landing Outcomes (2010-2017):** Ranked count of landing outcomes between 2010 and 2017.

## 7. Interactive Visual Analytics with Folium
- **Launch Site Locations:** Map with all launch sites marked.
- **Success/Failed Launches per Site:** Map showing the success and failure of launches for each site.
- **Proximity Analysis:** Map showing the distances between launch sites and their proximities (e.g., coastlines, cities).

## 8. Predictive Analysis (Machine Learning)
- **Methodology:**
    - Feature engineering and selection.
    - Data standardization and splitting into training and testing sets.
    - Hyperparameter tuning for Support Vector Machine (SVM), Classification Trees, and Logistic Regression.
- **Results:**
    - Confusion matrices for each model.
    - Comparison of model performance based on accuracy and other metrics.
    - Identification of the best performing model.

## 9. Plotly Dash Dashboard
- Showcase the interactive dashboard created with Plotly Dash.
- Explain the features of the dashboard and how it can be used to explore the data.

## 10. Conclusion
- Summary of the project's findings and the insights gained.
- The final machine learning model can effectively predict the success of Falcon 9 first stage landings.
- Potential for future work and improvements.

## 11. Creativity & Innovation
- Highlight any creative approaches or innovative insights discovered during the project.

## 12. Thank You & Questions


