#-------------------------------------------------------------------------------
# project_5_madison_project_leo_valladares.py
# This project analyzes Madisson data
# Author: Leonardo Valladares
# Date: 2025-10-10
#------------------------------------------------------------------------------

# --------------------------------------
# Import necessary libraries
# --------------------------------------
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the Maddison data
df = pd.read_csv("mpd2023_web.csv")

# --------------------------------------
# Select countries to include 
# --------------------------------------

# # Count valid (non-null) rows for each country based on both 'gdppc' and 'pop'
# df_valid = df.dropna(subset=["gdppc", "pop"])

# # Group by country and count number of valid rows
# summary = (
#     df_valid
#     .groupby(["countrycode", "country", "region"])
#     .size()
#     .reset_index(name="valid_years")
#     .sort_values(by="valid_years", ascending=False)
# )

# Show top 10 countries with the most data
# print(summary.head(100))

# countries to include Spain (ESP), United States (USA), Australia (AUS), France (FRA),
# United Kingdom (GBR), and Germany (DEU)

# --------------------------------------
# Filter and clean
# --------------------------------------
# Define selected countries
countries = ["ESP", "USA", "AUS", "FRA", "GBR", "DEU"]

# Keep only relevant columns
df = df[["countrycode", "country", "year", "gdppc", "pop"]]

# Keep only selected countries
df = df[df["countrycode"].isin(countries) & (df["year"] >= 1820)]

# Convert columns to numeric types and handle errors safely
df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")  # allows missing ints
df["gdppc"] = pd.to_numeric(df["gdppc"], errors="coerce")
df["pop"] = pd.to_numeric(df["pop"], errors="coerce")

# Drop rows with missing GDP or population
df = df.dropna(subset=["gdppc", "pop", "year"])

# Convert to standard integer types now that NaNs are gone
df["year"] = df["year"].astype(int)
df["gdppc"] = df["gdppc"].astype(int)
df["pop"] = df["pop"].astype(int)

# Set 'year' as the index (useful for time series plots)
df = df.set_index("year").sort_index()

# Group by country and count number of valid rows
# summary = (
#     df
#     .groupby(["countrycode"])
#     .size()
#     .reset_index(name="valid_years")
#     .sort_values(by="valid_years", ascending=False)
# )
# print(summary.head(6))

#Australia and USA have 203 valid years, while others have 207

# --------------------------------------
# Plot GDP per capita over time
# --------------------------------------

# Using Seaborn, depict GDP per capita of the 5 countries over time (line chart)
plt.figure(figsize=(12, 6))
sns.lineplot(data=df, x=df.index, y="gdppc", hue="country")
plt.title("GDP per Capita Over Time")
plt.xlabel("Year")
plt.ylabel("GDP per Capita")
plt.legend(title="Country")
plt.show()

# --------------------------------------
# Calculate sigma convergence: standard deviation of log(gdppc) per year
# --------------------------------------

# Calculate log of GDP per capita 
df["log_gdppc"] = np.log(df["gdppc"])

# Calculate sigma convergence
sigma = df.groupby(df.index)["log_gdppc"].std().reset_index()
sigma.columns = ["year", "sigma_convergence"]

# Plot sigma convergence over time. 
plt.figure(figsize=(10, 6))
sns.lineplot(data=sigma, x="year", y="sigma_convergence")
plt.title("Sigma Convergence Over Time")
plt.xlabel("Year")
plt.ylabel("Sigma Convergence")
plt.tight_layout()
plt.savefig("sigma_convergence.png")
plt.show()
