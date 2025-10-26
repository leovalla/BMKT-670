import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.iolib.summary2 import summary_col
from sklearn.linear_model import LinearRegression

#STEP 1: Data import
#Import csv files as DataFrame
file = "uk_property_data.csv"
df = pd.read_csv(file)
print(df.head())

#STEP 2: Convert date variable
df['time_split'] = df.time.str.split("-")
print()
print(df.head())

#Create year and month variable
df['year'] = df.time_split.apply(lambda x: int(x[0]))
df['month'] = df.time_split.apply(lambda x: int(x[1]))

#Remove unwanted columns
df = df.drop('time_split', axis=1)

#Check DataFrame
print()
print(df.head())

#STEP 3: Plot time series
#Set index
df = df.set_index('time')
fig1, axes = plt.subplots(nrows=2, ncols=1)
axes[0].set_ylabel('Price')
axes[1].set_ylabel('Volume')
df.price.plot(ax=axes[0])
df.volume.plot(ax=axes[1], color='red')
plt.tight_layout()
fig1.savefig("reg_series.png")
# plt.show()

#STEP 4: Seasonal adjustment and lags
df['adj_price'] = (df.price-df.price.shift(12)).shift(1)
df['adj_volume'] = df.volume-df.volume.shift(12)
df['d_volume'] = df.volume.diff()
fig2, axes = plt.subplots(nrows=3, ncols=1)
axes[0].set_ylabel('Diff Volume')
axes[1].set_ylabel('Adjusted Volume')
axes[2].set_ylabel('Adjusted Price')
df.d_volume.plot(ax=axes[0], color='green')
df.adj_volume.plot(ax=axes[1], color='red')
df.adj_price.plot(ax=axes[2], color='blue')
plt.tight_layout()
fig2.savefig("reg_adjustment.png")
# plt.show()

#STEP 5: Regression models
mod1 = smf.ols('adj_volume ~ adj_price', data=df)
res1 = mod1.fit()
print(res1.summary())

# --- Create the regression plot ---
# Scatter plot of actual data
plt.figure(figsize=(8,6))
plt.scatter(df['adj_price'], df['adj_volume'], label='Observed data')

# Predicted (fitted) line
pred_df = pd.DataFrame({'adj_price': sorted(df['adj_price'])})
pred_df['predicted_volume'] = res1.predict(pred_df)

plt.plot(pred_df['adj_price'], pred_df['predicted_volume'],
         color='red', linewidth=2, label='Regression line')

# Labels and title
plt.xlabel('Adjusted Price')
plt.ylabel('Adjusted Volume')
plt.title('Regression: Adjusted Volume vs Adjusted Price')
plt.legend()
plt.tight_layout()
# plt.show()

#STEP 6: Create year dummies
year_dummies = pd.get_dummies(data = df.year, prefix = 'Y')
df = df.join(year_dummies)
print(df)


#STEP 7: Second model with year effects, 2005-2023
mod2 = smf.ols('adj_volume ~ adj_price + Y_2008 + Y_2009', data=df)
res2 = mod2.fit()
print(res2.summary())

#STEP 8: Regression tables
info_dict={'N':lambda x: "{0:d}".format(int(x.nobs)),'R2':lambda x: "{:.2f}".format(x.rsquared)}
dfoutput = summary_col([res1,res2],stars=True,float_format="%.3f", \
model_names=['Reference', 'Year'], info_dict=info_dict, \
regressor_order=['const','adj_price','Y_2008','Y_2009'])
print("Regression Results Table")
print(dfoutput)