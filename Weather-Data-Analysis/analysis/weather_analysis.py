import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import json
import warnings

warnings.filterwarnings("ignore")

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 110
COLOR_MAIN = "#1f4e79"
COLOR_ACC = "#4a90d9"

RAW_PATH = "data/raw/weather_raw.csv"
CLEAN_PATH = "data/cleaned/weather_cleaned.csv"
CHART_DIR = "charts"


df = pd.read_csv(RAW_PATH)

inspection = {
    "n_rows": len(df),
    "n_cols": df.shape[1],
    "columns": list(df.columns),
    "dtypes": {c: str(t) for c, t in df.dtypes.items()},
    "missing_values": df.isnull().sum().to_dict(),
    "duplicate_rows": int(df.duplicated().sum()),
}



df["Date"] = pd.to_datetime(df["Date"], format="%m/%d/%Y", errors="coerce")
unparseable_dates = df["Date"].isnull().sum()

dup_rows = df.duplicated().sum()
dup_dates = df["Date"].duplicated().sum()
df = df.drop_duplicates()

missing_total = df.isnull().sum().sum()

checks = {}
checks["MinTemp_gt_MaxTemp"] = int((df["MinTemp"] > df["MaxTemp"]).sum())
checks["Humidity_out_of_range"] = int(
    (
        (df["Humidity9am"] < 0) | (df["Humidity9am"] > 100) |
        (df["Humidity3pm"] < 0) | (df["Humidity3pm"] > 100)
    ).sum()
)
checks["Negative_Rainfall"] = int((df["Rainfall"] < 0).sum())
checks["Negative_WindSpeed"] = int(
    ((df["WindSpeed9am"] < 0) | (df["WindSpeed3pm"] < 0) | (df["WindGustSpeed"] < 0)).sum()
)
checks["Cloud_out_of_0_9"] = int(
    (
        (df["Cloud9am"] < 0) | (df["Cloud9am"] > 9) |
        (df["Cloud3pm"] < 0) | (df["Cloud3pm"] > 9)
    ).sum()
)
checks["Sunshine_out_of_0_24"] = int(((df["Sunshine"] < 0) | (df["Sunshine"] > 24)).sum())
checks["RainToday_boundary_mismatch_at_1mm"] = int(
    (((df["RainToday"] == "Yes") & (df["Rainfall"] < 1)) |
     ((df["RainToday"] == "No") & (df["Rainfall"] >= 1))).sum()
)

valid_dirs = {"N","NNE","NE","ENE","E","ESE","SE","SSE","S","SSW","SW","WSW","W","WNW","NW","NNW"}
dir_cols = ["WindGustDir", "WindDir9am", "WindDir3pm"]
bad_dirs = {c: sorted(set(df[c].unique()) - valid_dirs) for c in dir_cols}

df = df.sort_values("Date").reset_index(drop=True)

full_range = pd.date_range(df["Date"].min(), df["Date"].max(), freq="D")
missing_days = full_range.difference(df["Date"])
n_missing_days = len(missing_days)


df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["MonthName"] = df["Date"].dt.month_name()
df["Day"] = df["Date"].dt.day
df["DayOfWeek"] = df["Date"].dt.day_name()
df["Quarter"] = df["Date"].dt.quarter


def to_season(month):
    
    if month in (12, 1, 2):
        return "Summer"
    elif month in (3, 4, 5):
        return "Autumn"
    elif month in (6, 7, 8):
        return "Winter"
    else:
        return "Spring"


df["Season"] = df["Month"].apply(to_season)

df["AvgTemp"] = (df["MinTemp"] + df["MaxTemp"]) / 2
df["TempRange"] = df["MaxTemp"] - df["MinTemp"]
df["AvgHumidity"] = (df["Humidity9am"] + df["Humidity3pm"]) / 2
df["AvgWindSpeed"] = (df["WindSpeed9am"] + df["WindSpeed3pm"]) / 2


def temp_category(t):
    if t < 10:
        return "Cold"
    elif t < 20:
        return "Mild"
    elif t < 30:
        return "Warm"
    else:
        return "Hot"


df["TempCategory"] = df["AvgTemp"].apply(temp_category)


def rainfall_category(r):
    if r == 0:
        return "No Rain"
    elif r < 2.5:
        return "Light"
    elif r < 15:
        return "Moderate"
    else:
        return "Heavy"


df["RainfallCategory"] = df["Rainfall"].apply(rainfall_category)


