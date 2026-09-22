# Weather Data Analysis & Dashboard

A data analysis project focused on cleaning historical weather data, exploring temperature, humidity, wind, and rainfall patterns, identifying anomalies, and designing an interactive Power BI dashboard.

## Project Overview

The goal of this project was to transform raw daily weather data into meaningful insights through data cleaning, exploratory analysis, statistical analysis, and dashboard design.

The analysis focuses on:

* Temperature trends and distributions
* Humidity patterns
* Wind speed and direction
* Rainfall patterns
* Monthly and seasonal changes
* Statistical anomalies
* Weather-related KPIs
* Power BI dashboard design

## Dataset

* **Records:** 3,271 daily observations
* **Raw columns:** 22
* **Engineered columns:** 14
* **Date range:** February 2008 – June 2017
* **Location:** Single unidentified weather station

The dataset contains weather variables including temperature, rainfall, humidity, wind speed and direction, atmospheric pressure, cloud cover, sunshine, and rain indicators.

## Data Cleaning

The dataset was checked for:

* Missing values
* Duplicate records
* Invalid or physically impossible values
* Date consistency
* Rainfall/rain indicator consistency
* Potential data-quality anomalies

No missing values, duplicate rows, or impossible readings were identified.

Additional data-quality checks revealed a small number of rainfall/rain-indicator boundary mismatches and a large repeated-value pattern in wind-gust data, which was documented as a potential upstream data issue rather than modified manually.

## Analysis

The exploratory analysis covered:

* Temperature distribution and trends
* Humidity distribution and trends
* Wind speed analysis
* Rainfall distribution and trends
* Monthly and seasonal comparisons
* Year-over-year temperature patterns
* Correlation analysis
* Temperature vs. humidity relationships
* Wind vs. rainfall relationships
* Statistical anomaly detection using the IQR method

All generated visualizations are available in the `charts/` directory.

## Key KPIs

The following KPIs were defined for monitoring weather conditions:

| KPI                           | Purpose                               |
| ----------------------------- | ------------------------------------- |
| Average Temperature           | Overall temperature level             |
| Maximum / Minimum Temperature | Temperature extremes                  |
| Average Temperature Range     | Daily temperature variation           |
| Average Humidity              | Overall humidity level                |
| Average / Maximum Wind Gust   | Wind intensity                        |
| Total Rainfall                | Overall precipitation                 |
| Average Rainfall              | Average precipitation per observation |
| Number of Rainy Days          | Rainfall frequency                    |
| Number of Observations        | Dataset coverage                      |
| Date Range                    | Analysis period                       |

## Key Insights

* Average temperature across the dataset was **18.9°C**.
* The highest recorded temperature was **45.8°C**, while the lowest was **4.3°C**.
* Total recorded rainfall was **10,932 mm**.
* Approximately **26% of observations were rainy days**.
* The highest daily rainfall was **119.4 mm**.
* The maximum recorded wind gust was **96 km/h**.
* **919 statistical anomaly flags** were identified using the IQR method, with rainfall accounting for most of them.
* Location-based comparisons could not be performed because the dataset does not contain city or country information.

## Power BI Dashboard

A four-page dashboard structure was designed:

1. **Weather Overview**
2. **Temperature & Humidity**
3. **Rainfall & Wind**
4. **Anomalies & Trends**

The dashboard is designed to support filtering by:

* Year
* Month
* Season
* Date range

The dashboard specifications and required DAX measures are available in the `dashboard/` directory.

## Technologies

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Power BI
* DAX
* Git & GitHub

## Project Structure

```text
Weather-Data-Analysis/
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

* The dataset contains no city, country, or regional information.
* 162 calendar days are missing from the date sequence.
* 2017 contains only partial-year data.
* Repeated wind-gust values may indicate an upstream imputation issue.
* A `.pbix` dashboard file was not included; instead, the dashboard structure and DAX measures are provided.

## Conclusion

This project demonstrates an end-to-end weather data analysis workflow, from raw data preparation and exploratory analysis to anomaly detection, KPI development, and Power BI dashboard planning.
