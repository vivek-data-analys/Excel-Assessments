"""
YourName_M3-A1  |  Section B - Task 4 (Python part)
Delivery Performance EDA: descriptive statistics, IQR outliers, correlation matrix.
Input : SectionB_Task4_delivery_data.csv  (CSV export of the tblDelivery Excel table)
"""
import pandas as pd

df = pd.read_csv("SectionB_Task4_delivery_data.csv")

# ---------------- 1. Descriptive statistics (.describe) ----------------
print("=" * 60)
print("DESCRIPTIVE STATISTICS - DeliveryTime (minutes)")
print("=" * 60)
dt_ = df["DeliveryTime"]
print(dt_.describe().round(2))
print(f"Median   : {dt_.median():.2f}")
print(f"Mode     : {dt_.mode().iloc[0]}")
print(f"Variance : {dt_.var():.2f}   (sample, ddof=1 -> same as Excel VAR.S)")
print(f"Std Dev  : {dt_.std():.2f}   (sample, ddof=1 -> same as Excel STDEV.S)")

# ---------------- 2. Manual IQR outlier detection ----------------
# Excel QUARTILE.INC uses linear interpolation = pandas default quantile method
q1 = dt_.quantile(0.25)
q3 = dt_.quantile(0.75)
iqr = q3 - q1
lower = q1 - 1.5 * iqr
upper = q3 + 1.5 * iqr
outliers = df[(dt_ < lower) | (dt_ > upper)]
print("\n" + "=" * 60)
print("IQR OUTLIER DETECTION")
print("=" * 60)
print(f"Q1 = {q1:.2f} | Q3 = {q3:.2f} | IQR = {iqr:.2f}")
print(f"Lower bound = {lower:.2f} | Upper bound = {upper:.2f}")
print(f"Outliers found: {len(outliers)}")
print(outliers[["OrderID", "DeliveryTime"]].to_string(index=False))

# ---------------- 3. Correlation matrix ----------------
corr = df[["Revenue", "DeliveryTime", "Rating"]].corr()
print("\n" + "=" * 60)
print("CORRELATION MATRIX (Pearson)")
print("=" * 60)
print(corr.round(3))

# INTERPRETATION (business meaning of each coefficient)
# DeliveryTime vs Rating  : strong NEGATIVE correlation -> the slower the delivery, the lower
#   the customer rating. Operations should treat delivery speed as the #1 driver of satisfaction
#   and target the slow zones/riders first.
# DeliveryTime vs Revenue : weak POSITIVE (about +0.2) -> bigger orders tend to take slightly longer to
#   prepare/deliver; speed alone will not raise basket size, but large orders need extra prep-time planning.
# Revenue vs Rating       : weak -> big orders are not automatically happier customers, so revenue
#   alone is a poor proxy for satisfaction - monitor Rating separately.
# Note: correlation is not causation; outliers (very long times) can inflate |r|, so re-check without them.
r_dt = corr.loc["DeliveryTime", "Rating"]
print(f"\nDeliveryTime vs Rating r = {r_dt:.3f} -> "
      f"{'longer deliveries are linked to lower ratings' if r_dt < 0 else 'no negative link found'}")
