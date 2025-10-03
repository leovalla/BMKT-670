import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Country list
countries = ["india", "united-kingdom"]

# Empty list
dfs = []

for country in countries:
    # API URL
    url_part1 = "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Regional/TAVG/"
    url_part2 = "-TAVG-Trend.txt"
    url = url_part1 + country + url_part2
    response = requests.get(url, allow_redirects=True)

    # obtain strings
    strings = response.text
    file_name = country + "_output.txt"
    open(file_name, 'w').write(strings)

    #Load data to obtain DataFrame
    data = np.loadtxt(file_name, comments= "%")
    df_name = pd.DataFrame(data[:,:6], columns=["year", "month", "m_ano", "m_temp", "a_ano", "a_temp"])    
    dfs.append(df_name)

#Merge Data
dfs = [df[["year", "month", "m_ano"]] for df in dfs]
print(dfs[0].head())

#Rename variable
dfs_renamed = []
for df, country in zip(dfs, countries):
    df = df.rename(columns={"m_ano": country})
    dfs_renamed.append(df)
print(dfs_renamed[0].head())

# Merge Dataframes 
df_merged = dfs_renamed[0].merge(dfs_renamed[1])
df_merged.reindex(["year", "month"])
print(df_merged.head())
print(df_merged.tail())

# Plot temperatures
fig, axes = plt.subplots(nrows = 1, ncols = 2, sharey = True)
df_merged['india'].plot(ax = axes[0], color = 'red')
df_merged['united-kingdom'].plot(ax = axes[1], color = 'blue')

# Modifications
axes[0].set_xlabel('Time')
axes[1].set_xlabel('Time')

axes[0].set_ylabel('Anomaly')
axes[0].set_title('India')
axes[1].set_title('UK')

plt.savefig('DW_climate.png')
plt.show()