def humidity_category(h):
    if h < 30:
        return "Low"
    elif h < 60:
        return "Moderate"
    else:
        return "High"


df["HumidityCategory"] = df["AvgHumidity"].apply(humidity_category)


def wind_category(w):
    if w < 20:
        return "Calm"
    elif w < 40:
        return "Breezy"
    else:
        return "Strong"


df["WindCategory"] = df["WindGustSpeed"].apply(wind_category)

df.to_csv(CLEAN_PATH, index=False)


summary = {}

summary["temperature"] = {
    "avg_MaxTemp": round(df["MaxTemp"].mean(), 2),
    "avg_MinTemp": round(df["MinTemp"].mean(), 2),
    "min_MinTemp": round(df["MinTemp"].min(), 2),
    "max_MaxTemp": round(df["MaxTemp"].max(), 2),
    "avg_TempRange": round(df["TempRange"].mean(), 2),
}
summary["humidity"] = {
    "avg_Humidity9am": round(df["Humidity9am"].mean(), 2),
    "avg_Humidity3pm": round(df["Humidity3pm"].mean(), 2),
    "min_Humidity": int(min(df["Humidity9am"].min(), df["Humidity3pm"].min())),
    "max_Humidity": int(max(df["Humidity9am"].max(), df["Humidity3pm"].max())),
}
summary["wind"] = {
    "avg_WindGustSpeed": round(df["WindGustSpeed"].mean(), 2),
    "max_WindGustSpeed": round(df["WindGustSpeed"].max(), 2),
    "avg_WindSpeed9am": round(df["WindSpeed9am"].mean(), 2),
    "avg_WindSpeed3pm": round(df["WindSpeed3pm"].mean(), 2),
}
summary["rainfall"] = {
    "total_Rainfall": round(df["Rainfall"].sum(), 2),
    "avg_Rainfall": round(df["Rainfall"].mean(), 2),
    "max_Rainfall": round(df["Rainfall"].max(), 2),
    "rainy_days": int((df["Rainfall"] > 1).sum()),
    "rainy_day_pct": round((df["Rainfall"] > 1).mean() * 100, 1),
}

monthly_temp = df.groupby("MonthName")["AvgTemp"].mean().reindex(
    ["January","February","March","April","May","June","July",
     "August","September","October","November","December"]
)
seasonal_temp = df.groupby("Season")["AvgTemp"].mean().reindex(["Summer","Autumn","Winter","Spring"])
seasonal_rain = df.groupby("Season")["Rainfall"].sum().reindex(["Summer","Autumn","Winter","Spring"])
yearly_temp = df.groupby("Year")["AvgTemp"].mean()
yearly_rain = df.groupby("Year")["Rainfall"].sum()


def iqr_outliers(series, k=1.5):
    q1, q3 = series.quantile(0.25), series.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - k * iqr, q3 + k * iqr
    return lower, upper

anomaly_records = []
for col, label in [
    ("MaxTemp", "Unusually high/low max temperature"),
    ("MinTemp", "Unusually high/low min temperature"),
    ("Rainfall", "Extreme rainfall"),
    ("WindGustSpeed", "Unusually high wind gust"),
    ("Humidity3pm", "Unusually high/low humidity"),
]:
    lower, upper = iqr_outliers(df[col])
    outliers = df[(df[col] < lower) | (df[col] > upper)]
    for _, row in outliers.iterrows():
        anomaly_records.append({
            "Date": row["Date"].strftime("%Y-%m-%d"),
            "Variable": col,
            "ObservedValue": row[col],
            "NormalRange": f"{round(lower,1)} to {round(upper,1)}",
            "Type": label,
        })

anomalies_df = pd.DataFrame(anomaly_records).sort_values("Date")
anomalies_df.to_csv("reports/anomalies.csv", index=False)


corr_cols = ["MaxTemp","MinTemp","Rainfall","Evaporation","Sunshine",
             "WindGustSpeed","Humidity9am","Humidity3pm","Pressure9am","Pressure3pm"]
corr_matrix = df[corr_cols].corr()


