import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


# Data of empty weight and total weight (Wo) of different planes

# Planes with Landing Gear
# Wo_data = np.array([21.5, 9, 10, 15, 39, 17.5, 9.75]).reshape(-1, 1)
# We_data = np.array([14.9, 3.3, 3, 6.5, 35, 9.5, 5.5])

# All planes data]
Wo_data = np.array([ 9, 10, 15, 17.5, 9.75, 3.55, 5.7, 7]).reshape(-1, 1)
We_data = np.array([ 3.3, 3, 6.5, 9.5, 5.5, 2.4, 4, 5.9])


# Calculation of the empty-to-weight ratio (we/wo)
we_wo_data = We_data / Wo_data.ravel()

# Natural logarithm of both sides of the equation
ln_We_Wo = np.log(we_wo_data)
ln_Wo = np.log(Wo_data)


regression_model = LinearRegression().fit(ln_Wo, ln_We_Wo)
R_squared = regression_model.score(ln_Wo, ln_We_Wo)


L = regression_model.coef_[0]
ln_A = regression_model.intercept_


A = np.exp(ln_A)

# Plotting the data points and the regression line
plt.figure(figsize=(8, 6))
plt.scatter(ln_Wo, ln_We_Wo, label='Data Points')
plt.plot(ln_Wo, regression_model.predict(ln_Wo), color='red', label='Regression Line')
plt.xlabel('ln($W_{0}$)')
plt.ylabel('ln($W_{e}/{W_{0}}$)')
plt.title('Linear Regression of Logarithmic Equation')
plt.legend()
plt.grid(True, linestyle='dashed')
plt.show()



print("A:", A)
print("L:", L)