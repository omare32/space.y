# Module 02 — SQL MCQ Answers

Generated: 2025-08-26

## Q1. Which of the following will retrieve up to 20 records from the SPACEXTBL table?
- Answer: `SELECT *  from SPACEXTBL LIMIT 20`

## Q2. Which query displays the minimum payload mass?
- Answer: `select min(payload_mass__kg_) from SPACEXTBL`

## Q3. Total payload mass carried (result column named "Total_Payload_Mass")
- Answer: `SELECT sum(PAYLOAD_MASS__KG_) as Total_Payload_Mass from SPACEXTBL`

## Q4. Mission outcome counts for each launch site
- Answer: `select  count("Mission_Outcome") as MISSION_OUTCOME_COUNT, Launch_Site from SPACEXTBL group by "Launch_Site";`

## Q5. Unique launch sites mentioned in the Spacex table
- Answer: `CCAFS LC-40, KSC LC-39A, VAFB SLC-4E, CCAFS SLC-40`
- Selected option: `CCAFS LC-40,KSC LC-39A, VAFB SLC-4E , CCAFS SLC-40`