kpis = {
    "Average Temperature (C)": round(df["AvgTemp"].mean(), 2),
    "Maximum Temperature Recorded (C)": round(df["MaxTemp"].max(), 2),
    "Minimum Temperature Recorded (C)": round(df["MinTemp"].min(), 2),
    "Average Temperature Range (C)": round(df["TempRange"].mean(), 2),
    "Average Humidity (%)": round(df["AvgHumidity"].mean(), 2),
    "Maximum Humidity (%)": int(max(df["Humidity9am"].max(), df["Humidity3pm"].max())),
    "Average Wind Gust Speed (km/h)": round(df["WindGustSpeed"].mean(), 2),
    "Maximum Wind Gust Speed (km/h)": round(df["WindGustSpeed"].max(), 2),
    "Total Rainfall (mm)": round(df["Rainfall"].sum(), 2),
    "Average Daily Rainfall (mm)": round(df["Rainfall"].mean(), 2),
    "Number of Rainy Days (>1mm)": int((df["Rainfall"] > 1).sum()),
    "Number of Observations": len(df),
    "Date Range": f"{df['Date'].min().date()} to {df['Date'].max().date()}",
    "Number of Cities": "N/A (dataset has no City column)",
    "Number of Countries": "N/A (dataset has no Country column)",
}



plt.figure(figsize=(8, 5))
sns.histplot(df["MaxTemp"], color=COLOR_MAIN, label="MaxTemp", kde=True, alpha=0.5)
sns.histplot(df["MinTemp"], color=COLOR_ACC, label="MinTemp", kde=True, alpha=0.5)
plt.title("Temperature Distribution")
plt.xlabel("Temperature (°C)")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/temperature_distribution.png")
plt.close()

plt.figure(figsize=(10, 5))
plt.plot(df["Date"], df["AvgTemp"], color=COLOR_MAIN, linewidth=0.6)
plt.plot(df["Date"], df["AvgTemp"].rolling(30).mean(), color="red", linewidth=1.5, label="30-day rolling avg")
plt.title("Average Temperature Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Average Temperature (°C)")
plt.legend()
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/temperature_trend.png")
plt.close()

plt.figure(figsize=(7, 5))
sns.barplot(x=seasonal_temp.index, y=seasonal_temp.values, color=COLOR_MAIN)
plt.title("Average Temperature by Season (Location data unavailable)")
plt.xlabel("Season")
plt.ylabel("Average Temperature (°C)")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/temperature_by_season.png")
plt.close()

plt.figure(figsize=(8, 5))
sns.histplot(df["Humidity9am"], color=COLOR_MAIN, label="Humidity 9am", kde=True, alpha=0.5)
sns.histplot(df["Humidity3pm"], color=COLOR_ACC, label="Humidity 3pm", kde=True, alpha=0.5)
plt.title("Humidity Distribution")
plt.xlabel("Humidity (%)")
plt.legend()
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/humidity_distribution.png")
plt.close()

plt.figure(figsize=(10, 5))
plt.plot(df["Date"], df["AvgHumidity"], color=COLOR_MAIN, linewidth=0.6)
plt.plot(df["Date"], df["AvgHumidity"].rolling(30).mean(), color="red", linewidth=1.5, label="30-day rolling avg")
plt.title("Average Humidity Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Average Humidity (%)")
plt.legend()
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/humidity_trend.png")
plt.close()

plt.figure(figsize=(8, 5))
sns.histplot(df["WindGustSpeed"], color=COLOR_MAIN, kde=True)
plt.title("Wind Gust Speed Distribution")
plt.xlabel("Wind Gust Speed (km/h)")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/wind_speed_distribution.png")
plt.close()

plt.figure(figsize=(10, 5))
plt.plot(df["Date"], df["WindGustSpeed"], color=COLOR_MAIN, linewidth=0.5)
plt.plot(df["Date"], df["WindGustSpeed"].rolling(30).mean(), color="red", linewidth=1.5, label="30-day rolling avg")
plt.title("Wind Gust Speed Trend Over Time")
plt.xlabel("Date")
plt.ylabel("Wind Gust Speed (km/h)")
plt.legend()
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/wind_speed_trend.png")
plt.close()

plt.figure(figsize=(8, 5))
sns.histplot(df[df["Rainfall"] > 0]["Rainfall"], color=COLOR_MAIN, kde=False, bins=40)
plt.title("Rainfall Distribution (Rainy Days Only)")
plt.xlabel("Rainfall (mm)")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/rainfall_distribution.png")
plt.close()

plt.figure(figsize=(10, 5))
monthly_rain = df.set_index("Date")["Rainfall"].resample("ME").sum()
plt.bar(monthly_rain.index, monthly_rain.values, width=20, color=COLOR_MAIN)
plt.title("Monthly Total Rainfall Over Time")
plt.xlabel("Month")
plt.ylabel("Total Rainfall (mm)")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/rainfall_trend.png")
plt.close()

