# Power BI Dashboard Guide - Employee Attrition Analysis

A `.pbix` file cannot be created in this environment (Power BI Desktop is a
Windows-only application), so this guide gives everything needed to build
the dashboard in Power BI Desktop in a few minutes: the data to import, the
DAX measures, the layout, and the slicers.

## 1. Data to Import

Import `data/employee_data_cleaned.csv` into Power BI (Get Data > Text/CSV).
This is the cleaned version of the dataset — 1,470 rows, 34 columns, no
missing values or duplicates, with the three constant/non-informative
columns (`EmployeeCount`, `Over18`, `StandardHours`) removed and two
helper columns added (`AttritionFlag` = 1/0 version of Attrition,
`AgeGroup` = binned age ranges).

## 2. DAX Measures

Create these as new measures on the imported table (call it `Employees`).

```DAX
Total Employees = COUNTROWS(Employees)

Attrition Count = CALCULATE([Total Employees], Employees[Attrition] = "Yes")

Attrition Rate = DIVIDE([Attrition Count], [Total Employees], 0)

Average Salary = AVERAGE(Employees[MonthlyIncome])

Average Performance = AVERAGE(Employees[PerformanceRating])

Average Job Satisfaction = AVERAGE(Employees[JobSatisfaction])

Average Work-Life Balance = AVERAGE(Employees[WorkLifeBalance])

Average Experience (Years) = AVERAGE(Employees[TotalWorkingYears])

Overtime Rate =
DIVIDE(
    CALCULATE([Total Employees], Employees[OverTime] = "Yes"),
    [Total Employees], 0
)

Attrition Rate (Overtime) =
CALCULATE([Attrition Rate], Employees[OverTime] = "Yes")

Attrition Rate (No Overtime) =
CALCULATE([Attrition Rate], Employees[OverTime] = "No")
```

Format `Attrition Rate`, `Overtime Rate`, and the two overtime-split
measures as **Percentage** with 1-2 decimal places. Format salary measures
as **Currency**.

## 3. Recommended Dashboard Layout (3 pages)

### Page 1 - Overview
- KPI cards (top row): Total Employees, Attrition Rate, Average Salary,
  Average Performance, Average Job Satisfaction
- Bar chart: Employees by Department
- Bar chart: Employees by Job Role
- Column chart: Average Salary by Department
- Histogram/column: Total Working Years distribution

### Page 2 - Attrition Analysis
- KPI cards: Attrition Count, Attrition Rate
- Bar chart: Attrition Rate by Department
- Bar chart: Attrition Rate by Job Role
- Clustered column: Attrition Rate by Overtime (Yes/No)
- Clustered column: Attrition Rate by Job Satisfaction level (1-4)
- Clustered column: Attrition Rate by Work-Life Balance level (1-4)
- Matrix/heatmap: Work-Life Balance x Overtime x Attrition Rate

### Page 3 - Performance & Satisfaction
- Bar chart: Average Performance by Department
- Bar chart: Average Job Satisfaction by Department
- Scatter chart: MonthlyIncome (Y) vs TotalWorkingYears (X), colored by
  Attrition
- Scatter chart: PerformanceRating (Y) vs MonthlyIncome (X)

## 4. Slicers (add to every page, or a shared filter pane)

- Department
- JobRole
- Gender
- OverTime
- Attrition
- Education (numeric 1-5, or map to labels: Below College, College,
  Bachelor, Master, Doctor)
- AgeGroup
- MaritalStatus
- BusinessTravel

## 5. Design Notes

- Use a consistent HR/business palette: blue for neutral/overview metrics,
  red or orange for attrition-related metrics, so attrition risk visuals
  are visually distinct at a glance.
- Sort all "by category" bar charts descending by the metric shown (e.g.
  Attrition Rate by Job Role sorted highest to lowest) so the highest-risk
  groups are immediately visible.
- Add a text box on the Attrition Analysis page noting that the patterns
  shown are associations found in the data, not proven causes.
