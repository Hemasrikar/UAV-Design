import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Atlas II, Shahbal, Arya UAV, Lancaster-5, Warmate, Avian Puma AE UAV, Blackswift S2, Skyrobot FX-20
Wo_data = np.array([ 10, 17.5, 9.75, 3.55, 5.7, 7, 9.5, 12]).reshape(-1, 1)
fuselage_length = np.array([ 1.15, 1.921, 2.093, 0.982, 1.1, 1.657, 1.673, 1.05])


# Natural logarithm of both sides of the equation
ln_fuselage_length = np.log(fuselage_length)
ln_Wo = np.log(Wo_data)


regression_model = LinearRegression().fit(ln_Wo, ln_fuselage_length)
R_squared = regression_model.score(ln_Wo, ln_fuselage_length)

c = regression_model.coef_[0]
ln_a = regression_model.intercept_

a = np.exp(ln_a)

print(ln_fuselage_length)
print("a:", a)
print("c:", c)

# Plotting the data points and the regression line
plt.figure(figsize=(8, 6))
plt.scatter(ln_Wo, ln_fuselage_length, label='Data Points')
plt.plot(ln_Wo, regression_model.predict(ln_Wo), color='red', label='Regression Line')
plt.xlabel('ln($W_{0}$)')
plt.ylabel('ln(Fuselage Length)')
plt.title('Linear Regression of Logarithmic Equation')
plt.legend()
plt.grid(True, linestyle='dashed')
plt.show()


