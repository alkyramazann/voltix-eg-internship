# Power BI Dashboard — Specification & Build Steps

**A `.pbix` file cannot be generated in this environment** (Power BI Desktop
is a Windows application and isn't available here). What follows is a
complete, ready-to-build specification: the exact data sources, pages,
visuals, filters, and DAX measures needed to recreate the dashboard in
Power BI Desktop in a few minutes.

## 1. Data sources to load

1. `data/cleaned/weather_cleaned.csv` → main table, rename to `weather_cleaned`
2. `reports/anomalies.csv` → secondary table, rename to `anomalies`

In Power Query, set `Date` to **Date** type in both tables, and confirm
`Year`, `Month`, `Quarter` import as whole numbers.

Load the DAX measures from `dashboard/DAX_Measures.md` into `weather_cleaned`.

## 2. Global filters / slicers (added to every page via a filter pane or a sync'd slicer)

- **Year** (slicer, `weather_cleaned[Year]`)
- **Month** (slicer, `weather_cleaned[MonthName]`)
- **Season** (slicer, `weather_cleaned[Season]`)
- **Date range** (between slicer, `weather_cleaned[Date]`)

> City/Country/Region slicers are **not included** — the dataset contains
> no location column, so a location filter would be meaningless here.

## 3. Page 1 — Weather Overview

**KPI cards (top row):**
Observation Count · Average Temperature · Average Humidity 9am/3pm ·
Average Wind Gust Speed · Total Rainfall · Rainy Days

**Visuals:**
- Line chart: `Average Temperature` by `Date` (use `temperature_trend.png` as the Python reference)
- Bar/column chart: `Total Rainfall` by `Date` (monthly grain — drill down enabled)
- Bar chart: Average Temperature by `Season`
- Combo chart: Average Temperature (line) + Average Rainfall (bar) by `MonthName`

## 4. Page 2 — Temperature & Humidity

**KPI cards:** Average Temperature · Maximum Temperature · Minimum Temperature · Average Humidity 9am · Average Humidity 3pm

**Visuals:**
- Line chart: `MaxTemp` and `MinTemp` trend by `Date`
- Line chart: `Humidity9am` and `Humidity3pm` trend by `Date`
- Scatter chart: `MaxTemp` (x) vs `Humidity3pm` (y) — matches `scatter_temp_vs_humidity.png`
- Table: Monthly average Temp / Humidity

Filter interactions: Year, Month, Season, Date range slicers apply.

## 5. Page 3 — Rainfall & Wind

**KPI cards:** Total Rainfall · Average Rainfall · Maximum Rainfall (Single Day) · Average Wind Gust Speed · Maximum Wind Gust Speed

**Visuals:**
- Column chart: Total Rainfall by Month
- Line chart: Wind Gust Speed trend by Date
- Scatter chart: Wind Gust Speed (x) vs Rainfall (y) — matches `scatter_wind_vs_rainfall.png`
- Donut/bar chart: count of days by `WindCategory` (Calm / Breezy / Strong)

## 6. Page 4 — Weather Anomalies / Trends

**Data source:** `anomalies` table (loaded from `reports/anomalies.csv`)

**Visuals:**
- Table/matrix: `anomalies` filtered/grouped by `Variable`, showing Date, ObservedValue, NormalRange, Type
- Bar chart: count of anomalies by `Variable` (Type)
- Line chart: `MaxTemp` trend from `weather_cleaned` with anomaly dates highlighted (use a second series filtered to `anomalies[Variable] = "MaxTemp"`, joined on Date)
- Card: total anomaly count

Add a text box calling out that:
- Anomalies were identified using the **IQR method** (1.5×IQR beyond Q1/Q3), per numeric variable, independently.
- An anomaly is a **statistically unusual observation**, not automatically a data error — see `reports/insights.md` for interpretation.

## 7. Theme

- Palette: dark blue `#1F4E79` (primary), mid blue `#4A90D9` (accent), white
  background, red `#D64545` reserved only for anomaly/alert markers.
- Font: Segoe UI (Power BI default) for consistency and readability.
- Consistent KPI card style across all 4 pages; page navigation buttons at
  the top of each page.

## 8. Known limitation carried into the dashboard

Because the source data has no City/Country/Region field, **Step 6
(Location Analysis) from the project brief cannot be built** — there is
nothing to compare across locations. This is called out explicitly in
`reports/final_report.md` under Limitations, and no location slicer or
visual is included anywhere in the dashboard so as not to imply data that
doesn't exist.
