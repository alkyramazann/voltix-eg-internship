# Video Game Industry Analysis

An end-to-end data analysis project exploring the video game industry through data cleaning, exploratory data analysis, feature engineering, and interactive dashboards.

The project analyzes video game releases, sales performance, genres, platforms, publishers, ratings, and industry trends using a cleaned dataset of **16,715 games**.

---

## Project Overview

The goal of this project is to understand the main patterns and trends in the video game industry and identify factors associated with game releases and sales performance.

The project covers the complete data analysis workflow:

* Data understanding and quality assessment
* Data cleaning and preprocessing
* Feature engineering
* Exploratory Data Analysis (EDA)
* Statistical analysis
* Data visualization
* Business and industry insights
* Interactive Excel dashboard
* Interactive Streamlit dashboard

---

## Project Structure

```text
Video-Game-Industry-Analysis/
│
├── data/
│   ├── cleaned_video_games.csv
│   ├── cleaning_log.csv
│   └── raw/
│       ├── ...
│       ├── ...
│       └── ...
│
├── notebook/
│   └── Video_Game_Analysis.ipynb
│
├── charts/
│   ├── chart_01.png
│   ├── chart_02.png
│   ├── ...
│   └── chart_13.png
│
├── dashboard/
│   ├── Video_Game_Dashboard.xlsx
│   ├── app.py
│   └── requirements.txt
│
├── clean.py
├── Video_Game_Analysis_Summary.docx
└── README.md
```

---

## Dataset

The original dataset consists of three CSV files containing information about video games.

After cleaning and preprocessing, the final dataset contains:

* **16,715 rows**
* **23 columns**
* Original game, platform, genre, publisher, rating, and sales information
* Additional engineered features created during the analysis

The cleaned dataset is available at:

```text
data/cleaned_video_games.csv
```

---

## Data Cleaning

The raw data contained several quality issues that needed to be addressed before analysis.

The cleaning pipeline includes:

* Handling missing values
* Removing or resolving duplicate records
* Standardizing categorical variables
* Converting columns to appropriate data types
* Cleaning numerical sales variables
* Handling inconsistent values
* Validating year-related fields
* Creating derived variables
* Checking the final dataset for consistency

Every cleaning operation is documented in:

```text
data/cleaning_log.csv
```

The same preprocessing workflow can also be executed independently using:

```bash
python clean.py
```

---

## Exploratory Data Analysis

The notebook investigates several aspects of the video game industry, including:

### Industry Trends

* Number of game releases over time
* Changes in the industry across different periods
* Sales trends

### Genre Analysis

* Most common game genres
* Genre popularity
* Sales performance by genre

### Platform Analysis

* Most frequently used platforms
* Platform sales performance
* Platform maker comparisons

### Publisher Analysis

* Leading publishers
* Publisher release activity
* Sales performance of major publishers

### Game Performance

* Distribution of game sales
* Average sales per release
* Differences between genres and platforms

### Ratings

* ESRB rating distribution
* Relationship between ratings and game performance

The complete analysis is available in:

```text
notebook/Video_Game_Analysis.ipynb
```

---

## Interactive Excel Dashboard

The project includes an interactive Excel dashboard designed for exploring the dataset without directly working with the raw data.

```text
dashboard/Video_Game_Dashboard.xlsx
```

### Dashboard Filters

The main dashboard includes dropdown filters for:

* Genre
* Platform Maker
* Year From
* Year To

### Key Performance Indicators

The dashboard dynamically displays:

* Total Releases
* Total Sales
* Top Genre
* Top Platform
* Top Publisher
* Average Sales per Release

It also contains **8 interactive charts** that update based on the selected filters.

### Workbook Structure

| Sheet          | Description                         |
| -------------- | ----------------------------------- |
| `Dashboard`    | Main interactive dashboard          |
| `Data`         | Cleaned dataset and filter logic    |
| `Calc`         | Calculation and chart feeder tables |
| `Insights`     | Main findings and observations      |
| `Cleaning_Log` | Data cleaning documentation         |

> **Note:** The Excel dashboard is designed for desktop Excel. If some values initially appear as `0`, use **Ctrl + Alt + F9** to force a full recalculation.

---

## Streamlit Dashboard

A second interactive version of the dashboard was developed using Streamlit.

It allows users to dynamically filter the dataset and explore the results through an interactive web interface.

### Available Filters

* Genre
* Platform Maker
* Platform
* Year Range
* ESRB Rating

### Run the Dashboard

Install the required packages:

```bash
pip install -r dashboard/requirements.txt
```

Then run:

```bash
streamlit run dashboard/app.py
```

The dashboard will open automatically in your browser.

---

## Visualizations

The project contains **13 visualizations** generated during the analysis.

They cover areas such as:

* Release trends
* Sales trends
* Genre distribution
* Platform performance
* Publisher performance
* Rating distribution
* Comparative industry analysis

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* SciPy
* Jupyter Notebook
* Excel
* Streamlit

---

## Key Deliverables

| File                               | Description                                                   |
| ---------------------------------- | ------------------------------------------------------------- |
| `Video_Game_Analysis_Summary.docx` | Written summary of data issues, findings, and recommendations |
| `cleaned_video_games.csv`          | Final cleaned dataset                                         |
| `cleaning_log.csv`                 | Complete data cleaning log                                    |
| `Video_Game_Analysis.ipynb`        | Full analysis notebook                                        |
| `clean.py`                         | Standalone data cleaning pipeline                             |
| `Video_Game_Dashboard.xlsx`        | Interactive Excel dashboard                                   |
| `app.py`                           | Streamlit dashboard                                           |
| `charts/`                          | Generated visualizations                                      |

---

## Reproducing the Analysis

Install the required Python packages:

```bash
pip install pandas numpy matplotlib seaborn scipy jupyter
```

Then open:

```text
notebook/Video_Game_Analysis.ipynb
```

The notebook uses relative paths, so it should be opened from the project structure provided above.

---

## Project Focus

This project demonstrates an end-to-end approach to data analysis, starting from raw and inconsistent data and progressing through cleaning, feature engineering, exploratory analysis, visualization, and interactive reporting.

It is designed to demonstrate practical skills in **Python, data cleaning, exploratory data analysis, visualization, Excel dashboards, and data-driven business insights**.
