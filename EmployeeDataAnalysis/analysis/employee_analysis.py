
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

for d in [DATA_DIR, CHARTS_DIR, REPORTS_DIR]:
    os.makedirs(d, exist_ok=True)

sns.set_style("whitegrid")
plt.rcParams["figure.dpi"] = 110
COLORS = {"stay": "#2E86AB", "leave": "#E63946", "accent": "#457B9D"}

RAW_PATH = os.path.join(DATA_DIR, "employee_data_original.csv")
CLEAN_PATH = os.path.join(DATA_DIR, "employee_data_cleaned.csv")

df_raw = pd.read_csv(RAW_PATH)
rows_before, cols_before = df_raw.shape

inspection_notes = []
inspection_notes.append(f"Rows: {rows_before}, Columns: {cols_before}")
inspection_notes.append(f"Missing values (total): {df_raw.isnull().sum().sum()}")
inspection_notes.append(f"Duplicate rows: {df_raw.duplicated().sum()}")


df = df_raw.copy()

str_cols = df.select_dtypes(include="object").columns
for c in str_cols:
    df[c] = df[c].astype(str).str.strip()

constant_cols = [c for c in ["EmployeeCount", "Over18", "StandardHours"] if df[c].nunique() == 1]
df = df.drop(columns=constant_cols)

id_col = "EmployeeNumber"

numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
invalid_value_notes = []
for c in numeric_cols:
    if (df[c] < 0).any():
        invalid_value_notes.append(f"{c} has negative values")


outlier_summary = {}
for c in ["MonthlyIncome", "TotalWorkingYears", "YearsAtCompany", "NumCompaniesWorked"]:
    q1, q3 = df[c].quantile(0.25), df[c].quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    n_outliers = ((df[c] < lower) | (df[c] > upper)).sum()
    outlier_summary[c] = n_outliers


if df.isnull().sum().sum() > 0:
    num_cols_missing = df[numeric_cols].columns[df[numeric_cols].isnull().any()]
    for c in num_cols_missing:
        df[c] = df[c].fillna(df[c].median())
    cat_cols_missing = df[str_cols].columns[df[str_cols].isnull().any()] if len(str_cols) else []
    for c in cat_cols_missing:
        df[c] = df[c].fillna(df[c].mode()[0])

dupes_removed = df.duplicated().sum()
df = df.drop_duplicates()

df["AttritionFlag"] = (df["Attrition"] == "Yes").astype(int)
df["AgeGroup"] = pd.cut(
    df["Age"], bins=[17, 25, 35, 45, 55, 65],
    labels=["18-25", "26-35", "36-45", "46-55", "56-60"]
)

rows_after, cols_after = df.shape

df.to_csv(CLEAN_PATH, index=False)


overview = {
    "Total Employees": len(df),
    "Departments": df["Department"].nunique(),
    "Job Roles": df["JobRole"].nunique(),
    "Average Age": round(df["Age"].mean(), 1),
    "Average Monthly Income ($)": round(df["MonthlyIncome"].mean(), 0),
    "Average Total Working Years": round(df["TotalWorkingYears"].mean(), 1),
    "Average Performance Rating": round(df["PerformanceRating"].mean(), 2),
    "Average Job Satisfaction (1-4)": round(df["JobSatisfaction"].mean(), 2),
    "Employees Who Left": int(df["AttritionFlag"].sum()),
    "Attrition Rate (%)": round(df["AttritionFlag"].mean() * 100, 2),
}


dept_summary = df.groupby("Department").agg(
    Employees=("EmployeeNumber", "count"),
    Avg_Salary=("MonthlyIncome", "mean"),
    Avg_Performance=("PerformanceRating", "mean"),
    Avg_Satisfaction=("JobSatisfaction", "mean"),
    Attrition_Rate=("AttritionFlag", "mean"),
).reset_index()
dept_summary["Attrition_Rate"] = (dept_summary["Attrition_Rate"] * 100).round(2)
dept_summary[["Avg_Salary", "Avg_Performance", "Avg_Satisfaction"]] = dept_summary[
    ["Avg_Salary", "Avg_Performance", "Avg_Satisfaction"]
].round(2)
dept_summary = dept_summary.sort_values("Attrition_Rate", ascending=False)

