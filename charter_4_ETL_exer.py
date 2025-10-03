import pandas as pd
import numpy as np

# ------- Extract -------
df = pd.read_csv("sales_raw.csv")

# ------- Transform (Data Wrangling) -------
print("Original")
print(df)

# 1) Trim whitespace on common string columns
str_cols = ["customer_name", "state", "product", "coupon_code"]
for c in str_cols:
    df[c] = df[c].astype(str).str.strip()

# 2) Standardize state abbreviations
df["state"] = df["state"].str.upper()

# 3) Parse dates with mixed formats
for col in ["order_date", "ship_date"]:
    s = df[col].astype(str).str.strip()
    # normalize separators: '/' , '.' -> '-'
    s = s.str.replace(r"[./]", "-", regex=True)

    # Pass 1: parse easy cases
    dt = pd.to_datetime(s, errors="coerce")

    # Pass 2: ONLY rows like MM-DD-YYYY (e.g., 08-02-2025)
    mask_mdy = dt.isna() & s.str.match(r"^\d{2}-\d{2}-\d{4}$")
    dt.loc[mask_mdy] = pd.to_datetime(
        s[mask_mdy], format="%m-%d-%Y", errors="coerce"
    )

    df[col] = dt

# 4) Coerce qty & price to numeric
df["qty"] = pd.to_numeric(df["qty"], errors="coerce")
df["price_usd"] = pd.to_numeric(df["price_usd"], errors="coerce")

# 5) Drop exact duplicate rows
df = df.drop_duplicates()

# 6) Remove invalid rows (qty <= 0 or price <= 0) and rows missing qty/price
df = df[(df["qty"] > 0) & (df["price_usd"] > 0)]

# 7) Normalize customer names (title case)
df["customer_name"] = df["customer_name"].str.title()

# 8) Map coupon codes to discount percent
coupon_map = {"SUMMER10": 0.10, "SUMMER20": 0.20}
df["discount_pct"] = df["coupon_code"].map(coupon_map).fillna(0.0)

# 9) Derive revenue fields
df["gross_revenue"] = df["qty"] * df["price_usd"]
df["net_revenue"] = df["gross_revenue"] * (1 - df["discount_pct"])

print("\nCleaned")
print(df)

# -------- Load --------
# A) Save cleaned CSV
df.to_csv("sales_clean.csv", index=False)

print("Done. Wrote:")
print(" - sales_clean.csv")


