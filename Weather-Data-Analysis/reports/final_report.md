# Weather Data Analysis — Final Report

Machine Learning Engineer Internship — Elevoo Pathways

## 1. Executive Summary

This project analyzes a daily weather dataset of 3,271 observations
spanning February 2008 to June 2017. The dataset was inspected, cleaned,
and enriched with time-based features, then explored across temperature,
humidity, wind, and rainfall dimensions. Statistically unusual
observations were identified using the IQR method, relationships between
variables were examined through correlation analysis, and a set of KPIs
and a four-page Power BI dashboard specification were developed. The
dataset does not include a City or Country field, so cross-location
comparison — one of the tasks requested in the project brief — could not
be performed; this is documented as a limitation rather than worked
around with invented data.

## 2. Dataset Description

- **File:** `Weather_Data.csv` (3,271 rows × 22 columns)
- **Grain:** one row per calendar day
- **Date range:** 2008-02-01 to 2017-06-25 (162 calendar days are absent
  from the sequence — gaps in collection, not missing values within
  existing rows)
- **Columns:** `Date`, `MinTemp`, `MaxTemp`, `Rainfall`, `Evaporation`,
  `Sunshine`, `WindGustDir`, `WindGustSpeed`, `WindDir9am`, `WindDir3pm`,
  `WindSpeed9am`, `WindSpeed3pm`, `Humidity9am`, `Humidity3pm`,
  `Pressure9am`, `Pressure3pm`, `Cloud9am`, `Cloud3pm`, `Temp9am`,
  `Temp3pm`, `RainToday`, `RainTomorrow`
- **No City or Country column exists.** The variable set (MinTemp/MaxTemp,
  Evaporation, Sunshine, WindGustDir, Cloud oktas, `RainToday`/
  `RainTomorrow`) matches the structure commonly used for Australian daily
  weather station data, but the specific location cannot be confirmed
  from the file itself and is not stated anywhere in it, so no location
  name is assumed or invented anywhere in this project.

### What the key columns represent

- `MinTemp` / `MaxTemp`: the day's minimum and maximum air temperature (°C)
- `Temp9am` / `Temp3pm`: point-in-time temperature readings at 9am and 3pm (°C)
- `Rainfall`: total rainfall recorded for the day (mm)
- `Evaporation`: Class A pan evaporation for the day (mm)
- `Sunshine`: hours of bright sunshine recorded during the day
- `WindGustDir` / `WindGustSpeed`: direction and speed (km/h) of the day's strongest wind gust
- `WindDir9am/3pm`, `WindSpeed9am/3pm`: wind direction/speed at the two observation times
- `Humidity9am` / `Humidity3pm`: relative humidity (%) at the two observation times
- `Pressure9am` / `Pressure3pm`: atmospheric pressure (hPa) at the two observation times
- `Cloud9am` / `Cloud3pm`: cloud cover in oktas (0–9 scale)
- `RainToday` / `RainTomorrow`: binary Yes/No flags for rain on the current/next day

## 3. Data Cleaning

**Data quality findings:**
- 0 missing values in any column
- 0 fully duplicate rows, 0 duplicate dates
- 0 rows with MinTemp > MaxTemp, negative rainfall/wind speed, humidity
  outside 0–100%, cloud cover outside 0–9, or sunshine outside 0–24 hours
- 0 invalid wind-direction codes (all values fall within the 16 standard
  compass points)
- 37 rows (1.1%) where `RainToday` disagrees with `Rainfall` exactly at
  the 1.0mm boundary (e.g. Rainfall = 1.0mm but RainToday = "No"). This is
  a rounding/threshold artifact at the boundary itself, not a data error,
  and was **left as-is** rather than "corrected" without a documented
  source rule.
- **Notable finding:** 1,144 rows (35%) share an identical
  `WindGustSpeed` of 41 km/h, 1,027 of which also share `WindGustDir = W`.
  This strongly suggests these particular values were imputed/default-filled
  upstream of this file rather than independently measured. They were
  **retained** (each value is individually plausible) but are flagged as a
  known data-quality caveat rather than treated as ground truth.

**Cleaning steps applied:**
1. Parsed `Date` from `M/D/YYYY` text into a proper date type
2. Sorted rows chronologically and reset the index
3. Verified there were no duplicates or missing values to handle (none found)
4. Verified there were no impossible values to correct (none found)
5. Saved the result to `data/cleaned/weather_cleaned.csv`

No rows were dropped and no values were imputed, because the dataset
did not contain missing values or invalid values requiring correction —
its only quality issues (documented above) are non-destructive to leave
in place.

## 4. Exploratory Data Analysis

See `charts/` for all supporting visuals and `reports/insights.md` for the
full set of numbered insights. Summary highlights are repeated by section
below.

## 5. Temperature Analysis

Average temperature 18.9°C (MaxTemp avg 23.0°C, MinTemp avg 14.9°C),
average daily range 8.1°C. Hottest day: 45.8°C (2013-01-18). Coldest day:
4.3°C (2010-06-30). Warmest month: January. Coldest month: July.

## 6. Humidity Analysis

Average humidity 68.2% at 9am vs. 54.7% at 3pm — a consistent morning-to-
afternoon drying pattern. Humidity ranges from 10% to 100% across the
dataset. Afternoon humidity is weakly negatively correlated with afternoon
temperature (r ≈ -0.15).

## 7. Wind Speed Analysis

