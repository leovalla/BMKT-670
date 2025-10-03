#-------------------------------------------------------------------------------
# project_5_stock_data_lv.py
# This project downloads and visualizes stock data for selected companies
# Author: Leonardo Valladares
# Date: 2025-10-03
#------------------------------------------------------------------------------

# --------------------------------------
# Import necessary libraries and load data
# --------------------------------------
import yfinance as yf
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


# Download data 
# NVDA = Nvidia, UNH = UnitedHealth, HD = Home Depot
tickers = ["NVDA", "UNH", "HD"]
raw = yf.download(tickers, period="5y", interval="1d")
close = raw["Close"]    # DataFrame: columns NVDA, UNH, HD
volume = raw["Volume"]  # DataFrame: columns NVDA, UNH, HD

# scale volume to millions
volume = volume / 1e6           # values now in millions (float)
volume = volume.round(3)      

# Rename columns to friendly names
close = close.rename(columns={"NVDA": "Nvidia", "UNH": "UnitedHealth", "HD": "Home_Depot"})
volume = volume.rename(columns={"NVDA": "Nvidia", "UNH": "UnitedHealth", "HD": "Home_Depot"})

# combine close and volume into one DataFrame and save to CSV
close.columns = [c + "_Close" for c in close.columns]
volume.columns = [c + "_Volume" for c in volume.columns]
data = pd.concat([close, volume], axis=1).sort_index(axis=1)

# Display data info
print("\nInitial data info:")
print(data.head())
print("Data frame Shape:", data.shape)

# Check for missing values
rows_with_missing = data[data.isnull().any(axis=1)]

if rows_with_missing.empty:
    print("\nNo missing values in the data set")
else:
    print("\nNumber of rows with missing values:", len(rows_with_missing))
    # remove missing values
    data = data.dropna()
    print("\nAfter dropping missing values, new shape:", data.shape)


# Display final data info
print("\nFinal data info:")
print(data.head())
print("Data frame Shape:", data.shape)

# --------------------------------------
# writes CSV with dates formatted as MM-DD-YYYY, preserves index (the dates)
'''
data.to_csv("stock_close_and_volume.csv", date_format="%m-%d-%Y", float_format="%.4f", index=True)
print("\nDone. Wrote:")
print(" - stock_data.csv")
'''

# --------------------------------------
# plot closing prices
'''
fig, ax = plt.subplots(nrows=3, ncols=1)
ax[0].plot(data.Nvidia_Close)
ax[0].set_title("Nvidia Closing Prices")
ax[0].set_xlabel("Date")
ax[0].set_ylabel("Price (USD)")
ax[0].ticklabel_format(axis='y', style='plain')
ax[1].plot(data.UnitedHealth_Close)
ax[1].set_title("UnitedHealth Closing Prices")
ax[1].set_xlabel("Date")
ax[1].set_ylabel("Price (USD)")
ax[1].ticklabel_format(axis='y', style='plain')
ax[2].plot(data.Home_Depot_Close)
ax[2].set_title("Home Depot Closing Prices")
ax[2].set_xlabel("Date")
ax[2].set_ylabel("Price (USD)")
ax[2].ticklabel_format(axis='y', style='plain')
fig.tight_layout()

plt.show()
'''

# --------------------------------------
# plot trading volumes
'''
fig, ax = plt.subplots(nrows=3, ncols=1)
ax[0].plot(data.Nvidia_Volume)
ax[0].set_title("Nvidia Trading Volume")
ax[0].set_xlabel("Date")
ax[0].set_ylabel("Volume (Millions)")

ax[0].ticklabel_format(axis='y', style='plain')
ax[1].plot(data.UnitedHealth_Volume)
ax[1].set_title("UnitedHealth Trading Volume")
ax[1].set_xlabel("Date")
ax[1].set_ylabel("Volume (Millions)")
ax[1].ticklabel_format(axis='y', style='plain')
ax[2].plot(data.Home_Depot_Volume)
ax[2].set_title("Home Depot Trading Volume")
ax[2].set_xlabel("Date")
ax[2].set_ylabel("Volume (Millions)")
ax[2].ticklabel_format(axis='y', style='plain')
fig.tight_layout()

plt.show()  
'''

# --------------------------------------
# Plot percentage growth of each ticker with brand colors
# --------------------------------------
'''
# Normalize close prices to start at 100
normalized_close = close / close.iloc[0] * 100

# Define brand colors for each stock
color_map = {
    "Nvidia_Close": "green",          # Nvidia → green
    "Home_Depot_Close": "orange",     # Home Depot → orange
    "UnitedHealth_Close": "blue"      # UnitedHealth → blue
}

# Create the plot
plt.figure(figsize=(12, 6))
for col in normalized_close.columns:
    label = col.replace("_Close", "")
    plt.plot(normalized_close.index, normalized_close[col],
             label=label,
             color=color_map.get(col, "gray"))  # fallback to gray if not found

# Format y-axis as percent from baseline
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0, xmax=100))

# Add labels and styling
plt.title("Percentage Growth of Stock Prices Over 5 Years", fontsize=14)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Growth Since Start (%)", fontsize=12)
plt.legend()
# plt.grid(True)
plt.tight_layout()
plt.show()
'''

# --------------------------------------
# Compute performance metrics for each stock
# --------------------------------------

# 1. Calculate daily returns
daily_returns = close.pct_change().dropna()

# 2. Resample to monthly and compute monthly returns (last day price of each month)
monthly_close = close.resample('ME').last()
monthly_returns = monthly_close.pct_change().dropna()

# 3. Create an empty summary table
summary = pd.DataFrame(index=close.columns)  # index = Nvidia_Close etc.

# 4. Compute metrics
summary["Cumulative_Return (%)"] = ((close.iloc[-1] / close.iloc[0]) - 1) * 100
summary["Annualized_Volatility (%)"] = daily_returns.std() * (252**0.5) * 100
summary["Average_Monthly_Return (%)"] = monthly_returns.mean() * 100
summary["Max_Daily_Loss (%)"] = daily_returns.min() * 100
summary["Sharpe_Ratio"] = daily_returns.mean() / daily_returns.std() * (252**0.5)

# 5. Clean column names
summary.index.name = "Ticker"
summary = summary.round(2)

# Display comparison table
# print("\nPerformance Summary (5-Year Period):")
# print(summary)

# --------------------------------------
# Save summary table 
# --------------------------------------
def plot_df_table(df, title="Performance Summary", filename="summary_table.png"):
    # Define output path next to script
    output_path = os.path.join(os.path.dirname(__file__), filename)

    # Setup figure size dynamically
    fig, ax = plt.subplots(figsize=(12, 2 + 0.5 * len(df)))
    ax.axis('off')

    # Clean row/column names
    col_labels = [col.replace("_", " ") for col in df.columns]
    row_labels = [idx.replace("_Close", "").replace("_", " ") for idx in df.index]

    # Build table
    table = ax.table(
        cellText=df.round(2).values.astype(str),
        colLabels=col_labels,
        rowLabels=row_labels,
        cellLoc='center',
        rowLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 1.5)

    # Header formatting
    for (row, col), cell in table.get_celld().items():
        if row == 0 or col == -1:
            cell.set_fontsize(13)
            cell.set_text_props(weight='bold')
            cell.set_facecolor("#f0f0f0")

    # Add title and save
    plt.title(title, fontsize=16, weight='bold', pad=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')  # <-- Save BEFORE plt.show()
    print(f"\nImage saved at: {output_path}")

    # Optional: Show and open
    plt.show()

# actually run the function
plot_df_table(summary)