role_summary = df.groupby("JobRole").agg(
    Employees=("EmployeeNumber", "count"),
    Avg_Salary=("MonthlyIncome", "mean"),
    Avg_Performance=("PerformanceRating", "mean"),
    Avg_Satisfaction=("JobSatisfaction", "mean"),
    Attrition_Rate=("AttritionFlag", "mean"),
).reset_index()
role_summary["Attrition_Rate"] = (role_summary["Attrition_Rate"] * 100).round(2)
role_summary[["Avg_Salary", "Avg_Performance", "Avg_Satisfaction"]] = role_summary[
    ["Avg_Salary", "Avg_Performance", "Avg_Satisfaction"]
].round(2)
role_summary = role_summary.sort_values("Attrition_Rate", ascending=False)


salary_experience_corr = df["MonthlyIncome"].corr(df["TotalWorkingYears"])
salary_performance_corr = df["MonthlyIncome"].corr(df["PerformanceRating"])
experience_performance_corr = df["TotalWorkingYears"].corr(df["PerformanceRating"])
experience_satisfaction_corr = df["TotalWorkingYears"].corr(df["JobSatisfaction"])


performance_vs_attrition = df.groupby("Attrition")["PerformanceRating"].mean().round(2)


satisfaction_cols = ["JobSatisfaction", "EnvironmentSatisfaction", "RelationshipSatisfaction", "WorkLifeBalance"]
satisfaction_by_attrition = df.groupby("Attrition")[satisfaction_cols].mean().round(2)


compare_cols = ["MonthlyIncome", "TotalWorkingYears", "PerformanceRating",
                 "JobSatisfaction", "WorkLifeBalance", "YearsAtCompany", "DistanceFromHome"]
stay_vs_leave = df.groupby("Attrition")[compare_cols].mean().round(2)

overtime_attrition = pd.crosstab(df["OverTime"], df["Attrition"], normalize="index").round(4) * 100
jobsat_attrition = pd.crosstab(df["JobSatisfaction"], df["Attrition"], normalize="index").round(4) * 100
wlb_attrition = pd.crosstab(df["WorkLifeBalance"], df["Attrition"], normalize="index").round(4) * 100



def save_fig(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(CHARTS_DIR, name), bbox_inches="tight")
    plt.close(fig)

fig, ax = plt.subplots(figsize=(7, 5))
order = df["Department"].value_counts().index
sns.countplot(data=df, y="Department", order=order, color=COLORS["accent"], ax=ax)
ax.set_title("Employees by Department")
ax.set_xlabel("Number of Employees")
save_fig(fig, "employees_by_department.png")

fig, ax = plt.subplots(figsize=(8, 6))
order = df["JobRole"].value_counts().index
sns.countplot(data=df, y="JobRole", order=order, color=COLORS["accent"], ax=ax)
ax.set_title("Employees by Job Role")
ax.set_xlabel("Number of Employees")
save_fig(fig, "employees_by_job_role.png")

fig, ax = plt.subplots(figsize=(7, 5))
sns.barplot(data=dept_summary.sort_values("Avg_Salary", ascending=False),
            x="Avg_Salary", y="Department", color=COLORS["stay"], ax=ax)
ax.set_title("Average Monthly Salary by Department")
ax.set_xlabel("Average Monthly Income ($)")
save_fig(fig, "salary_by_department.png")

fig, ax = plt.subplots(figsize=(7, 5))
sns.scatterplot(data=df, x="TotalWorkingYears", y="MonthlyIncome",
                 hue="Attrition", palette={"Yes": COLORS["leave"], "No": COLORS["stay"]},
                 alpha=0.6, ax=ax)
ax.set_title("Salary vs. Total Working Years")
ax.set_xlabel("Total Working Years")
ax.set_ylabel("Monthly Income ($)")
save_fig(fig, "salary_vs_experience.png")

fig, ax = plt.subplots(figsize=(6, 5))
sns.countplot(data=df, x="PerformanceRating", color=COLORS["accent"], ax=ax)
ax.set_title("Performance Rating Distribution")
ax.set_xlabel("Performance Rating (3=Excellent, 4=Outstanding)")
save_fig(fig, "performance_distribution.png")

fig, ax = plt.subplots(figsize=(7, 5))
sat_by_dept = df.groupby("Department")["JobSatisfaction"].mean().sort_values()
sns.barplot(x=sat_by_dept.values, y=sat_by_dept.index, color=COLORS["stay"], ax=ax)
ax.set_title("Average Job Satisfaction by Department")
ax.set_xlabel("Average Job Satisfaction (1-4)")
save_fig(fig, "satisfaction_by_department.png")

