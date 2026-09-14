# Employee Data Analysis - Attrition & Performance

## Project Overview
This project analyzes an HR dataset of 1,470 employees to understand
performance, salaries, satisfaction, and — most importantly — why
employees leave the company. It was built as part of a CodeAlpha Data
Analytics internship task.

## Business Problem
The company wants to understand its workforce and, specifically, what's
driving employee attrition, with a particular focus on overtime, job
satisfaction, and work-life balance, so management can act on the
findings.

## Dataset Description
The dataset is the IBM HR Analytics Employee Attrition dataset
(`data/employee_data_original.csv`), containing 1,470 employees and 35
columns covering demographics, compensation, job role, performance
ratings, satisfaction scores, and attrition status.

## Data Cleaning Steps
- Checked for missing values and duplicate rows — none were found.
- Stripped leading/trailing whitespace from all text columns.
- Dropped three constant, non-informative columns: `EmployeeCount`
  (always 1), `Over18` (always "Y"), `StandardHours` (always 80).
- Investigated outliers in salary, experience, tenure, and number of
  companies worked using the IQR method. These were kept rather than
  removed — they reflect real, plausible employees (e.g. senior staff
  with long tenure or high pay), not data-entry errors.
- Added two helper columns: `AttritionFlag` (1/0 version of Attrition)
  and `AgeGroup` (binned age ranges), used for analysis and Power BI.
- Saved the result as `data/employee_data_cleaned.csv`.

## Exploratory Analysis & Methodology
The analysis (`analysis/employee_analysis.py`) is a single script that
runs cleaning, EDA, attrition analysis, KPI calculation, and chart
generation end-to-end using Pandas, Matplotlib, and Seaborn. It groups
metrics by department and job role, compares employees who stayed vs.
left, and checks how overtime, job satisfaction, and work-life balance
relate to attrition. Relationships are described as correlations or
associations throughout — the script does not claim causation anywhere.

## KPIs
| KPI | Value |
|---|---|
| Total Employees | 1,470 |
| Employees with Attrition | 237 |
| Attrition Rate | 16.12% |
| Average Salary | $6,503 |
| Average Experience | 11.3 years |
| Average Performance Rating | 3.15 |
| Average Job Satisfaction | 2.73 / 4 |
| Average Work-Life Balance | 2.76 / 4 |
| Overtime Rate | 28.3% |

## Visualizations
13 charts are saved in `charts/`, including employee counts by department
and job role, salary and performance distributions, satisfaction by
department, and — the core of the analysis — attrition broken down by
department, job role, overtime, job satisfaction, and work-life balance,
plus a full correlation heatmap.

## Key Findings
- Overall attrition rate is **16.12%** (237 of 1,470 employees).
- **Sales** has the highest departmental attrition rate (20.63%),
  Research & Development the lowest (13.84%).
- **Sales Representative** has by far the highest attrition rate among
  job roles (39.76%); **Research Director** the lowest (2.5%).
- Employees who work overtime leave at **30.53%**, nearly three times the
  rate of those who don't (10.44%) — the single strongest pattern found.
- Attrition falls steadily as job satisfaction rises: 22.84% at the
  lowest satisfaction level down to 11.33% at the highest.
- Attrition falls steadily as work-life balance improves: 31.25% at the
  worst level down to 17.65% at the best.
- Employees who left earned less on average ($4,787/month) than those who
  stayed ($6,833/month).
- Salary correlates strongly with experience (r = 0.77) but only weakly
  with performance rating (r = -0.02) — pay in this dataset tracks tenure
  and job level far more than the annual performance score.

Full detail is in `reports/key_insights.txt`, `reports/department_summary.csv`,
and `reports/jobrole_summary.csv`.

## Business Recommendations
1. **Review overtime policy in Sales and Laboratory roles.** Overtime is
   the strongest attrition signal in the data; reducing mandatory
   overtime or compensating it better could directly lower turnover.
2. **Prioritize retention efforts on Sales Representatives.** This role's
   attrition rate (39.76%) is more than double the company average —
   investigate compensation, workload, and career path specifically for
   this group.
3. **Address low work-life balance and satisfaction as a pair.** Both
   independently correlate with attrition; an engagement or workload
   review for employees scoring 1-2 on either scale is likely to have the
   most impact.
4. **Re-examine junior-role compensation.** Roles with the highest
   attrition (Sales Representative, Laboratory Technician) also have the
   lowest average salaries — a pay-equity review for these levels is
   worth considering.
5. **Decouple performance reviews from pay conversations.** Since
   performance rating barely correlates with salary, employees may not
   see a clear link between performance and reward — worth checking
   whether this is intentional or a gap in the compensation model.

## Power BI Dashboard
A `.pbix` file could not be created in this text-only environment, so
`reports/powerbi_dashboard_guide.md` provides the cleaned data reference,
all required DAX measures, a 3-page layout (Overview / Attrition Analysis
/ Performance & Satisfaction), and recommended slicers — everything
needed to rebuild the dashboard directly in Power BI Desktop.

## Technologies Used
- Python 3 (Pandas, NumPy, Matplotlib, Seaborn)
- Power BI Desktop (dashboard, built from the guide provided)

## Project Structure
```
Task-4-Employee-Data-Analysis/
├── data/
│   ├── employee_data_original.csv
│   └── employee_data_cleaned.csv
├── analysis/
│   └── employee_analysis.py
├── charts/               (13 PNG charts)
├── reports/
│   ├── key_insights.txt
│   ├── summary.csv
│   ├── department_summary.csv
│   ├── jobrole_summary.csv
│   └── powerbi_dashboard_guide.md
└── README.md
```

## How to Run
```bash
cd analysis
pip install pandas numpy matplotlib seaborn
python employee_analysis.py
```
The script uses relative paths and creates all output folders
automatically — no manual column-name edits are needed.

## Limitations
- The dataset is a single, static snapshot — it shows association, not
  causation, and doesn't capture why individual employees actually left.
- Performance ratings only take two values (3 and 4) across the whole
  dataset, which limits how much can be said about performance as a
  driver of outcomes.
- No time-series data is available, so trends over time (e.g. attrition
  by year) could not be analyzed.

## Conclusion
Overtime, low job satisfaction, and poor work-life balance are the
clearest, most consistent signals associated with attrition in this
dataset, concentrated most heavily in the Sales department and the Sales
Representative role. These are concrete, actionable levers for HR and
management to target first.
