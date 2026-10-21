# Superstore Sales Exploratory Data Analysis (EDA)

## Project overview
A beginner-friendly data analytics project using Python, Pandas, and Matplotlib to clean a retail sales dataset, explore sales and profit patterns, and present business insights.

## Files
- `superstore_sales.csv` — raw practice dataset (600 sample orders; includes a few missing values for cleaning practice).
- `analysis.py` — complete Python analysis script.
- `outputs/` — generated cleaned data, summary tables, charts, and findings after running the script.

## Tools
- Python 3.10+
- Pandas
- Matplotlib

## Setup and run
1. Install Python from the official Python website if it is not already installed.
2. Open this folder in VS Code.
3. Open the terminal in VS Code and run:

   ```bash
   python -m pip install pandas matplotlib
   python analysis.py
   ```

   On some Windows computers, use `py analysis.py` if `python analysis.py` does not work.

4. Open the `outputs` folder to view the charts, cleaned CSV, summary tables, and business findings.

## Analysis steps
1. Inspect dataset shape, column types, and missing values.
2. Convert dates and numeric columns to the correct types.
3. Fill missing category fields and remove rows missing essential numeric/date values.
4. Remove duplicate order IDs.
5. Analyze sales and profit by category, region, sub-category, and month.
6. Create charts and write business recommendations.

## Deliverables
- Cleaned CSV
- Category, region, monthly, and sub-category summary CSVs
- Four Matplotlib charts
- Five key business findings and recommendations

## Important note
This is a **practice dataset generated for learning** and is not official company or client data. Do not present its figures as real-world business results. You can replace the CSV with an approved dataset while keeping the same analysis workflow.
