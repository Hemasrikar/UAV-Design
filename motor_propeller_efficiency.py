import numpy as np
import matplotlib.pyplot as plt


# Motor Data
motor_kv_data = 320
motor_v_data = np.array([24.30, 24.29, 24.27, 24.26, 24.25, 24.23, 24.22, 24.20, 24.19, 24.17, 24.16, 24.14, 24.12, 24.11, 24.09, 24.07, 23.97, 23.86, 23.70])
motor_torque = np.array([0.37, 0.39, 0.42, 0.44, 0.48, 0.51, 0.54, 0.57, 0.60, 0.63, 0.66, 0.69, 0.72, 0.75, 0.78, 0.80, 0.96, 1.11, 1.30])
motor_thrust = np.array([1573, 1677, 1795, 1895, 2048, 2156, 2264, 2409, 2543, 2666, 2788, 2927, 3061, 3194, 3300, 3421, 4112, 4694, 5547])*0.00981
current_data = np.array([5.65, 6.16, 6.81, 7.42, 8.12, 8.83, 9.61, 10.48, 11.17, 12.04, 12.96, 13.85, 14.81, 15.67, 16.66, 17.57, 23.37, 29.44, 38.31])
RPM_data = np.array([2681, 2765, 2858, 2953, 3036, 3120, 3205, 3288, 3369, 3454, 3536, 3608, 3684, 3760, 3830, 3903, 4256, 4569, 4935]) * 0.1047
power_data = np.array([137, 150, 165, 180, 197, 214, 233, 254, 270, 291, 313, 334, 357, 378, 401, 423, 560, 703, 908])
overall_efficiency = np.array([11.47, 11.20, 10.86, 10.52, 10.40, 10.08, 9.73, 9.50, 9.41, 9.16, 8.90, 8.76, 8.57, 8.45, 8.22, 8.09, 7.34, 6.68, 6.11]) # in g/Watt

# Motor Efficiency
mecahnical_poweroutput = motor_torque * RPM_data
motor_efficiency = mecahnical_poweroutput / power_data

# Propeller Efficiency
propeller_Efficiency = overall_efficiency / (motor_efficiency*1000)


plt.figure(figsize=(8, 6))
plt.plot( RPM_data , motor_efficiency, color='red', label='Motor Efficiency')
plt.xlabel('RPM')
plt.ylabel('Efficiency ($\eta$) ')
plt.title('Effieciency of Motor')
plt.legend()
plt.grid(True, linestyle='dashed')
plt.show()

plt.figure(figsize=(8, 6))
plt.plot( RPM_data, propeller_Efficiency, color='blue', label='Propeller Efficiency')
plt.xlabel('RPM')
plt.ylabel('Efficiency ($\eta$) (in Kg/Watt) ')
plt.title('Effieciency of Propeller')
plt.legend()
plt.grid(True, linestyle='dashed')
plt.show()

print("Motor Efficiency:", motor_efficiency)
print("Propeller Efficiency:", propeller_Efficiency)