fig, ax = plt.subplots(figsize=(7, 5))
sns.barplot(data=dept_summary.sort_values("Attrition_Rate", ascending=False),
            x="Attrition_Rate", y="Department", color=COLORS["leave"], ax=ax)
ax.set_title("Attrition Rate by Department")
ax.set_xlabel("Attrition Rate (%)")
save_fig(fig, "attrition_by_department.png")

fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=role_summary.sort_values("Attrition_Rate", ascending=False),
            x="Attrition_Rate", y="JobRole", color=COLORS["leave"], ax=ax)
ax.set_title("Attrition Rate by Job Role")
ax.set_xlabel("Attrition Rate (%)")
save_fig(fig, "attrition_by_job_role.png")

fig, ax = plt.subplots(figsize=(6, 5))
overtime_pct = df.groupby("OverTime")["AttritionFlag"].mean().mul(100).round(2)
sns.barplot(x=overtime_pct.index, y=overtime_pct.values, color=COLORS["leave"], ax=ax)
ax.set_title("Attrition Rate by Overtime Status")
ax.set_ylabel("Attrition Rate (%)")
ax.set_xlabel("Overtime")
save_fig(fig, "attrition_vs_overtime.png")

fig, ax = plt.subplots(figsize=(6, 5))
jobsat_pct = df.groupby("JobSatisfaction")["AttritionFlag"].mean().mul(100).round(2)
sns.barplot(x=jobsat_pct.index, y=jobsat_pct.values, color=COLORS["leave"], ax=ax)
ax.set_title("Attrition Rate by Job Satisfaction Level")
ax.set_ylabel("Attrition Rate (%)")
ax.set_xlabel("Job Satisfaction (1=Low, 4=Very High)")
save_fig(fig, "attrition_vs_satisfaction.png")

fig, ax = plt.subplots(figsize=(6, 5))
wlb_pct = df.groupby("WorkLifeBalance")["AttritionFlag"].mean().mul(100).round(2)
sns.barplot(x=wlb_pct.index, y=wlb_pct.values, color=COLORS["leave"], ax=ax)
ax.set_title("Attrition Rate by Work-Life Balance Level")
ax.set_ylabel("Attrition Rate (%)")
ax.set_xlabel("Work-Life Balance (1=Bad, 4=Best)")
save_fig(fig, "attrition_vs_worklife_balance.png")

fig, ax = plt.subplots(figsize=(12, 10))
corr_cols = ["Age", "DailyRate", "DistanceFromHome", "Education", "EnvironmentSatisfaction",
             "HourlyRate", "JobInvolvement", "JobLevel", "JobSatisfaction", "MonthlyIncome",
             "MonthlyRate", "NumCompaniesWorked", "PercentSalaryHike", "PerformanceRating",
             "RelationshipSatisfaction", "StockOptionLevel", "TotalWorkingYears",
             "TrainingTimesLastYear", "WorkLifeBalance", "YearsAtCompany", "YearsInCurrentRole",
             "YearsSinceLastPromotion", "YearsWithCurrManager", "AttritionFlag"]
corr_matrix = df[corr_cols].corr()
sns.heatmap(corr_matrix, cmap="coolwarm", center=0, ax=ax, annot=False, linewidths=0.3)
ax.set_title("Correlation Heatmap - Numeric HR Variables")
save_fig(fig, "correlation_heatmap.png")

fig, ax = plt.subplots(figsize=(8, 5))
grp = df.groupby(["WorkLifeBalance", "OverTime"])["AttritionFlag"].mean().mul(100).round(2).reset_index()
sns.barplot(data=grp, x="WorkLifeBalance", y="AttritionFlag", hue="OverTime",
            palette={"Yes": COLORS["leave"], "No": COLORS["stay"]}, ax=ax)
ax.set_title("Attrition Rate by Work-Life Balance and Overtime")
ax.set_ylabel("Attrition Rate (%)")
ax.set_xlabel("Work-Life Balance (1=Bad, 4=Best)")
save_fig(fig, "attrition_worklife_overtime_combo.png")


