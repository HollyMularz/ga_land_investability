CREATE OR REPLACE VIEW GA_LAND_INVESTABILITY.ANALYTICS.VW_COUNTY_INVESTABILITY AS
WITH pop AS (
  SELECT
    UPPER(TRIM(county_name))   AS county_key,
    county_name,
    pop_base_2020,
    pop_2025,
    pop_growth_pct
  FROM GA_LAND_INVESTABILITY.RAW.CENSUS_POPULATION
),
inc AS (
  SELECT
    UPPER(TRIM(county_name))   AS county_key,
    fips,
    median_family_income,
    national_rank
  FROM GA_LAND_INVESTABILITY.RAW.HDPULSE_INCOME
),
sch AS (
  SELECT
    UPPER(TRIM(county_name))   AS county_key,
    MAX(ccrpi_score)           AS ccrpi_score
  FROM GA_LAND_INVESTABILITY.RAW.GOSA_SCHOOL_GRADES
  GROUP BY UPPER(TRIM(county_name))
),
joined AS (
  SELECT
    p.county_name,
    i.fips,
    p.pop_base_2020,
    p.pop_2025,
    p.pop_growth_pct,
    i.median_family_income,
    i.national_rank                             AS income_national_rank,
    s.ccrpi_score,
    CASE
      WHEN s.ccrpi_score >= 90 THEN 'A'
      WHEN s.ccrpi_score >= 80 THEN 'B'
      WHEN s.ccrpi_score >= 65 THEN 'C'
      WHEN s.ccrpi_score >= 50 THEN 'D'
      ELSE 'F'
    END                                         AS school_letter_grade,
    ROUND(
      LEAST(p.pop_growth_pct / 15.0, 1.0) * 40
      + LEAST(i.median_family_income / 120000.0, 1.0) * 35
      + COALESCE(s.ccrpi_score / 100.0, 0.5) * 25
    , 1) AS investability_score
  FROM pop p
  LEFT JOIN inc i ON p.county_key = i.county_key
  LEFT JOIN sch s ON p.county_key = s.county_key
)
SELECT *,
  CASE
    WHEN investability_score >= 70 THEN 'High'
    WHEN investability_score >= 50 THEN 'Medium'
    ELSE 'Low'
  END AS investability_tier
FROM joined
ORDER BY investability_score DESC;