import pandas as pd
import matplotlib.pyplot as plt
import itertools

df = pd.read_csv('co2_emissions.csv')
df = df.set_index(df['Year'])

# Select data for 2022, excluding world aggregate
df_top = df[(df['Code'] != 'OWID_WRL') & (df['Year'] == 2022)].dropna()

# Sort by CO2 emissions in 2022
# Select top 5
df_top = df_top.sort_values(by=['Emission'], ascending=False).iloc[:5, :]
print(df_top)

# Add selected countries to a list
countries = df_top['Entity'].tolist()
print(countries)

# ...

# Plot top 5 countries over time
df = df[(df['Code'] != 'OWID_WRL') & (df['Year'] >= 1900)].dropna()
df = df[df['Entity'].isin(countries)]
print(df)

# Linestyles in list - this is to differentiate lines in the plot
style = itertools.cycle(["-", "--", "-.", ":", "."])

# Group by country code
grouped = df.groupby('Code')

# Plot each country
# for key, group in grouped:
#     plt.plot(group['Year'], group['Emission'], "k" + next(style), label=key) # k is black, label is country code

# plt.legend()
# plt.title('Top 5 CO2 Emitters Over Time')
# plt.xlabel('Year')
# plt.ylabel('CO2 Emissions (Million Tonnes)')
# plt.show() 

# cumulative emissions over time
print(grouped)

for key, group in grouped:
    plt.plot(group['Year'], group['Emission'].cumsum(), "k" + next(style), label=key) # k is black, label is country code 

plt.legend()
plt.title('Cumulative CO2 Emissions of Top 5 Emitters Over Time')
plt.xlabel('Year')
plt.ylabel('Cumulative CO2 Emissions (Million Tonnes)')
plt.show() 