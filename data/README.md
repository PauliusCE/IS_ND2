
# Dataset: Simulated Patch Antenna for 2.4 GHz Applications

## Overview
This dataset contains 55,053 simulation samples of a patch antenna designed for operation around the 2.4 GHz ISM band. Each sample represents a different antenna configuration, with corresponding S11 (return loss) values measured in dB across frequencies ranging from 1.8 GHz to 2.8 GHz.

The dataset is intended to support research in:
- Machine Learning-based antenna design and optimization
- Electromagnetic simulation analysis
- Wearable and IoT antenna development

## File Structure
- "cleaned_dataset.csv": The cleaned and structured dataset ready for direct use in ML applications.
- "antenna_geometry.png":  snapshot of the antenna design.
- "ML_Patch_Antenna.ipynb":  A sample notebook demonstrating how to predict S11 using a regression model.
- "README.md": This file.

## Dataset Description

| Column Name            | Unit      | Description |
|------------------------|-----------|-------------|
| width_substrate_mm     | mm        | Width of the dielectric substrate |
| width_imp_line_mm      | mm        | Width of the microstrip feed line |
| length_imp_line_mm     | mm        | Length of the microstrip feed line |
| substrate_height_mm    | mm        | Height/thickness of the substrate |
| patch_height_mm        | mm        | Thickness of the patch metal layer |
| width_slot_mm          | mm        | Width of the slot within the patch |
| length_slot_mm         | mm        | Length of the slot |
| patch_width_mm         | mm        | Width of the patch |
| substrate_length_mm    | mm        | Length of the substrate |
| patch_length_mm        | mm        | Length of the patch |
| frequency_GHz          | GHz       | Frequency of analysis |
| S11_dB                 | dB        | Simulated reflection coefficient (S11) |

## Simulation Conditions
- Software: CST Microwave Studio 
- Substrate: FR4 (εr = 4.3), height 1.6 mm
- Patch material: PEC
- Frequency sweep: 1.8 to 2.8 GHz

## Cleaning and Processing
- Removed duplicate entries and corrupted simulations
- Formatted all numerical values in SI units
- Normalized S11 range 
- Consistent spacing of frequency values

## How to Use
The cleaned dataset can be used for:
- Training ML models (e.g., SVR, XGBoost, Neural Networks)
- Regression of S11 based on physical parameters
- Inverse design (predicting optimal dimensions for a target S11)

## License
This dataset is released under the CC BY 4.0 License.

## Contact
For questions or suggestions, please contact the author: [Ameni Mersani / mersani.ameni@gmail.com]

