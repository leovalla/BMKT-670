import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('co2_emissions.csv')
print(df.head())
df = df.set_index(df['Year'])

# this is a type of Series 
temp = df['Emission'][df['Entity'] == 'World']
print(type(temp))
print(temp.head())
print("")

# this is a convversion to DataFrame 
# it was shown by the professor only so we can understand the difference 
# between Series and DataFrame
temp = temp.reset_index()
print(type(temp))
temp.columns = ['Year', 'Emission']
print(temp.head())

df['Emission'][df['Entity'] == 'World'].plot(title='Global Emissions',
                                             ylabel='CO2 Emission',
                                             logy=True)

print(df.head())
plt.savefig('DV_world.png')
plt.show()
