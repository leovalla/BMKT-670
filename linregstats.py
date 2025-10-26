import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Data
x = np.array([1, 5, 3, 7, 2, 11])
y = np.array([2, 4, 1, 5, 3, 7])

# Add constant for intercept and fit OLS
X = sm.add_constant(x)  # creates a column of 1s (tells model
model_sm = sm.OLS(y, X).fit()
print(model_sm.summary())  # full table: coef, std err, t, p,

# Get fitted values for plotting
y_hat_sm = model_sm.predict(X)

# Plot
plt.scatter(x, y, label="Data")
plt.plot(x, y_hat_sm, label="Best-fit line (statsmodels)")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Simple Linear Regression - statsmodels")
plt.legend()
plt.show()