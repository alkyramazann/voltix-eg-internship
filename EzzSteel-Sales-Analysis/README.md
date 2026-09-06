# EzzSteel Sales Analysis

##  Project Overview

This project analyzes **EzzSteel sales data** to identify sales trends, product performance, regional patterns, and other business insights.

The analysis was conducted as part of my internship work at **Voltix-EG**, using Python and common data analysis and visualization libraries.

##  Objectives

The main objectives of this project are to:

* Clean and prepare the sales dataset
* Explore the structure and characteristics of the data
* Analyze sales performance
* Identify top-performing products
* Compare sales across different regions or categories
* Discover trends and patterns in the dataset
* Create clear and informative visualizations
* Extract actionable business insights

## Dataset

The project uses an Excel dataset containing EzzSteel sales information.

The dataset includes sales-related variables that can be used to analyze:

* Orders
* Products
* Categories
* Regions
* Quantities
* Sales values
* Dates

The original dataset is included in the project folder as:

`EzzSteel_Full_Dataset.xlsx`

##  Analysis

The notebook covers several stages of the analysis:

### 1. Data Loading

The dataset is imported from an Excel file using Pandas.

### 2. Data Cleaning

The data is checked for:

* Missing values
* Duplicate records
* Incorrect data types
* Inconsistent values

### 3. Exploratory Data Analysis

Different aspects of the sales data are explored to understand overall business performance.

### 4. Data Visualization

Charts are created using Matplotlib and Seaborn to make trends and comparisons easier to understand.

### 5. Business Insights

The analysis identifies important patterns in sales performance and highlights areas that can support business decision-making.

##  Data Cleaning

Several data quality issues were identified and handled during the preprocessing stage:

* **8 exact duplicate records** were identified and removed.
* `Revenue_EGP` was stored as text values such as `"20099100 EGP"` and converted into a numeric format.
* **Mixed date formats** (ISO and DD/MM/YYYY) were standardized.
* A **kg-vs-ton unit mix-up** was identified in `Quantity_Tons`, where some values were 100–1000× larger than expected, and corrected.
* **Negative quantities** were identified and handled.
* **Invalid discounts** above 100% were detected and corrected.
* Inconsistent category names were standardized, including:

  * `contractor` → `Contractor`
  * `long steel rebar` → `Long Steel`

These cleaning steps were important for ensuring that the subsequent analysis and visualizations were based on reliable data.

##  Key Findings

The cleaned dataset contains **2,378 invoices** covering the period from **2020 to 2023**, with approximately **49.5 billion EGP in total sales**.

### Main insights

* **Long Steel** was the leading category, accounting for approximately **61% of total revenue**.
* **Egypt (domestic)** was by far the largest market, generating approximately **15× the sales of the next-largest export market**.
* **B500C** was the best-selling steel grade by revenue.
* Annual sales increased by approximately **195% between 2020 and 2023**, meaning sales nearly tripled over the four-year period.
* The sales-over-time analysis revealed a clear **multi-year growth trend** rather than a single-year fluctuation.

##  Results

The analysis demonstrates a strong overall growth trajectory in EzzSteel's sales between 2020 and 2023.

The combination of category, market, product, and time-based analysis provides a broader view of sales performance and highlights the importance of **Long Steel, the domestic Egyptian market, and B500C** in overall revenue generation.

##  Business Insights

Based on the analysis:

1. **Long Steel represents the core revenue segment**, making it an important category for maintaining overall sales performance.
2. The strong dominance of the **Egyptian domestic market** suggests that domestic demand is a major driver of revenue.
3. **B500C's strong revenue performance** indicates its importance within the product portfolio.
4. The significant growth from **2020 to 2023** indicates a strong positive sales trajectory during the analyzed period.
5. Maintaining data quality is essential because issues such as incorrect units, invalid discounts, and inconsistent categories can significantly distort business analysis.


##  Technologies Used

| Technology       | Purpose                   |
| ---------------- | ------------------------- |
| Python           | Data analysis             |
| Pandas           | Data manipulation         |
| NumPy            | Numerical operations      |
| Matplotlib       | Data visualization        |
| Seaborn          | Statistical visualization |
| Jupyter Notebook | Analysis environment      |
| Microsoft Excel  | Dataset format            |

##  How to Run

### 1. Clone the repository

```bash
git clone https://github.com/alkyramazann/voltix-eg.git
cd voltix-eg
```

### 2. Install the required libraries

```bash
pip install pandas numpy matplotlib seaborn openpyxl jupyter
```

### 3. Open the notebook

```bash
jupyter notebook
```

Then open:

`EzzSteel_Sales_Analysis.ipynb`

##  Project Structure

```text
EzzSteel-Sales-Analysis/
│
├── README.md
├── EzzSteel_Sales_Analysis.ipynb
└── EzzSteel_Full_Dataset.xlsx
```

## 📈
The analysis provides an overview of EzzSteel's sales performance and demonstrates how data analysis and visualization can be used to transform raw sales data into meaningful business insights.

##  Author

**Ramazan Allahverdizada**

GitHub: [alkyramazann](https://github.com/alkyramazann)
