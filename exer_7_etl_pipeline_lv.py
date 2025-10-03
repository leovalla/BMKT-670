#-------------------------------------------------------------------------------
# exer_7_etl_pipeline_lv.py
# This project implements an ETL pipeline for sales data
# Author: Leonardo Valladares
# Date: 2025-10-02
#------------------------------------------------------------------------------

# --------------------------------------
# Import necessary libraries and load data
# --------------------------------------
import pandas as pd
import numpy as np

df = pd.read_csv("sales_raw_large.csv")

# --------------------------------------
# Transform (Data Wrangling)
# --------------------------------------
print("Original")
print(df.head())

# 1) Trim whitespace on common string columns
str_cols = ["customer_name", "state", "product", "coupon_code"]
for c in str_cols:
    df[c] = df[c].astype(str).str.strip()

# 2. Clean up 'coupon_code'
df["coupon_code"] = (
    df["coupon_code"]
    .replace({"": np.nan, "nan": np.nan})  # Handle blanks and string "nan"
    .fillna("")                             # Replace NaN with empty string
)

# 3. Standardize state abbreviations
df["state"] = df["state"].str.upper()

# 4. Parse dates with mixed formats
for col in ["order_date", "ship_date"]:
    s = df[col].astype(str).str.strip()
    s = s.str.replace(r"[./]", "-", regex=True)  # Normalize separators

    # Pass 1: parse standard cases
    dt = pd.to_datetime(s, errors="coerce")

    # Pass 2: handle MM-DD-YYYY manually
    mask_mdy = dt.isna() & s.str.match(r"^\d{2}-\d{2}-\d{4}$")
    dt.loc[mask_mdy] = pd.to_datetime(s[mask_mdy], format="%m-%d-%Y", errors="coerce")

    df[col] = dt

# 5. Coerce numeric columns
df["qty"] = pd.to_numeric(df["qty"], errors="coerce")
df["price_usd"] = pd.to_numeric(df["price_usd"], errors="coerce")

# 6. Drop exact duplicates
df = df.drop_duplicates()

# 7. Remove rows with invalid/missing qty or price
df = df[(df["qty"] > 0) & (df["price_usd"] > 0)]

# 8. Normalize customer names
df["customer_name"] = df["customer_name"].str.title()

# 9. Map coupon codes to discount percentage
coupon_map = {"SUMMER10": 0.10, "SUMMER20": 0.20}
df["discount_pct"] = (
    df["coupon_code"].str.upper().map(coupon_map).fillna(0.0)
)

# 10. Calculate revenue fields
df["gross_revenue"] = df["qty"] * df["price_usd"]
df["net_revenue"] = df["gross_revenue"] * (1 - df["discount_pct"])

# --------------------------------------
# Output results (Load)
# --------------------------------------
print("\nCleaned:")
print(df)

df.to_csv("sales_clean.csv", index=False)
print("\nDone. Wrote:")
print(" - sales_clean.csv")