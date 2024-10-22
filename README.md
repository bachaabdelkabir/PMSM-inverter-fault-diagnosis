# PMSM Inverter Fault Dataset

## Dataset Overview
This dataset contains comprehensive multi-sensor measurements from an inverter-driven PMSM system under various fault conditions. It provides valuable data for developing and validating fault detection and diagnosis algorithms in motor drive systems.

### Key Features
- 10,892 samples across 9 operational conditions
- 8 raw sensor measurements
- 15 derived features
- Data collected at 10 Hz sampling rate
- Fault scenarios including open-circuit, short-circuit, and overheating conditions

### Keywords
- PMSM
- Fault Detection
- Inverter Faults
- Motor Drive Systems
- Experimental Data
- Machine Learning

## Data Collection

### Experimental Setup
The data was collected from a custom-built experimental setup consisting of:
- Three-phase voltage source inverter with MOSFETs (IRF540N)
- PMSM (converted DENSO car alternator)
- Arduino-based control system
- Multiple sensors for current, voltage, and temperature measurements

### Sensor Specifications
| Sensor Type | Application | Specifications |
|-------------|-------------|----------------|
| ACS712 20A | Current Measurement | Sensitivity: 100mV/A |
| ACS712 with 100Ω | Voltage Measurement | Voltage divider configuration |
| 10k NTC | Temperature Measurement | With 10k resistor voltage divider |
| SCANCON Encoder | Position Measurement | 100 PPR resolution |

### Data Collection Protocol
1. System initialization in normal operating condition
2. Motor operation at constant speed (10 rad/s)
3. Data recording for approximately 5 minutes per condition
4. Fault introduction and monitoring
5. Continuous data collection during fault conditions

## Dataset Structure

### File Organization
```
dataset/
├── README.md                 # Dataset documentation
├── raw_data/                # Raw sensor measurements
│   ├── normal_operation/
│   ├── fault_scenarios/
│   └── thermistor_calib_data/
├── processed_data/          # Preprocessed data
│   ├── features/
│   └── labels/
├── metadata/                # Data description files
│   ├── sensor_specs.csv
│   └── fault_definitions.csv
├── code/                    # Example scripts
│   ├── data_conversion_script_v4.py
│   ├── calibrage_thermistance.cpp
│   └── dataAcq.cpp
└── visualizations/          # Key plots and figures
```

### Feature Descriptions
| Feature Name | Description | Sensor Type | Raw Range |
|--------------|-------------|-------------|-----------|
| Ia | Phase A inline current | ACS712 20A | 0-1023 |
| Ib | Phase B inline current | ACS712 20A | 0-1023 |
| Vdc | DC bus voltage | ACS712 20A with 100Ω resistor | 0-1023 |
| Idc | DC bus current | ACS712 20A | 0-1023 |
| T1 | Temperature of Half bridge 1 | 10k NTC with voltage divider | 0-1023 |
| T2 | Temperature of Half bridge 2 | 10k NTC with voltage divider | 0-1023 |
| T3 | Temperature of Half bridge 3 | 10k NTC with voltage divider | 0-1023 |
| Vd | Driver voltage | ACS712 20A with 100Ω resistor | 0-1023 |

### Fault Labels
| Label | Description | Number of Samples |
|-------|-------------|------------------|
| F0 | Normal operation | 4295 |
| F1-F2 | Open-circuit faults | 1814 |
| F3-F5 | Short-circuit faults | 1160 |
| F6-F8 | Overheating conditions | 3623 |

## Usage Instructions

### Data Loading Example
```python
import pandas as pd

# Load raw data
data = pd.read_csv('raw_data/sensor_measurements.csv')

# Load preprocessed features
features = pd.read_csv('processed_data/features/derived_features.csv')

# Load fault labels
labels = pd.read_csv('processed_data/labels/fault_labels.csv')
```

### Basic Data Processing Example
```python
# Convert ADC values to physical units
def convert_current(adc_value):
    return (adc_value - 512) * 0.185  # For ACS712 20A

def convert_temperature(adc_value):
    # NTC conversion using Steinhart-Hart equation
    # Constants from calibration data
    pass

# Apply conversions
data['Ia_amps'] = data['Ia'].apply(convert_current)
data['T1_celsius'] = data['T1'].apply(convert_temperature)
```

## License
This dataset is released under Creative Commons Attribution 4.0 International License.

## Contact
**Prof Abdelkabir BACHA**  
Institut Supérieur d'Etudes Maritimes  
Hassan II University of Casablanca

Email:
- abdelkabir.bacha@ensem.ac.ma
- a.bacha@isem.ac.ma

## Citation
If you use this dataset in your research, please cite:
```
[Citation information will be added after publication]
```

DOI

10.5281/zenodo.13974503

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.13974503.svg)](https://doi.org/10.5281/zenodo.13974503)


