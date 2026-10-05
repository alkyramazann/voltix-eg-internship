# Task 11 - Video Game Industry Analysis

## Package contents
| Path | What it is |
|---|---|
| `Video_Game_Analysis_Summary.docx` | Short written summary: data issues, key findings, recommendations |
| `data/cleaned_video_games.csv` | Cleaned dataset (16,715 rows, 23 columns incl. engineered features) |
| `data/cleaning_log.csv` | Every cleaning step and the rows it affected |
| `data/raw/` | Original 3 CSV files from Video_Games.zip |
| `notebook/Video_Game_Analysis.ipynb` | Full analysis (understanding, cleaning, EDA, charts, insights); already executed |
| `clean.py` | Same cleaning pipeline as a standalone script |
| `charts/` | 13 PNG visualizations produced by the notebook |
| `dashboard/Video_Game_Dashboard.xlsx` | **Excel interactive dashboard** (see below) |
| `dashboard/app.py` | **Streamlit interactive dashboard** (optional second version) |

## Excel dashboard
Open `Dashboard` sheet, use the yellow dropdown cells (Genre, Platform Maker, Year From/To). KPIs (releases, total sales, top genre / platform / publisher, avg sales per release) and 8 charts update through formulas. Other sheets: `Data` (cleaned data + filter flag), `Calc` (chart feeder tables), `Insights`, `Cleaning_Log`. Works in desktop Excel; if values show as 0 after opening, press Ctrl+Alt+F9 to recalculate.

## Streamlit dashboard
```
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```
Sidebar filters: genre, platform maker, platform, year range, ESRB rating.

## Re-run the notebook
`pip install pandas numpy matplotlib seaborn scipy jupyter`, then open the notebook from the `notebook/` folder (paths are relative).
