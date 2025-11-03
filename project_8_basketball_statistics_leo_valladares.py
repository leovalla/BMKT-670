#-------------------------------------------------------------------------------
# project_8_basketball_statistics_leo_valladares.py
# This project analyze a Formula 1 dataset and generate vizualizations
# Author: Leonardo Valladares
# Date: 2025-10-19
#------------------------------------------------------------------------------

# --------------------------------------
# Import necessary libraries
# --------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from sklearn.linear_model import LinearRegression

# --------------------------------------
# Load data
# --------------------------------------
file = "NBA.csv"
df = pd.read_csv(file)
#print(df.head())

# --------------------------------------
# Part 1 
# --------------------------------------

# original columns namens
print("Original names:", df.columns.tolist())

# 1.1 Rename columns that start with a number or contain '%'
df.columns = df.columns.str.replace(r'^3', 'THREE_', regex=True).str.replace('%', '_PCT')

# Verify the changes
print("Updated columns:", df.columns.tolist())

# 1.2 Create POSS column: Possessions = FGA + 0.44×FTA - OREB + TOV
df['POSS'] = df['FGA'] + 0.44 * df['FTA'] - df['OREB'] + df['TOV']

# 1.3 Create OFF_EFF:  OFF_EFF = PTS/POSS * 100
df['OFF_EFF'] = df['PTS']/df['POSS'] * 100

# 1.4 Regression models PTS = a + b*(FG%)
mod1 = smf.ols('PTS ~ FG_PCT', data=df)
res1 = mod1.fit()
print(res1.summary())

# 1.5 Regression models  PTS = a + b1*(FG%) + b2*(FT%) + b3*(3P%)
mod2 = smf.ols('PTS ~ FG_PCT + FT_PCT + THREE_P_PCT', data=df)
res2 = mod2.fit()
print(res2.summary())

# 1.6 Regression models PTS = a + b1*(OFF_EFF)
mod3 = smf.ols('PTS ~ OFF_EFF', data=df)
res3 = mod3.fit()
print(res3.summary())

# Extra. Regression models PTS = a + b1*(POSS)
mod4 = smf.ols('PTS ~ POSS', data=df)
res4 = mod4.fit()
print(res4.summary())

# 1.7 --- Create the regression plot ---
# Scatter plot of actual data
plt.figure(figsize=(8,6))
plt.scatter(df['FG_PCT'], df['PTS'], label='Observed data')

# Predicted (fitted) line
pred_df = pd.DataFrame({'FG_PCT': sorted(df['FG_PCT'])})
pred_df['predicted_PTS'] = res1.predict(pred_df)

plt.plot(pred_df['FG_PCT'], pred_df['predicted_PTS'],
         color='red', linewidth=2, label='Regression line')

# Labels and title
plt.xlabel('Field Goal Percentage (FG%)')
plt.ylabel('Points')
plt.title('Regression: Points vs FG%')
plt.legend()
plt.tight_layout()
#plt.show()


# --------------------------------------
# Part 2
# --------------------------------------

# load Sthephen Curry Data for 2024-25 season
file = "stephen_curry_24_25.csv"
df_sc = pd.read_csv(file)
print(df_sc.head())

# original columns namens
print("Names:", df_sc.columns.tolist())

# Filter out records with string values in PTS or FTA
df_sc = df_sc[pd.to_numeric(df_sc['PTS'], errors='coerce').notna() & 
              pd.to_numeric(df_sc['FGA'], errors='coerce').notna()]

# Convert numeric columns to proper numeric types
numeric_cols = ['FGA', 'PTS']
df_sc[numeric_cols] = df_sc[numeric_cols].apply(pd.to_numeric, errors='coerce')

# 2.1 Regression models PTS = a + b*(FGA)
mod5 = smf.ols('PTS ~ FGA', data=df_sc)
res5 = mod5.fit()
print(res5.summary())

# --- Create the regression plot ---
# Scatter plot of actual data
plt.figure(figsize=(8,6))
plt.scatter(df_sc['FGA'], df_sc['PTS'], label='Observed data')

# Predicted (fitted) line
pred_df_sc = pd.DataFrame({'FGA': sorted(df_sc['FGA'])})
pred_df_sc['predicted_PTS'] = res5.predict(pred_df_sc)

plt.plot(pred_df_sc['FGA'], pred_df_sc['predicted_PTS'],
         color='red', linewidth=2, label='Regression line')

# Labels and title
plt.xlabel('FGA')
plt.ylabel('Points')
plt.title('Regression: Sthephen Curry Points vs FGA')
plt.legend()
plt.tight_layout()
plt.show()
