# Sales Data Analysis — Wide World Importers Sales Fact Data

Data cleaning, validation and business analytics project built from a single source file, `FactSale.csv`
(a sales fact table covering 2013-01-01 to 2016-05-31, 26,397 order lines / 8,188 orders).

## Contents

```
Sales_Analysis/
├── data/
│   └── cleaned_sales_data.csv        Cleaned, validated dataset with added time features
│                                      and a derived Product Category column
├── dashboard/
│   └── dashboard.html                Self-contained interactive dashboard (open in any browser,
│                                      no server needed). Filter by Year / Category / Package.
├── reports/
│   └── Sales_Analysis_Report.docx    Full write-up: dataset overview, cleaning & validation
│                                      summary, data quality report, business analysis,
│                                      key insights, recommendations, executive summary
└── README.md
```

## Key numbers

- Total sales: $19,879,593 · Total profit: $9,923,892 · Overall margin: 49.9%
- 8,188 orders across 26,397 order lines, Jan 2013 – May 2016 (2016 is a partial year)
- Core category: Packaging & Shipping Supplies (58% of revenue, 51.7% margin)
- Data-quality flag: the Halloween zombie mask product sold at a loss on 100% of its
  492 transactions (−$33,060 total) — see the report for full detail

## Notes on scope

The source file has no linked dimension tables, so City Key, Customer Key and Salesperson Key
are analyzed as anonymous numeric identifiers only (no names/regions were available). Product
Category is a field derived from the product Description text for this analysis — it is not a
column present in the original data — and is documented as such in the report.

Open `dashboard/dashboard.html` directly in a browser to explore the data interactively.
