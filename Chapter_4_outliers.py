import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("hh_data.csv")
pd.set_option('display.float_format', '{:.2f}'.format) #Turns off scientific notation for all DataFrames
print("\nDescriptive statistics: Pandas Series\n") 
stats = data['INC'].describe() 
print(stats) 
print("\nDescriptive statistics: Pandas DataFrame\n") 
stats = data.describe(include = 'all') 
print(stats)

data['ln_INC'] = np.log(data['INC'] + 1)
#data['INC'].replace(0, np.nan, inplace = True)
#data.dropna(subset = ['INC'], inplace = True)
#print(data.describe(include = 'all'))
#data['ln_INC'] = np.log(data['INC'])

#Histograms
fig, axes = plt.subplots(nrows = 1, ncols = 2)
bin_edges = np.arange(0, 500_000 + 5000, 5000)
data['INC'].hist(bins = bin_edges, edgecolor = "black", ax = axes[0], color = 'green')
data['ln_INC'].hist(bins = 16, ax = axes[1], color = 'blue')

#Add titles and save the graph
axes[0].set_title('Income')
axes[1].set_title('Log income')
plt.savefig('DW_transform.png')
plt.show()
