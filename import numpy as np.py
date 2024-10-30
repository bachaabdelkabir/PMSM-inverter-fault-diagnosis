import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Define the data
setpoints = [30, 40, 50, 60]
thermistor_readings = [
    [463, 385, 311, 264],  # 30°C setpoint
    [380, 311, 264, 222],  # 40°C setpoint
    [300, 251, 212, 181],  # 50°C setpoint
    [218, 181, 154, 132]   # 60°C setpoint
]

# Flatten the data for curve fitting
X = np.repeat(setpoints, 4)
Y = np.array(thermistor_readings).flatten()

# Define the curve fitting function (Steinhart-Hart equation)
def steinhart_hart(R, A, B, C):
    return 1 / (A + B * np.log(R) + C * (np.log(R))**3)

# Perform curve fitting
popt, _ = curve_fit(steinhart_hart, Y, 1/(X + 273.15))

# Generate points for the fitted curve
R_fit = np.linspace(min(Y), max(Y), 1000)
T_fit = steinhart_hart(R_fit, *popt) * 1000 - 273.15

# Create the plot
plt.figure(figsize=(10, 6))
for i, setpoint in enumerate(setpoints):
    plt.scatter(thermistor_readings[i], [setpoint]*4, label=f'{setpoint}°C Setpoint')

plt.plot(R_fit, T_fit, 'r-', label='Fitted Curve')

plt.xlabel('Thermistor Reading')
plt.ylabel('Temperature (°C)')
plt.title('Thermistor Calibration Curve')
plt.legend()
plt.grid(True)

# Add the equation to the plot
equation = f'T = 1 / ({popt[0]:.2e} + {popt[1]:.2e}*ln(R) + {popt[2]:.2e}*(ln(R))³) - 273.15'
plt.text(0.05, 0.05, equation, transform=plt.gca().transAxes, fontsize=10, verticalalignment='bottom')

plt.show()

# Print the Steinhart-Hart coefficients
print(f"A = {popt[0]:.6e}")
print(f"B = {popt[1]:.6e}")
print(f"C = {popt[2]:.6e}")