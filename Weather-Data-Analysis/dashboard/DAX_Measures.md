# DAX Measures — Weather Dashboard

Table name used below: **weather_cleaned** (the table created by importing
`data/cleaned/weather_cleaned.csv` into Power BI). Column names match the
cleaned dataset exactly (including the engineered columns `AvgTemp`,
`TempRange`, `AvgHumidity`, `AvgWindSpeed`, `Season`, `Year`, `Month`,
`MonthName`).

> Note: this dataset has **no City or Country column**, so no
> location-based measures (e.g. "City Count") are meaningful. A literal
> "N/A" measure is provided for `City Count` / `Country Count` only so the
> KPI cards on the dashboard don't break if reused from a template — do not
> present these as real metrics.

```dax
Average Temperature =
AVERAGE ( weather_cleaned[AvgTemp] )

Maximum Temperature =
MAX ( weather_cleaned[MaxTemp] )

Minimum Temperature =
MIN ( weather_cleaned[MinTemp] )

Temperature Range =
[Maximum Temperature] - [Minimum Temperature]

Average Daily Temperature Range =
AVERAGE ( weather_cleaned[TempRange] )

Average Humidity 9am =
AVERAGE ( weather_cleaned[Humidity9am] )

Average Humidity 3pm =
AVERAGE ( weather_cleaned[Humidity3pm] )

Maximum Humidity =
MAXX (
    weather_cleaned,
    MAX ( weather_cleaned[Humidity9am], weather_cleaned[Humidity3pm] )
)

Average Wind Gust Speed =
AVERAGE ( weather_cleaned[WindGustSpeed] )

Maximum Wind Gust Speed =
MAX ( weather_cleaned[WindGustSpeed] )

Total Rainfall =
SUM ( weather_cleaned[Rainfall] )

Average Rainfall =
AVERAGE ( weather_cleaned[Rainfall] )

Maximum Rainfall (Single Day) =
MAX ( weather_cleaned[Rainfall] )

Rainy Days =
CALCULATE (
    COUNTROWS ( weather_cleaned ),
    weather_cleaned[RainToday] = "Yes"
)

Rainy Day Percentage =
DIVIDE ( [Rainy Days], COUNTROWS ( weather_cleaned ), 0 )

Observation Count =
COUNTROWS ( weather_cleaned )

Date Range Start =
MIN ( weather_cleaned[Date] )

Date Range End =
MAX ( weather_cleaned[Date] )

City Count = "N/A"          -- dataset has no City column
Country Count = "N/A"       -- dataset has no Country column

-- Time-intelligence-style measures (no true DAX time intelligence,
-- since dates are not necessarily contiguous / no separate Date table
-- is assumed; a Date table is recommended if you build one)

Average Temp (Selected Season) =
CALCULATE ( [Average Temperature], ALLSELECTED ( weather_cleaned[Season] ) )

YoY Avg Temp Change =
VAR CurrentYear = SELECTEDVALUE ( weather_cleaned[Year] )
VAR CurrentAvg = [Average Temperature]
VAR PriorAvg =
    CALCULATE (
        [Average Temperature],
        FILTER ( ALL ( weather_cleaned ), weather_cleaned[Year] = CurrentYear - 1 )
    )
RETURN
    DIVIDE ( CurrentAvg - PriorAvg, PriorAvg, BLANK () )
```

## Measure usage notes

- Build all KPI cards on **Page 1 (Overview)** from: `Average Temperature`,
  `Average Humidity 9am` / `Average Humidity 3pm`, `Average Wind Gust Speed`,
  `Total Rainfall`, `Observation Count`.
- `Rainy Days` and `Rainy Day Percentage` use the existing `RainToday`
  column rather than re-deriving it, since it is already present and
  validated in the cleaned dataset.
- For the anomaly page, do **not** create a DAX measure that "detects"
  anomalies dynamically — anomalies were identified in Python with the IQR
  method (see `reports/anomalies.csv`) and should be loaded as a **separate
  table** (`anomalies`) and visualized directly, since DAX has no native
  IQR/outlier function.
