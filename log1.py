import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv("ad_click.csv")
print("Head of the DataFrame:")
print(df.head())
print()
print("Info about the DataFrame:")
print(df.info())
print()
print("Descriptive statistics of the DataFrame:")
print(df.describe())
print()
print("Shape of the DataFrame:")
print(df.shape)
print()

sns.set_style("darkgrid")
g = sns.pairplot(df, height=2.5, corner=True)

def corr(x, y, **kwargs):
    # Calculate the value
    coef = np.corrcoef(x, y)[0][1]
    
    # Make the label
    label = r'$\rho$ = ' + str(round(coef, 2))

# Add the label to the plot
    ax = plt.gca()
    ax.annotate(label, xy=(0.25, 0.75), size=11, xycoords=ax.transAxes)


g.map_lower(corr)
plt.show()