import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Import data as DataFrame
df = pd.read_csv('policy_ranking.csv')

# Remove missing values
df = df.dropna()

# Change column name
df = df.rename(columns = {
    "Country Name": "Country",
    "Time": "Year",
    "Value": "CPIA"
})

# Change float to integer for Year
df['Year'] = df['Year'].astype(int)

# Check the data structure
print(df.head())
print(df.tail())

# Define a list of years
years_selected = [2005, 2010, 2015, 2022]

# Select years
df = df[df['Year'].isin(years_selected)]

# Subplots
# Combine barplot and boxplot
sns.set_theme(style="whitegrid")
sns.color_palette("Spectral", as_cmap=True)

# Define figure with two subplots and axes
fig, axes = plt.subplots(1, 2, sharex=True, figsize=(9, 6))
fig.suptitle('Ratings over time')
axes[0].set_title('Barplot')
axes[1].set_title('Boxplot')

# Barplot
sns.barplot(
    data = df,
    x = "Year", y = "CPIA", hue = "Year",
    legend = False, ax = axes[0]
)

# Boxplot
sns.boxplot(
    data = df,
    x = "Year", y = "CPIA", hue = "Year",
    legend = False, ax = axes[1]
)

plt.savefig('DV_rating.png')
plt.show()
