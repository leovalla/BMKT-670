#-------------------------------------------------------------------------------
# project_4_titanic_leo_valladares.py
# This project analyzes Titanic passenger data
# Author: Leonardo Valladares
# Date: 2025-09-28
#------------------------------------------------------------------------------

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Load data
pd.set_option("display.max_columns", None)  # Show all columns
# Load Titanic dataset from seaborn
titanic = sns.load_dataset("titanic")

# 2. Inspect the data
print(type(titanic)) # Titanic is a dataframe
print(titanic.describe(include='all'))
print(titanic.head())

# 3. Apply a log transformation (handle zero fares safely - remember log(0) is undefined).
titanic['log_fare'] = np.log(titanic['fare'] + 1)  # Adding a small constant to avoid log(0)
print(titanic[['fare', 'log_fare']].head())

# 4. Plot histograms
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6)) 
sns.histplot(titanic['fare'], bins=40, kde=True, ax=axes[0]) 
axes[0].set_title('Distribution of Fare')
axes[0].set_xlabel('Fare')
axes[0].set_ylabel('Frequency')
sns.histplot(titanic['log_fare'], bins=40, kde=True, ax=axes[1])
axes[1].set_title('Distribution of Log(Fare)')
axes[1].set_xlabel('Log(Fare)')
axes[1].set_ylabel('Frequency')
plt.savefig('titanic_histograms.png')
plt.show()