Average wind gust speed 41.5 km/h; maximum recorded gust 96 km/h
(2014-06-28). West (W) is the dominant gust direction (43.6% of days),
though this figure is affected by the imputation artifact noted in
Section 3.

## 8. Rainfall Analysis

Total rainfall over the period: 10,932 mm. Average 3.3 mm/day. 26.0% of
days recorded measurable rain (>1mm). Wettest single day: 119.4 mm
(2015-04-21). June is the wettest month; Winter is the wettest season
(3,034 mm total) and Spring the driest (1,803 mm total).

## 9. Time-Based Analysis

Year-over-year average temperature ranged from 17.7°C (2008) to 20.8°C
(2017), broadly trending upward across the period, but 2017 is a partial
year (data through June only, biased toward warmer months) and should not
be read as a genuine single-year jump. No claim of a "climate change"
trend is made here — the dataset covers roughly 9.4 years at a single
location, which is not sufficient to support a climate-scale conclusion;
the wording used throughout is "temperature was higher/lower during the
observed period."

## 10. Location Analysis

**Not possible.** The dataset has no City, Country, or Region column.
This entire analysis step from the project brief could not be performed
and is not simulated or faked; see Limitations below.

## 11. Anomaly Analysis

Using the IQR method (1.5× IQR beyond Q1/Q3) independently per variable
across MaxTemp, MinTemp, Rainfall, WindGustSpeed, and Humidity3pm, 919
anomaly flags were raised (a day can be flagged on more than one
variable): 603 from Rainfall, 266 from WindGustSpeed, 31 from MaxTemp,
and 19 from Humidity3pm. The large share of rainfall-based flags reflects
rainfall's naturally skewed distribution (mostly zero, with occasional
large totals) rather than data error. Full detail is in
`reports/anomalies.csv`.

## 12. Correlation Analysis

Key relationships identified (Pearson correlation):

| Pair | r |
|---|---|
| MaxTemp vs Humidity3pm | -0.151 |
| MaxTemp vs Sunshine | 0.327 |
| Rainfall vs Sunshine | -0.309 |
| Rainfall vs Humidity3pm | 0.306 |
| Pressure9am vs MaxTemp | -0.386 |
| WindGustSpeed vs Rainfall | 0.150 |

All relationships are moderate at best. None of these are interpreted as
causal — they describe observed statistical association only (e.g. lower
pressure tends to coincide with warmer afternoons in this dataset; this is
a correlation, not a causal claim).

## 13. KPI Selection

| KPI | Value | Why it's useful |
|---|---|---|
| Average Temperature | 18.9°C | Headline climate indicator |
| Max / Min Temperature Recorded | 45.8°C / 4.3°C | Shows the extremes the location experiences |
| Average Temperature Range | 8.1°C | Indicates daily volatility |
| Average Humidity | 61.5% | Overall moisture indicator |
| Average / Max Wind Gust Speed | 41.5 / 96 km/h | Wind exposure and peak-event risk |
| Total Rainfall | 10,932 mm | Cumulative water input over the period |
| Number of Rainy Days | 849 (26.0%) | Frequency, not just volume, of rain |
| Number of Observations | 3,271 | Confirms data coverage/completeness |
| Date Range | 2008-02-01 – 2017-06-25 | Frames all other KPIs in time |

City Count / Country Count were intentionally **excluded** as KPIs since
the data cannot support them.

## 14. Dashboard Overview

A 4-page Power BI dashboard was specified (full build steps in
`dashboard/Dashboard_Specification.md`, measures in
`dashboard/DAX_Measures.md`): **Weather Overview**, **Temperature &
Humidity**, **Rainfall & Wind**, and **Weather Anomalies / Trends**, each
filterable by Year, Month, Season, and date range. A `.pbix` binary file
could not be produced in this text-based environment, so the
specification is provided in full detail for direct rebuild in Power BI
Desktop.

## 15. Key Findings

See `reports/insights.md` for the full numbered list (14 insights across
temperature, humidity, rainfall, wind, location, and data-quality/anomaly
categories).

## 16. Limitations

1. **No location data.** No City, Country, or Region column exists, so
   Step 6 of the brief (location comparison) could not be performed at
   all — not partially, not approximately.
2. **The location itself is unconfirmed.** The column structure resembles
   Australian daily weather station data, but this is not stated in the
   file and is not treated as fact anywhere in the analysis or dashboard.
3. **162 calendar days are absent** from the date sequence (gaps in
   collection), which slightly limits the precision of day-level trend
   and rolling-average calculations across those gaps.
4. **2017 is a partial year** (through June only), which biases its
   average temperature upward relative to full years and should not be
   compared directly to them.
5. **WindGustSpeed/WindGustDir show a likely-imputed cluster** (35% of
   rows share the same value), which limits how much confidence should be
   placed in wind-direction-specific conclusions.
6. Correlation values reported are descriptive only; none imply causation.

## 17. Conclusion

The dataset is well-formed and largely clean at the row level (no missing
values, no duplicates, no impossible readings), which made data cleaning
straightforward. It supports a solid temperature, humidity, wind, and
rainfall analysis with clear seasonal and time-based patterns, and
912+ anomaly flags give a concrete anomaly layer for the dashboard.
Its one structural gap — no location field — means the project cannot
deliver the location-comparison component requested in the brief; every
other requested component (cleaning, feature engineering, EDA, time
analysis, anomaly detection, correlation analysis, KPIs, dashboard
specification, DAX measures, insights, and this report) has been
completed using only the real values present in the file.
