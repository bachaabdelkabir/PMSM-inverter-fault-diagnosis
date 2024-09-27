
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os  # Add this line to import the os module

def adc_to_current_acs712_20a(adc_value):
    voltage = (adc_value / 1023) * 5  # Convert ADC to voltage
    current = (voltage - 2.5) / 0.100  # 100mV/A for ACS712 20A
    return current

def arduino_acs712_current(raw_value):
    return 0.074 * (raw_value - 512)

def adc_to_voltage_acs712_100ohm(adc_value):
    voltage = (adc_value / 1023) * 5  # Convert ADC to voltage
    current = (voltage - 2.5) / 0.100  # 100mV/A for ACS712 20A
    return current * 100  # Ohm's law: V = I * R

def adc_to_temperature_ntc(adc_value):
    # Constants
    R1 = 10000  # Fixed resistor value in ohms
    A = 1.2666e-3
    B = 2.3661e-4
    C = 9.6094e-8

    # Calculate thermistor resistance
    R_th = R1 / ((1023 / adc_value) - 1)

    # Steinhart-Hart equation
    ln_R_th = np.log(R_th)
    temp_kelvin = 1 / (A + B * ln_R_th + C * ln_R_th**3)

    return temp_kelvin - 273.15  # Convert Kelvin to Celsius



# Load the CSV file
df = pd.read_csv('your_dataset.csv')

# Add timestamp column
df['Timestamp'] = pd.Series(np.arange(0, len(df) * 0.1, 0.1))

# Convert data types to float for numeric columns
numeric_columns = ['Ia', 'Ib', 'VDC', 'IDC', 'T1', 'T2', 'T3', 'VD']
df[numeric_columns] = df[numeric_columns].astype(float)

# Apply conversions
df['Ia_original'] = df['Ia'].apply(adc_to_current_acs712_20a)
df['Ia_arduino'] = df['Ia'].apply(arduino_acs712_current)
df['Ib_original'] = df['Ib'].apply(adc_to_current_acs712_20a)
df['Ib_arduino'] = df['Ib'].apply(arduino_acs712_current)
df['VDC'] = df['VDC'].apply(adc_to_voltage_acs712_100ohm)
df['IDC_original'] = df['IDC'].apply(adc_to_current_acs712_20a)
df['IDC_arduino'] = df['IDC'].apply(arduino_acs712_current)
df['T1'] = df['T1'].apply(adc_to_temperature_ntc)
df['T2'] = df['T2'].apply(adc_to_temperature_ntc)
df['T3'] = df['T3'].apply(adc_to_temperature_ntc)
df['VD'] = df['VD'].apply(adc_to_voltage_acs712_100ohm)

# Calculate new derived features

# 1. Electrical Power
df['Power_DC'] = df['VDC'] * df['IDC_arduino']
df['Power_AC'] = df['VD'] * (df['Ia_arduino'] + df['Ib_arduino'])  # Assuming two-phase system

# 2. Current Imbalance
df['Current_Imbalance'] = np.abs(df['Ia_arduino'] - df['Ib_arduino']) / ((df['Ia_arduino'] + df['Ib_arduino']) / 2)

# 3. Temperature Difference
df['Temp_Diff_Max'] = df[['T1', 'T2', 'T3']].max(axis=1) - df[['T1', 'T2', 'T3']].min(axis=1)

# 4. Normalized Currents
df['Ia_Normalized'] = df['Ia_arduino'] / df['IDC_arduino']
df['Ib_Normalized'] = df['Ib_arduino'] / df['IDC_arduino']

# 5. Rate of Change
df['VDC_RateOfChange'] = df['VDC'].diff() / 0.1  # 0.1 seconds between samples
df['IDC_RateOfChange'] = df['IDC_arduino'].diff() / 0.1

# 6. Moving Averages (for trend analysis)
window_size = 10  # Adjust as needed
df['VDC_MovingAvg'] = df['VDC'].rolling(window=window_size).mean()
df['IDC_MovingAvg'] = df['IDC_arduino'].rolling(window=window_size).mean()

# Display the first few rows of the converted data
print("First few rows of converted data with new features:")
print(df.head())

# Display statistical summary
print("\nStatistical summary:")
print(df.describe())

# Count of each fault type
print("\nFault type distribution:")
print(df['FDD'].value_counts())

# Get the current working directory
current_dir = os.getcwd()

# Export the converted dataset to a new CSV file
csv_filename = 'converted_dataset.csv'
csv_path = os.path.join(current_dir, csv_filename)
df.to_csv(csv_path, index=False)
print(f"\nConverted dataset with new features and timestamp has been saved to {csv_path}")

# Export the converted dataset to a new Excel file
excel_filename = 'converted_dataset.xlsx'
excel_path = os.path.join(current_dir, excel_filename)
df.to_excel(excel_path, index=False, engine='openpyxl')
print(f"Converted dataset with new features and timestamp has been saved to {excel_path}")

# Visualization of new features
plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['Power_DC'], label='DC Power')
plt.plot(df['Timestamp'], df['Power_AC'], label='AC Power')
plt.title('DC and AC Power over Time')
plt.xlabel('Time (s)')
plt.ylabel('Power (W)')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['Current_Imbalance'], label='Current Imbalance')
plt.title('Current Imbalance over Time')
plt.xlabel('Time (s)')
plt.ylabel('Imbalance Ratio')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['Temp_Diff_Max'], label='Max Temperature Difference')
plt.title('Maximum Temperature Difference over Time')
plt.xlabel('Time (s)')
plt.ylabel('Temperature Difference (°C)')
plt.legend()
plt.show()

plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['VDC_RateOfChange'], label='VDC Rate of Change')
plt.plot(df['Timestamp'], df['IDC_RateOfChange'], label='IDC Rate of Change')
plt.title('Rate of Change of VDC and IDC over Time')
plt.xlabel('Time (s)')
plt.ylabel('Rate of Change')
plt.legend()
plt.show()

# Updated correlation heatmap
plt.figure(figsize=(12, 10))
correlation_matrix = df.drop(['FDD', 'Ia', 'Ib', 'IDC'], axis=1).corr()
sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm')
plt.title('Correlation Heatmap of Features (Including Derived Features)')
plt.show()