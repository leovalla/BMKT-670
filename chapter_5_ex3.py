import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Import data as DataFrame
df = pd.read_csv('food_price_index.csv')
print(df.head())

# Set index
df = df.set_index(df['Year'])

# Multiple lines
sns.lineplot(
    data=df[['Nominal', 'Real']],
    palette=['red', 'blue'],
    markers=True,
    dashes=True
)
plt.savefig('DV_food.png')
plt.show()
