"""
Superstore Sales EDA Project
Run: python analysis.py
Requirements: pandas, numpy, matplotlib
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent
OUT = BASE / "outputs"
OUT.mkdir(exist_ok=True)

df = pd.read_csv(BASE / "superstore_sales.csv")
print("Original shape:", df.shape)
print("\nMissing values before cleaning:\n", df.isna().sum())

# Data cleaning
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
for col in ["Region", "Category", "Sub_Category"]:
    df[col] = df[col].fillna("Unknown")
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Profit"] = pd.to_numeric(df["Profit"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df = df.dropna(subset=["Order_Date", "Sales", "Profit", "Quantity"])
df = df.drop_duplicates(subset=["Order_ID"])
df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
df["Profit_Margin_Pct"] = (df["Profit"] / df["Sales"].replace(0, pd.NA) * 100).round(2)

clean_path = OUT / "cleaned_superstore_sales.csv"
df.to_csv(clean_path, index=False)
print("\nCleaned shape:", df.shape)
print("\nDescriptive statistics:\n", df[["Sales", "Quantity", "Discount", "Profit"]].describe().round(2))

# Summary tables
category_summary = df.groupby("Category", as_index=False).agg(
    Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"),
    Orders=("Order_ID", "count"), Avg_Discount=("Discount", "mean")
).sort_values("Total_Sales", ascending=False)
region_summary = df.groupby("Region", as_index=False).agg(
    Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"),
    Orders=("Order_ID", "count")
).sort_values("Total_Sales", ascending=False)
monthly = df.groupby("Month", as_index=False).agg(Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum"))
subcategory = df.groupby("Sub_Category", as_index=False).agg(
    Total_Sales=("Sales", "sum"), Total_Profit=("Profit", "sum")
).sort_values("Total_Profit")

category_summary.to_csv(OUT / "category_summary.csv", index=False)
region_summary.to_csv(OUT / "region_summary.csv", index=False)
monthly.to_csv(OUT / "monthly_summary.csv", index=False)
subcategory.to_csv(OUT / "subcategory_summary.csv", index=False)

# Visualizations
plt.figure(figsize=(8, 5))
plt.bar(category_summary["Category"], category_summary["Total_Sales"])
plt.title("Total Sales by Category")
plt.xlabel("Category"); plt.ylabel("Sales")
plt.xticks(rotation=15); plt.tight_layout()
plt.savefig(OUT / "sales_by_category.png", dpi=150); plt.close()

plt.figure(figsize=(8, 5))
plt.bar(region_summary["Region"], region_summary["Total_Profit"])
plt.title("Total Profit by Region")
plt.xlabel("Region"); plt.ylabel("Profit")
plt.tight_layout(); plt.savefig(OUT / "profit_by_region.png", dpi=150); plt.close()

plt.figure(figsize=(10, 5))
plt.plot(monthly["Month"], monthly["Total_Sales"], marker="o")
plt.title("Monthly Sales Trend")
plt.xlabel("Month"); plt.ylabel("Sales")
plt.xticks(rotation=75); plt.tight_layout()
plt.savefig(OUT / "monthly_sales_trend.png", dpi=150); plt.close()

plt.figure(figsize=(8, 5))
plt.bar(subcategory["Sub_Category"], subcategory["Total_Profit"])
plt.title("Profit by Sub-Category")
plt.xlabel("Sub-Category"); plt.ylabel("Profit")
plt.xticks(rotation=35); plt.tight_layout()
plt.savefig(OUT / "profit_by_subcategory.png", dpi=150); plt.close()

# Print five data-driven insights
total_sales = df["Sales"].sum()
total_profit = df["Profit"].sum()
best_category = category_summary.iloc[0]
best_region = region_summary.sort_values("Total_Profit", ascending=False).iloc[0]
worst_subcat = subcategory.iloc[0]
loss_orders = int((df["Profit"] < 0).sum())
high_discount_loss = int(((df["Discount"] >= 0.20) & (df["Profit"] < 0)).sum())

insights = f"""KEY BUSINESS FINDINGS
=====================
1. Total sales across the cleaned dataset: {total_sales:,.2f}.
2. Total profit across the cleaned dataset: {total_profit:,.2f}.
3. Highest-sales category: {best_category['Category']} ({best_category['Total_Sales']:,.2f} in sales).
4. Region with the highest total profit: {best_region['Region']} ({best_region['Total_Profit']:,.2f} profit).
5. {loss_orders} orders have negative profit; {high_discount_loss} of these orders have discounts of 20% or more.

RECOMMENDATIONS
---------------
- Review discount rules for orders with high discounts and negative profit.
- Compare both sales and profit before prioritizing a product category.
- Monitor monthly sales to plan stock and promotions.
- Investigate the lowest-profit sub-categories before increasing their inventory.
- Validate missing or unusual values before publishing business reports.
"""
(OUT / "business_insights.txt").write_text(insights, encoding="utf-8")
print("\n" + insights)
print(f"\nDone. Outputs saved in: {OUT}")
