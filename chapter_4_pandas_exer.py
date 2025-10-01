import pandas as pd

data = pd.read_csv('hh_data.csv')
print("Head of the dataset:")
print(data.head())
print("\nStatistical summary of the dataset:")
print(data.describe())
print("\nShape of the dataset:")
print(data.shape)