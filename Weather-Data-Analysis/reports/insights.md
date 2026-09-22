# Key Insights — Weather Data Analysis

Dataset: 3,271 daily observations from a single, unidentified weather
station, spanning **2008-02-01 to 2017-06-25** (no City/Country field is
present — see Limitations in the final report).

### Temperature Insights

1. The average daily temperature across the full record is **18.9°C**
   (average MaxTemp 23.0°C, average MinTemp 14.9°C), with a typical daily
   range of **8.1°C** between the day's low and high.
2. The single hottest day on record was **2013-01-18, at 45.8°C**; the
   coldest was **2010-06-30, at 4.3°C** — a spread of over 41°C across the
   dataset.
3. **January** is the warmest month on average and **July** the coldest,
   consistent with a Southern-Hemisphere seasonal cycle (summer
   Dec–Feb, winter Jun–Aug) — the dataset's temperature and evaporation
   ranges are consistent with this pattern, though the location itself
   cannot be confirmed from the data alone.
4. Year-by-year average temperature moved from **17.7°C in 2008 to a peak
   of 20.8°C in 2017**, with most years in between sitting between 18–19.5°C.
   The 2017 figure should be read cautiously: that year only has data
   through June (175 days, all in the warmer half of the year), so it is
   not a fair full-year comparison and should not be read as a single-year
   temperature spike.

### Humidity Insights

5. Average humidity is noticeably higher in the morning than the
   afternoon — **68.2% at 9am vs. 54.7% at 3pm** — reflecting the typical
   daily humidity cycle as the day warms and dries out.
6. Humidity is negatively correlated with afternoon temperature
   (r ≈ **-0.15** between MaxTemp and Humidity3pm): hotter afternoons
   tend to be modestly drier, though the relationship is weak, not strong.

### Rainfall Insights

7. Total recorded rainfall across the ~9.4-year period is **10,932 mm**,
   averaging **3.3 mm/day**; **849 of 3,271 days (26.0%)** were recorded
   as rainy (`RainToday = Yes`).
8. The single wettest day was **2015-04-21, with 119.4 mm** of rain — more
   than 35× the daily average, and the most extreme rainfall anomaly in
   the dataset.
9. **June** has the highest total rainfall by month and Winter is the
   wettest season overall (**3,034 mm** across all winters combined) while
   Spring is the driest (**1,803 mm**) — rainfall and temperature move in
   largely opposite seasonal directions here.

### Wind Insights

10. The windiest recorded day was **2014-06-28, with a wind gust of
    96 km/h**, well above the typical daily gust range of 30–50 km/h.
11. **West (W)** is by far the dominant gust direction, recorded on 1,425
    of 3,271 days (43.6%) — but this concentration is partly a data-quality
    artifact rather than a pure meteorological signal (see Anomaly/Data
    Quality Insight #13 below).

### Location Insights

12. **Not available.** The dataset contains no City, Country, or Region
    column, so no cross-location comparison (hottest/coldest/wettest
    location, etc.) could be performed. This is a hard limitation of the
    source data, not a step that was skipped by choice.

### Anomaly / Data Quality Insight

13. A cluster of **1,144 rows (35% of the dataset)** share the exact same
    `WindGustSpeed` value of 41 km/h, and most of these (1,027 rows) also
    share `WindGustDir = W`. This is a strong signal that these values were
    **imputed or default-filled in an earlier processing stage** (before
    this file was produced) rather than independently measured each day.
    They were **not removed**, since 41 km/h and "W" are both plausible
    values individually and there's no basis to say which specific rows
    are wrong — but any wind-direction conclusions in this report should be
    read with that caveat in mind.
14. Using the IQR method independently on five key variables (MaxTemp,
    MinTemp, Rainfall, WindGustSpeed, Humidity3pm), **919 anomaly flags**
    were raised in total (a single day can trigger more than one flag).
    The large majority — **603 flags** — came from Rainfall, which is
    expected: rainfall is naturally right-skewed (most days have 0mm, a
    few days have very high totals), so IQR flags many genuine heavy-rain
    days rather than data errors. **266 flags** came from wind gust speed,
    **31** from max temperature, and **19** from humidity.
