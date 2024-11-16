import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

# Define the function based on the given relationship
def func(wo, A, L):
    return A * wo**L

# Planes with Landing Gear
# Wo = np.array([21.5, 9, 10, 15, 39, 17.5, 9.75])
# We = np.array([14.9, 3.3, 3, 6.5, 35, 9.5, 5.5])

# All planes data
Wo = np.array([ 9, 10, 15, 17.5, 9.75, 3.55, 5.7, 7])
We = np.array([ 3.3, 3, 6.5, 9.5, 5.5, 2.4, 4, 5.9])

We_Wo = We / Wo 

p0 = [4, 0.7]

# Perform curve fitting using least squares method
popt, pcov = curve_fit(func, Wo, We_Wo, p0=p0)
A = popt[0]
L = popt[1]


sorted_indices = np.argsort(Wo)
Wo_sorted = Wo[sorted_indices]
We_Wo_sorted = A * Wo_sorted**L

print("A:", A)
print("L:", L)

plt.figure(figsize=(8, 6))
plt.scatter(Wo, We_Wo, label='Data Points')
plt.plot(Wo_sorted, We_Wo_sorted, color='red', label='Regression Line')
plt.ylabel('$W_{e}/{W_{0}}$')
plt.xlabel('$W_{0}$')
plt.title('Total Empty weight empirical Equation')
plt.legend()
plt.grid(True, linestyle='dashed')
plt.show()