fig, ax1 = plt.subplots(figsize=(9, 5))
ax1.bar(monthly_temp.index, monthly_temp.values, color=COLOR_ACC, alpha=0.7, label="Avg Temp (°C)")
ax1.set_ylabel("Average Temperature (°C)")
ax1.tick_params(axis="x", rotation=45)
ax2 = ax1.twinx()
monthly_rain_avg = df.groupby("MonthName")["Rainfall"].mean().reindex(monthly_temp.index)
ax2.plot(monthly_rain_avg.index, monthly_rain_avg.values, color="red", marker="o", label="Avg Rainfall (mm)")
ax2.set_ylabel("Average Rainfall (mm)")
plt.title("Monthly Temperature and Rainfall Comparison")
fig.legend(loc="upper right", bbox_to_anchor=(0.9, 0.88))
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/monthly_seasonal_comparison.png")
plt.close()

plt.figure(figsize=(9, 7))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", center=0)
plt.title("Correlation Heatmap of Weather Variables")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/correlation_heatmap.png")
plt.close()

lower_t, upper_t = iqr_outliers(df["MaxTemp"])
temp_anom = df[(df["MaxTemp"] < lower_t) | (df["MaxTemp"] > upper_t)]
plt.figure(figsize=(10, 5))
plt.plot(df["Date"], df["MaxTemp"], color=COLOR_MAIN, linewidth=0.5, label="MaxTemp")
plt.scatter(temp_anom["Date"], temp_anom["MaxTemp"], color="red", s=25, zorder=5, label="Anomaly (IQR method)")
plt.title("Max Temperature Anomalies Over Time")
plt.xlabel("Date")
plt.ylabel("Max Temperature (°C)")
plt.legend()
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/anomaly_analysis.png")
plt.close()

plt.figure(figsize=(7, 6))
sns.scatterplot(x="Humidity3pm", y="MaxTemp", data=df, alpha=0.3, color=COLOR_MAIN)
plt.title("Temperature vs Humidity (3pm)")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/scatter_temp_vs_humidity.png")
plt.close()

plt.figure(figsize=(7, 6))
sns.scatterplot(x="WindGustSpeed", y="Rainfall", data=df, alpha=0.3, color=COLOR_MAIN)
plt.title("Wind Gust Speed vs Rainfall")
plt.tight_layout()
plt.savefig(f"{CHART_DIR}/scatter_wind_vs_rainfall.png")
plt.close()


output = {
    "inspection": inspection,
    "cleaning": {
        "unparseable_dates": int(unparseable_dates),
        "duplicate_rows_removed": int(dup_rows),
        "duplicate_dates": int(dup_dates),
        "missing_values_total": int(missing_total),
        "validity_checks": checks,
        "invalid_wind_direction_codes": {k: v for k, v in bad_dirs.items()},
        "missing_calendar_days": int(n_missing_days),
        "final_row_count": len(df),
    },
    "summary_stats": summary,
    "monthly_avg_temp": monthly_temp.round(2).to_dict(),
    "seasonal_avg_temp": seasonal_temp.round(2).to_dict(),
    "seasonal_total_rain": seasonal_rain.round(2).to_dict(),
    "yearly_avg_temp": {int(k): round(v, 2) for k, v in yearly_temp.to_dict().items()},
    "yearly_total_rain": {int(k): round(v, 2) for k, v in yearly_rain.to_dict().items()},
    "kpis": kpis,
    "n_anomalies": len(anomalies_df),
    "correlation_highlights": {
        "MaxTemp_vs_Humidity3pm": round(df["MaxTemp"].corr(df["Humidity3pm"]), 3),
        "MaxTemp_vs_Sunshine": round(df["MaxTemp"].corr(df["Sunshine"]), 3),
        "Rainfall_vs_Sunshine": round(df["Rainfall"].corr(df["Sunshine"]), 3),
        "Rainfall_vs_Humidity3pm": round(df["Rainfall"].corr(df["Humidity3pm"]), 3),
        "Pressure9am_vs_MaxTemp": round(df["Pressure9am"].corr(df["MaxTemp"]), 3),
        "WindGustSpeed_vs_Rainfall": round(df["WindGustSpeed"].corr(df["Rainfall"]), 3),
    },
}

with open("reports/analysis_summary.json", "w") as f:
    json.dump(output, f, indent=2, default=str)

print("Analysis complete.")
print(json.dumps(output["cleaning"], indent=2, default=str))
print(json.dumps(output["kpis"], indent=2, default=str))
