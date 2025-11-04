#-------------------------------------------------------------------------------
# project_09_heart_disease_part_1_lv.py
# This project analyze a heart disease dataset and generate visualizations
# Author: Leonardo Valladares
# Date: 2025-11-04
#------------------------------------------------------------------------------

# --------------------------------------
# Import necessary libraries
# --------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.linear_model import LogisticRegression

# --------------------------------------
# Load data 
# --------------------------------------

df = pd.read_csv("heart_disease.csv")

# --------------------------------------
# Explore the Data
# --------------------------------------

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

# --------------------------------------
# pair plot
# --------------------------------------

sns.set_style("darkgrid")
cols = ["age", "trestbps", "chol", "thalach", "oldpeak", "target"]
print(df[cols].describe())
g = sns.pairplot(df[cols], height=2.5, corner=True)

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
