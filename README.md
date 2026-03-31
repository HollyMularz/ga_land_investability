# Georgia Land Investability Pipeline

This repository contains all files and instructions to recreate the Georgia county-level land investability pipeline, including ETL processing, Snowflake setup, and investability scoring.

## Contents

- **ETL Script**: `etl_ga_land.py` — processes raw data into parquet files  
- **Processed Data**:  
  - `census_population.parquet`  
  - `hdpulse_income.parquet`  
  - `gosa_school_grades.parquet`  
  - `2025SchoolGrades_data` folder  
  - `HDPulse_data_export.csv`  
  - `co-est2025-pop-13.xlsx`  
- **Build Instructions**: `GA_Land_Pipeline_Build_Instructions.docx`  
- **Snowflake Setup**: `GA_Land_Investability_Setup.sql` — creates database, tables, and view  
- **ETL Session Notes**: `etl_ga_land_session_notes.md` — documents transformations, column changes, and logic

## How to Rebuild

1. Upload the parquet files (and any raw CSV/Excel files) to Snowflake.  
2. Run `GA_Land_Investability_Setup.sql` in your Snowflake environment.  
3. Query the view `VW_COUNTY_INVESTABILITY` to access the final investability scores and tiers.  

*Note:* The `VW_COUNTY_INVESTABILITY` view can also be used as a data source for dashboards, including Sigma.

## Scoring Overview

The **investability score** evaluates county-level land potential based on three weighted factors:

- **Population Growth (40%)** — Measures expected growth from 2020 to 2025. Higher growth indicates stronger housing demand.  
- **Median Family Income (35%)** — Reflects residents’ ability to afford new homes. Higher income contributes more to the score.  
- **School Quality (25%)** — Based on CCRPI scores. Converted into letter grades in Snowflake using these thresholds:  
  - **A:** ≥ 90  
  - **B:** ≥ 80  
  - **C:** ≥ 65  
  - **D:** ≥ 50  
  - **F:** < 50  

Each factor is scaled to its weight (**Population 40, Income 35, School 25**) and summed to create the **investability score**.

**Investability Tiers:**

- **High:** 70 and above  
- **Medium:** 50–69  
- **Low:** Below 50  

## Notes

- Fully reproducible from the files in this repo.  
- Requires a Snowflake account to run the SQL setup and recreate the database, tables, and view.  
- Includes detailed ETL session notes for transparency of transformations and column handling.  
- The `VW_COUNTY_INVESTABILITY` view can serve as a data source for dashboards such as Sigma.
