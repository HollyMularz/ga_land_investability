# Georgia Land Investability Pipeline — ETL Session Notes

## Overview

ETL script: `etl_ga_land.py`
Output parquet files: `census_population.parquet`, `hdpulse_income.parquet`, `gosa_school_grades.parquet`

---

## Step 1 — Complete the GOSA School Grades Section

**Problem:** The GOSA section in `etl_ga_land.py` only loaded the raw CSV and printed column names. It did not filter, transform, or write output.

**Actual column names in `school_grades_data.csv`:**
- `SCHOOLID`, `SYSTEMID`, `SYSTEMNAME`, `GRADES`
- CCRPI score columns: `CCRPISCOREE`, `CCRPISCOREM`, `CCRPISCOREH`

**Changes made:**
- Filtered to district-level rows using `Level == 'DISTRICT'`
- Extracted columns: `SCHOOLID`, `SYSTEMID`, `SYSTEMNAME`, `GRADES`, `CCRPISCOREE`, `CCRPISCOREM`, `CCRPISCOREH`
- Derived `county_name` from `SYSTEMNAME` by stripping `" County"` suffix
- Wrote output to `gosa_school_grades.parquet`

**Result:** 1,679 rows written.

---

## Step 2 — Rename Columns to Match Snowflake Schema

**Problem:** The Snowflake target table expected columns `system_id`, `system_name`, `letter_grade`, `ccrpi_score`, `county_name`, but the parquet had raw source column names and three separate CCRPI score columns.

**Changes made:**
- Computed `ccrpi_score` as the row-wise mean of `CCRPISCOREE`, `CCRPISCOREM`, `CCRPISCOREH` (ignoring nulls), rounded to 2 decimal places
- Renamed columns:
  - `SYSTEMID` → `system_id`
  - `SYSTEMNAME` → `system_name`
  - `GRADES` → `letter_grade`
- Dropped `SCHOOLID` and the three raw CCRPI columns
- Final column order: `system_id`, `system_name`, `letter_grade`, `ccrpi_score`, `county_name`

**Result:** 1,679 rows written with Snowflake-aligned schema.

---

## Step 3 — Standardize County Names in Census Population

**Problem:** `census_population.parquet` had county names including the word "County" (e.g., `"Appling County"`), while `hdpulse_income.parquet` had them without (e.g., `"Appling"`). This would prevent joins across parquet files.

**Changes made:**
- Added `.str.replace(' County', '', regex=False)` to the census `county_name` cleaning chain
- All three parquet files now use the same county name format (e.g., `"Appling"`)

**Result:** 159 rows written with consistent county names.

---

## Step 4 — Resolve `letter_grade` Column

**Problem:** After renaming `GRADES` → `letter_grade`, the column contains `"DISTRICT"` for every row — not actual A/B/C/D/F letter grades.

**Investigation findings:**
- `GRADES` column only ever contains the string `"DISTRICT"` for district-level rows
- `SSAS` column (likely the intended letter grade field) is **completely empty** across all rows
- No other column in the raw CSV contains A–F letter grade values

**Resolution:**
Letter grades are derived from `ccrpi_score` directly in the Snowflake view using these thresholds:

| Grade | CCRPI Score Range |
|-------|------------------|
| A     | ≥ 90             |
| B     | ≥ 80             |
| C     | ≥ 65             |
| D     | ≥ 50             |
| F     | < 50             |

**Status:** Resolved.

---

## Current Parquet Output Summary

| File | Rows | Key Columns |
|------|------|-------------|
| `census_population.parquet` | 159 | `county_name`, `pop_2025`, `pop_growth_pct` |
| `hdpulse_income.parquet` | 159 | `county_name`, `fips`, `median_family_income` |
| `gosa_school_grades.parquet` | 1,679 | `system_id`, `system_name`, `letter_grade`, `ccrpi_score`, `county_name` |
