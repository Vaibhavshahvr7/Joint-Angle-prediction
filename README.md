# Joint-Angle-prediction

Joint Angle Prediction with IMU Sensor Data - Jupyter Notebook
This repository contains a Jupyter Notebook that demonstrates a workflow for processing IMU sensor data and predicting joint angles (hip, knee, and ankle) using feature extraction, filtering, and prediction techniques.

Joint Angle prediction from raw IMU data (Code provided with the article Mayo Clinic Proceedings: Digital Health)

# Table of Contents

Requirements and Installation
Usage
Notebook Overview
License

# Requirements and Installation
Clone this repository or Download the library

All the requirement and installations are within the Notebook.

# Usage
Run the notebook file using Google collabe.

Notebook Joint_Angle_Prediction_Notebook.ipynb

Notebook Execution: Follow the steps in the notebook to:

Load and preprocess IMU data.

**
Apply filtering to smooth the sensor signals.**
Generate joint angle predictions for the hip, knee, and ankle.
Saving Processed Data: Processed data and predictions are saved as .pkl files, ready for further analysis or model training.

# Notebook Overview
Data Loading and Preprocessing:

The notebook includes code to load and clean IMU data files.
Data is processed using various helper functions defined within the notebook.
Feature Extraction and Filtering:

Extracts accelerometer and gyroscope features relevant to each joint.
Applies a low-pass Butterworth filter to remove high-frequency noise, enhancing data quality.

# Prediction:

Utilizes extracted raw IMU data to predict joint angles and evaluates the predictions using the root mean squared error (RMSE).

# License
This project is licensed under the MIT License.


