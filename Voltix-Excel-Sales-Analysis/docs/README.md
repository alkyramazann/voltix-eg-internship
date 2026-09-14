# Excel Sales Analysis & Reporting

## Overview
This project is a practical Excel-based sales analysis completed as part of a
Voltix-EG Data Analyst internship task. It works with a car sales dataset (30
orders, 6 sales agents, 6 car types) and focuses on applying core Excel
skills: professional formatting, conditional formatting, formulas, lookup
functions, sales analysis by person, and invoice creation. The goal was to
practice real Data Analyst tasks rather than build a data science model —
everything here is done with native Excel formulas and formatting.

## Tasks Completed

### Task 1 — Formatting
The raw sales report (Order Date, Sales Agent Name, Car Type, Car Price,
Count, Total Sales) was formatted for readability: dates use a `d-mmm`
format, prices use an EGP currency format, a bordered table with a dark
header row was applied, and inconsistent fonts/alignment in the original
data were cleaned up.

### Task 2 — Conditional Formatting
Conditional formatting rules were added to the Total Sales column to
automatically highlight the highest order amount in green and the lowest in
red, so they update if the underlying data changes.

### Task 3 — Conditional Formatting + MAX/MIN
A "Sales Report per Thousand" table compares each sales person's monthly
results against a target value in cell J3 (1000). Conditional formatting
highlights results above the target in green and below it in red. `MIN()`
and `MAX()` formulas calculate the lowest and highest results across the
whole table.

### Task 4 — Formulas
Four summary formulas were added: `SUM()` for Total Sales Amount, `SUM()`
for Total Sold Cars, `COUNT()` for Count of Orders, and `AVERAGE()` for
Average Order Amount — all referencing the order table directly.

### Task 5 — Sales Analysis
A per-salesperson summary table was built using `SUMIF()` to total sales for
each of the 6 sales agents, and `INDEX()`/`MATCH()` to automatically pull out
the best-performing sales person by total sales amount.

### Task 6 — Lookup / Calculations
`INDEX()`/`MATCH()` formulas look up each order's car price from a car-type
price table, and a simple multiplication formula calculates the full order
amount (Price × Count) for every order.

### Task 7 — Invoice / Bill
A sample bill was created listing car type, unit price (via lookup),
quantity, and line total for each item, with `SUM()` formulas totalling the
quantity and amount at the bottom.

## Key Results
| Metric | Value |
|---|---|
| Highest Order Amount (Total Sales) | EGP 2,370,000 |
| Lowest Order Amount (Total Sales) | EGP 375,000 |
| Highest Result (Task 3 table) | 6,831.00 |
| Lowest Result (Task 3 table) | 189.84 |
| Total Sales Amount | EGP 29,365,000 |
| Total Sold Cars | 50 |
| Count of Orders | 30 |
| Average Order Amount | EGP 978,833 |
| Best Sales Person | Ahmed (EGP 6,940,000 total sales) |

**Total sales by sales person:**
| Sales Person | Total Sales |
|---|---|
| Ahmed | EGP 6,940,000 |
| Hossam | EGP 6,770,000 |
| Abdullah | EGP 4,720,000 |
| Farida | EGP 5,425,000 |
| Mona | EGP 3,280,000 |
| Ali | EGP 2,230,000 |

*Note: the Task 1 sheet's own Total Sales column sums to EGP 28,615,000
because two rows on that sheet (24-May and 27-May) carry a Count of 1
instead of 2, while the same two orders show Count = 2 on every other
sheet. The figures above use the consistent value (Count = 2) found across
Tasks 2, 4, 5 and 6.*

## Excel Skills Demonstrated
- Data formatting (dates, currency, fonts, borders, table structure)
- Conditional formatting (formula-based highlighting)
- Excel formulas: `SUM`, `COUNT`, `AVERAGE`, `MIN`, `MAX`, `SUMIF`
- Lookup functions: `INDEX` / `MATCH`
- Sales analysis and data summarization by category
- Invoice/bill creation with linked lookups and totals
- Professional spreadsheet design

## Files
```
Voltix-Excel-Sales-Analysis/
├── workbook/
│   └── Excel_Sales_Analysis.xlsx   — the completed workbook (7 task sheets)
├── docs/
│   └── README.md                   — this file
```
- **Excel_Sales_Analysis.xlsx**: the single workbook containing all 7 tasks,
  each on its own sheet (Task 1–Task 7), with live formulas and conditional
  formatting rules — not hardcoded values.

## Conclusion
This project covers the core practical skills expected of a junior Data
Analyst working in Excel: cleaning and formatting raw data, using
conditional formatting to surface outliers, building summary formulas,
doing lookups across tables, and presenting results (salesperson report,
invoice) in a way a non-technical manager could read directly.
