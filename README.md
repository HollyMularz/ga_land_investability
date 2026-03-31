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
*Note:* The Snowflake view `VW_COUNTY_INVESTABILITY` can be used as a data source for a Sigma dashboard.

## Scoring Overview

- Population Growth, Median Family Income, and School Quality are all combined into an **investability score**.  
- School letter grades are derived from CCRPI scores in Snowflake.  

## Notes

- Fully reproducible from the files in this repo.  
- No external Snowflake access required — the SQL file recreates the full database, tables, and view.  
- Includes detailed ETL session notes for transparency of transformations and column handling.
