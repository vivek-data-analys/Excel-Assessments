# CORRECTED VERSION (my fixes are marked with  # FIX)
import pandas as pd
import numpy as np

df = pd.read_csv("SectionD_test_orders.csv")

# FIX 1: drop rows that are completely empty (they were counted/flagged as 'On Time')
df = df.dropna(how="all").copy()

# FIX 2: force numeric types so text/blank cells become NaN instead of breaking maths
df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")
df["DeliveryTime"] = pd.to_numeric(df["DeliveryTime"], errors="coerce")

# FIX 3: negative delivery time is a data-entry error -> treat as missing, keep a visible flag
df["DataQualityIssue"] = np.where(df["DeliveryTime"] < 0, "Negative DeliveryTime", "")
df.loc[df["DeliveryTime"] < 0, "DeliveryTime"] = np.nan

# FIX 4: NaN DeliveryTime must not be labelled 'On Time'
def flag(x):
    if pd.isna(x):
        return "Unknown"
    return "Delayed" if x > 60 else "On Time"
df["PerformanceFlag"] = df["DeliveryTime"].apply(flag)

# FIX 5: explicit aggregation - blanks ignored in sums/means, and count only orders that have a revenue value
summary = df.groupby("Cuisine").agg(
    Total_Revenue=("Revenue", lambda s: s.sum(min_count=1)),   # all-blank group -> NaN, not a fake 0
    Avg_DeliveryTime=("DeliveryTime", "mean"),                  # excludes the invalid -5
    Order_Count=("OrderID", "size"),
    Orders_Missing_Revenue=("Revenue", lambda s: s.isna().sum()),
).reset_index().round(2)

with pd.ExcelWriter("food_delivery_summary.xlsx") as writer:
    df.to_excel(writer, sheet_name="Orders", index=False)
    summary.to_excel(writer, sheet_name="Summary", index=False)

print(summary)
