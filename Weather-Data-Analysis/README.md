# Weather Data Analysis & Dashboard

A data cleaning, exploratory analysis, and dashboard-specification project
built on a real daily weather dataset — cleaning the data, analyzing
temperature/humidity/wind/rainfall patterns over time, detecting
statistical anomalies, and translating the findings into KPIs and a
Power BI dashboard design.

This project was completed as part of my Machine Learning Engineer
Internship at **Elevoo Pathways**.

## Project Overview

A weather data platform wants to understand temperature, humidity, wind,
and rainfall patterns from historical daily weather records: what the
normal ranges look like, how conditions change across months and seasons,
which observations are statistically unusual, and which KPIs and
dashboard views would be most useful for ongoing monitoring.

## Objectives

- Clean and prepare historical weather data
- Analyze temperature, humidity, rainfall, and wind speed
- Identify temporal patterns (monthly, seasonal, yearly)
- Detect unusual/anomalous observations
- Develop meaningful weather KPIs
- Specify an interactive Power BI dashboard
- Extract actionable, number-backed insights

## Dataset

- **Records:** 3,271 daily observations
- **Columns:** 22 raw columns (temperature, rainfall, evaporation,
  sunshine, wind direction/speed, humidity, pressure, cloud cover, and
  rain flags) + 14 engineered columns (Year, Month, MonthName, Day,
  DayOfWeek, Quarter, Season, AvgTemp, TempRange, AvgHumidity,
  AvgWindSpeed, TempCategory, RainfallCategory, HumidityCategory,
  WindCategory)
- **Date range:** 2008-02-01 to 2017-06-25
- **Locations:** none recorded — the dataset has **no City or Country
  column**. All analysis in this project reflects a single, unidentified
  station/location; see `reports/final_report.md` → Limitations.

## Data Cleaning

The raw data had **no missing values, no duplicate rows, and no
impossible readings** (temperatures, humidity %, wind speed, cloud cover,
and rainfall were all within valid physical ranges). Cleaning consisted of
parsing the date column into a proper date type, sorting chronologically,
and documenting two non-destructive quality notes: a small set of
boundary mismatches between `Rainfall` and `RainToday` at exactly 1.0mm,
and a large (35% of rows) cluster of identical `WindGustSpeed`/`WindGustDir`
values that looks like an upstream imputation artifact. Full detail in
`reports/final_report.md`.

## Exploratory Data Analysis

Covered temperature, humidity, wind, and rainfall distributions and
trends; monthly/seasonal comparisons; a year-over-year temperature view;
and scatter/correlation analysis between temperature, humidity, sunshine,
pressure, wind, and rainfall. All charts are in `charts/`.

## Key KPIs

Average Temperature, Max/Min Temperature, Average Temperature Range,
Average Humidity, Average/Max Wind Gust Speed, Total Rainfall, Average
Rainfall, Number of Rainy Days, Number of Observations, Date Range. (See
`reports/final_report.md` §13 for the full table with values and
rationale.)

## Dashboard

A 4-page Power BI dashboard was specified — **Weather Overview**,
**Temperature & Humidity**, **Rainfall & Wind**, and **Weather Anomalies /
Trends** — each filterable by Year, Month, Season, and date range. A
`.pbix` binary could not be generated in this text-based environment, so
`dashboard/Dashboard_Specification.md` gives the exact pages, visuals, and
filters, and `dashboard/DAX_Measures.md` gives every DAX measure needed,
ready to paste into Power BI Desktop against `data/cleaned/weather_cleaned.csv`.

## Key Insights

- Average temperature 18.9°C; hottest day 45.8°C (2013-01-18), coldest
  4.3°C (2010-06-30); January warmest month, July coldest.
- Total rainfall 10,932 mm over the period; 26.0% of days were rainy;
  wettest day 119.4 mm (2015-04-21); June wettest month, Winter wettest
  season, Spring driest.
- Windiest recorded gust 96 km/h (2014-06-28); West is the dominant gust
  direction, though partly influenced by a likely data-imputation artifact.
- 919 statistical anomaly flags identified via the IQR method, the
  majority (603) from rainfall's naturally skewed distribution.
- Location-based comparison could not be performed — no location data
  exists in the source file.

Full list with all 14 insights: `reports/insights.md`.

## Technologies

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Power BI
- DAX
- Git/GitHub

## Project Structure

```text
weather-data-analysis/
│
├── data/
│   ├── raw/
│   │   └── weather_raw.csv
│   └── cleaned/
│       └── weather_cleaned.csv
│
├── analysis/
│   └── weather_analysis.py
│
├── charts/
│   ├── temperature_distribution.png
│   ├── temperature_trend.png
│   ├── temperature_by_season.png
│   ├── humidity_distribution.png
│   ├── humidity_trend.png
│   ├── wind_speed_distribution.png
│   ├── wind_speed_trend.png
│   ├── rainfall_distribution.png
│   ├── rainfall_trend.png
│   ├── monthly_seasonal_comparison.png
│   ├── correlation_heatmap.png
│   ├── anomaly_analysis.png
│   ├── scatter_temp_vs_humidity.png
│   └── scatter_wind_vs_rainfall.png
│
├── dashboard/
│   ├── Dashboard_Specification.md
│   └── DAX_Measures.md
│
├── reports/
│   ├── analysis_summary.json
│   ├── anomalies.csv
│   ├── insights.md
│   └── final_report.md
│
├── requirements.txt
└── README.md
```

## Limitations

- No City/Country/Region field — location-based analysis and dashboard
  filters are not possible with this dataset.
- 162 calendar days are missing from the date sequence (gaps in
  collection).
- 2017 is a partial year (through June only) and is not directly
  comparable to full years in yearly aggregates.
- A likely-imputed cluster in `WindGustSpeed`/`WindGustDir` (35% of rows)
  limits confidence in wind-direction-specific conclusions.
- A real `.pbix` file could not be produced in this environment; a full
  build specification is provided instead.

See `reports/final_report.md` for complete details.
