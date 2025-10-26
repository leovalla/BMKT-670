import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

# Data
x = np.array([1, 5, 3, 7, 2, 11]).reshape(-1, 1)  # X must be 2D for sklearn
y = np.array([2, 4, 1, 5, 3, 7])

# Fit
model_skl = LinearRegression()
model_skl.fit(x, y)

# Parameters & predictions
slope = model_skl.coef_[0]
intercept = model_skl.intercept_
y_hat = model_skl.predict(x)
r2 = r2_score(y, y_hat)

print(f"[scikit-learn] Intercept: {intercept:.3f}, Slope: {slope:.3f}, R^2: {r2:.3f}")

# Plot
plt.scatter(x, y, label="Data")
plt.plot(x, y_hat, label="Best-fit line (sklearn)")
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Simple Linear Regression - scikit-learn")
plt.legend()
plt.show()