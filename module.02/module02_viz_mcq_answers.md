# Module 02 — Dataviz MCQ Answers

Generated: 2025-08-26

## Q1. What type of data does a Bar Chart best represent?
- Answer: Categorical

## Q2. Total number of columns in the features dataframe after one-hot encoding (Orbit, LaunchSite, LandingPad, Serial)
- Answer: 80
- Evidence: `module.02/spacex_eda_viz_summary.md` shows "Dummies shape: 90 rows x 80 columns".

## Q3. catplot code for scatterplot: FlightNumber vs LaunchSite with hue='Class'
- Answer:
  ```python
  sns.catplot(y="LaunchSite", x="FlightNumber", hue="Class", data=df, aspect=1)
  plt.ylabel("Launch Site", fontsize=15)
  plt.xlabel("Flight Number", fontsize=15)
  plt.show()
  ```
