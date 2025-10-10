import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Import data as DataFrame
df = pd.read_csv("uk_reserves.csv")

# Check the data structure
print(df.head())

# Drop Year 13
df = df.drop(columns = ['year'])

# Correlation matrix
corr_matrix = df.corr()
print(corr_matrix.head())

# Heat map
sns.heatmap(corr_matrix)
plt.savefig("DV_heat.png")
plt.show()