kpis = {
    "Total Employees": len(df),
    "Employees with Attrition": int(df["AttritionFlag"].sum()),
    "Attrition Rate (%)": round(df["AttritionFlag"].mean() * 100, 2),
    "Average Salary ($)": round(df["MonthlyIncome"].mean(), 0),
    "Average Experience (Years)": round(df["TotalWorkingYears"].mean(), 1),
    "Average Performance Rating": round(df["PerformanceRating"].mean(), 2),
    "Average Job Satisfaction": round(df["JobSatisfaction"].mean(), 2),
    "Average Work-Life Balance": round(df["WorkLifeBalance"].mean(), 2),
    "Overtime Rate (%)": round((df["OverTime"] == "Yes").mean() * 100, 2),
}

dept_summary.to_csv(os.path.join(REPORTS_DIR, "department_summary.csv"), index=False)
role_summary.to_csv(os.path.join(REPORTS_DIR, "jobrole_summary.csv"), index=False)

summary_rows = []
for k, v in kpis.items():
    summary_rows.append({"Metric": k, "Value": v})
pd.DataFrame(summary_rows).to_csv(os.path.join(REPORTS_DIR, "summary.csv"), index=False)

top_dept = dept_summary.iloc[0]
top_role = role_summary.iloc[0]
lowest_role = role_summary.iloc[-1]

insights_lines = []
insights_lines.append("KEY BUSINESS INSIGHTS - Employee Attrition Analysis")
insights_lines.append("=" * 55)
insights_lines.append("")
insights_lines.append(f"1. Overall attrition rate is {kpis['Attrition Rate (%)']}% "
                       f"({kpis['Employees with Attrition']} of {kpis['Total Employees']} employees).")
insights_lines.append(f"2. '{top_dept['Department']}' has the highest departmental attrition rate "
                       f"at {top_dept['Attrition_Rate']}%, versus "
                       f"{dept_summary.iloc[-1]['Attrition_Rate']}% in '{dept_summary.iloc[-1]['Department']}'.")
insights_lines.append(f"3. '{top_role['JobRole']}' has the highest attrition rate among job roles "
                       f"at {top_role['Attrition_Rate']}%, while '{lowest_role['JobRole']}' has the "
                       f"lowest at {lowest_role['Attrition_Rate']}%.")
insights_lines.append(f"4. Employees who work overtime leave at {overtime_attrition.loc['Yes', 'Yes']:.2f}% "
                       f"versus {overtime_attrition.loc['No', 'Yes']:.2f}% for those who do not work overtime - "
                       f"overtime is strongly associated with higher attrition (this is an association, not "
                       f"a proven cause).")
insights_lines.append(f"5. Employees with the lowest job satisfaction (level 1) leave at "
                       f"{jobsat_attrition.loc[1, 'Yes']:.2f}%, compared to "
                       f"{jobsat_attrition.loc[4, 'Yes']:.2f}% for those with the highest satisfaction (level 4).")
insights_lines.append(f"6. Employees with the worst work-life balance (level 1) leave at "
                       f"{wlb_attrition.loc[1, 'Yes']:.2f}%, versus "
                       f"{wlb_attrition.loc[4, 'Yes']:.2f}% for those with the best work-life balance (level 4).")
insights_lines.append(f"7. Employees who left the company had, on average, "
                       f"${stay_vs_leave.loc['Yes', 'MonthlyIncome']:,.0f} monthly income versus "
                       f"${stay_vs_leave.loc['No', 'MonthlyIncome']:,.0f} for those who stayed - "
                       f"lower pay is associated with higher turnover.")
insights_lines.append(f"8. Salary and total working years show a correlation of {salary_experience_corr:.2f}, "
                       f"indicating salary tends to rise with career experience, as expected; "
                       f"performance rating shows a weak correlation with salary "
                       f"({salary_performance_corr:.2f}), suggesting pay is driven more by tenure/level "
                       f"than by the annual performance score in this dataset.")
insights_lines.append("")
insights_lines.append("Note: All relationships above describe correlation/association found in this "
                       "dataset, not proven causation.")

with open(os.path.join(REPORTS_DIR, "key_insights.txt"), "w") as f:
    f.write("\n".join(insights_lines))

print("Analysis complete.")
print(f"Rows before: {rows_before}, after: {rows_after}")
print(f"Columns before: {cols_before}, after: {cols_after}")
print(f"Constant columns dropped: {constant_cols}")
print(f"Duplicate rows removed: {dupes_removed}")
print(f"Outlier counts (IQR method, not removed): {outlier_summary}")
print("KPIs:", kpis)
