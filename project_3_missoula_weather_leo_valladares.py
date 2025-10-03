#-------------------------------------------------------------------------------
# project_3_missoula_weather_leo_valladares.py
# This project analyzes weather data for Missoula, Montana
# Author: Leonardo Valladares
# Date: 2025-09-27
#------------------------------------------------------------------------------

# Import libraries
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. Load data
url = "https://data.berkeleyearth.org/auto/Stations/TAVG/Text/165187-TAVG-Data.txt"
response = requests.get(url, allow_redirects=True)
file_name = "Missoula_output.txt"
with open(file_name, 'w') as f:
    f.write(response.text)

# 2. Parse data
data = np.loadtxt(file_name, comments="%")
df_missoula = pd.DataFrame(data[:, :6], columns=["year", "month", "m_ano", "m_temp", "a_ano", "a_temp"])
df_missoula = df_missoula[["year", "month", "m_ano"]]
df_missoula = df_missoula.rename(columns={"m_ano": "Missoula"})

# 3. Create datetime column for plotting
df_missoula['date'] = pd.to_datetime(df_missoula[['year', 'month']].assign(day=1))
df_missoula.set_index('date', inplace=True)

# 4. Calculate 12-month rolling average
df_missoula['Rolling_12mo'] = df_missoula['Missoula'].rolling(window=12).mean()

# 5. Plot both on a grid
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 8), sharex=True)

# Top: Raw anomalies
df_missoula['Missoula'].plot(ax=axes[0], color='green')
axes[0].set_ylabel("Anomaly")
axes[0].set_title("Missoula Monthly Temperature Anomalies")

# Bottom: Smoothed anomalies
df_missoula['Rolling_12mo'].plot(ax=axes[1], color='orange')
axes[1].set_ylabel("Smoothed Anomaly")
axes[1].set_xlabel("Year")
axes[1].set_title("Missoula 12-Month Rolling Mean of Temperature Anomalies")

plt.tight_layout()
plt.savefig("Missoula_Climate_Grid.png")
plt.show()
