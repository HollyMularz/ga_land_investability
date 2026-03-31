import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# ── 1. Census Population (XLSX) ──────────────────────────────────────
pop_raw = pd.read_excel(
    'co-est2025-pop-13.xlsx',
    header=None,
    skiprows=4,
    usecols=[0, 1, 2, 3, 4, 5, 6, 7]
)
pop_raw.columns = ['county_name','pop_base_2020','pop_2020','pop_2021',
                   'pop_2022','pop_2023','pop_2024','pop_2025']

pop = pop_raw[pop_raw['county_name'].str.startswith('.', na=False)].copy()
pop['county_name'] = pop['county_name'].str.lstrip('.').str.replace(', Georgia','',regex=False).str.replace(' County','',regex=False).str.strip()
pop['pop_growth_pct'] = ((pop['pop_2025'] - pop['pop_base_2020']) / pop['pop_base_2020'] * 100).round(2)
pop = pop.reset_index(drop=True)
pq.write_table(pa.Table.from_pandas(pop), 'census_population.parquet')
print(f'Population: {len(pop)} rows written')

# ── 2. HDPulse Income (CSV) ──────────────────────────────────────────
inc_raw = pd.read_csv('HDPulse_data_export.csv', skiprows=4)
inc_raw.columns = ['county_name','fips','median_family_income_raw','national_rank']
inc = inc_raw[inc_raw['fips'].between(13001, 13321)].copy()
inc['median_family_income'] = (inc['median_family_income_raw'].str.replace(',','',regex=False).astype(int))
inc['county_name'] = inc['county_name'].str.replace(' County','',regex=False).str.strip()
inc['fips'] = inc['fips'].astype(int)
inc = inc[['county_name','fips','median_family_income','national_rank']].reset_index(drop=True)
pq.write_table(pa.Table.from_pandas(inc), 'hdpulse_income.parquet')
print(f'Income: {len(inc)} rows written')

# ── 3. GOSA School Grades ──────────────────────────────────────────
gosa_raw = pd.read_csv('2025SchoolGrades_data/school_grades_data.csv', low_memory=False)

gosa = gosa_raw[gosa_raw['Level'] == 'DISTRICT'].copy()
gosa['ccrpi_score'] = gosa[['CCRPISCOREE', 'CCRPISCOREM', 'CCRPISCOREH']].mean(axis=1).round(2)
gosa['county_name'] = gosa['SYSTEMNAME'].str.replace(' County', '', regex=False).str.strip()
gosa = gosa.rename(columns={
    'SYSTEMID':   'system_id',
    'SYSTEMNAME': 'system_name',
    'GRADES':     'letter_grade',
})
gosa = gosa[['system_id', 'system_name', 'letter_grade', 'ccrpi_score', 'county_name']].reset_index(drop=True)
pq.write_table(pa.Table.from_pandas(gosa), 'gosa_school_grades.parquet')
print(f'GOSA School Grades: {len(gosa)} rows written')
