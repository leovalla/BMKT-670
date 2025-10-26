import matplotlib.pyplot as plt
import numpy as np

#Independent variable x axis
x = np.array([1,5,3,7,2,11])
#Dependent variable y axis
y = np.array([2,4,1,5,3,7])

#Scatter plot
plt.scatter(x, y)
#Naming axes
plt.xlabel('x - axis')
plt.ylabel('y - axis')

# Use NumPy to calculate the best-fit line (slope and intercept)
slope, intercept = np.polyfit(x, y, 1)
print(f"Slope: {slope:.2f}, Intercept: {intercept:.2f}")

# Predicted values (the regression line)
y_hat = slope * x + intercept
plt.plot(x, y_hat, color='green', label='Best-fit line')

# Example of one deviation (error) for a specific point
x1 = np.array([2, 2])
y1 = np.array([intercept + slope*2, 3])  # connects predicted to actual
plt.plot(x1, y1, color='red', label='Example deviation')

#Save figure
plt.savefig("reg_illustration.png")
plt.show()