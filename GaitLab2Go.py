import numpy as np
import time
import matplotlib.pyplot as plt
import os
import pandas as pd
import glob
from scipy.signal import argrelextrema
from scipy import interpolate
from scipy.io import loadmat



class data_processing(object):
    """ GaitLab2Go Envrioment and Data Proccesing file:
    Shah, V. R., Dixon, P. C. (2022). Gait Speed and Task-Specificity in Predicting Lower-Limb Kinematics: A Deep Learning Approach Using Inertial Sensors. 
    
    def __init__(self):
        self.enviroment='GaitLab2Go'

    # Define a function to find files with a specific extension in a given path
    def find_files(self,path='.', ext='.xlsx'):
        """
        This function finds all the video files in the given path.

        Args:
          path: The path to the folder containing the video files.

        Returns:
          A list of all the video files in the given path.
        """
        # Construct the search term using the provided path and extension
        search_term = f"{path}/**/*{ext}"

        # Use a Python list to store file names instead of a NumPy array
        file_list = []

        # Iterate over files that match the search term using glob
        for file_name in glob.iglob(search_term, recursive=True):
            # Append the current file name to the file_list
            file_list.append(file_name)

        # Convert the list to a NumPy array if needed
        X = np.array(file_list)

        # Return the array containing the file names
        return X

    def delete_file(self, fl, deletefiles):
        """
        Delete specified files from a list of files.

        Parameters:
        - fl (numpy.ndarray): An array containing the names of files.
        - deletefiles (list): A list of files to be deleted from the 'fl' array.

        Returns:
        - numpy.ndarray: The updated array after removing the specified files.
        """

        # Iterate through each file to be deleted
        for de in deletefiles:
            # Find the indices of files that do not contain the current file to be deleted
            indices_to_keep = np.where(np.char.find(fl, de) == -1)[0]

            # Update the 'fl' array to keep only the files that were not found
            fl = fl[indices_to_keep]

        # Return the updated array after all specified files are deleted
        return fl

    def variables_zoo_IMU(self):
        # Define lists of body parts, sensor types, and axes
        A = ['shankR', 'thighR', 'shankL', 'thighL', 'trunk', 'footR', 'footL']
        B = ['Acc', 'Gyr']
        C = ['X', 'Y', 'Z']

        # Initialize an empty list to store the variable names
        variables = []

        # Generate variable names by combining body parts, sensor types, and axes
        for a1 in A:
            for b1 in B:
                for c1 in C:
                    variables.append(a1 + '_' + b1 + '_' + c1)
        return variables


    # This function converts data from a set of MATLAB files (in .mat format) to a Python dictionary
    # The function takes three parameters: self, fl (list of file paths), and variables (list of variable names to extract)
    def zoo2dictionary(self, fl, variables):
        # Iterate through each file in the provided file list (fl)
        for fn in fl:
            # Print a message indicating the current file being processed
            print('Extracting data from', fn)

            # Load data from the MATLAB file using the loadmat function
            data = loadmat(fn)

            # Get a list of variable names present in the 'data' field of the loaded file
            zoovariables = list(data['data'].dtype.fields.keys())

            # If the 'data' attribute does not exist in the object, create it as an empty dictionary
            if not hasattr(self, 'data'):
                self.data = {}

            # Initialize a variable to track missing variables
            missingvariable = 0

            # Iterate through the provided list of variables to extract
            for i in range(len(variables)):
                # Check if the current variable is present in the loaded data
                if len(np.where(np.char.find(zoovariables, variables[i]) == 0)[0]) > 0:
                    # If the variable is present, extract and store it in the 'data' dictionary
                    self.data[variables[i]] = data['data'][variables[i]][0, 0][0, 0][0].T
                else:
                    # If the variable is not present, print a message and set missingvariable flag to 1
                    print('skipping file because', variables[i], 'is not available')
                    missingvariable = 1

            # Check if any variables were missing in the current file
            if missingvariable == 0:
                # If no variables are missing, update the 'variables' attribute with the keys of the 'data' dictionary
                self.variables = list(self.data.keys())
                print('Extracting complete', fn)

                # Extract the file location and name for saving the pickle file
                location = fn[0:np.char.rfind(fn, '/')]
                filename = fn[np.char.rfind(fn, '/') + 1:-4]
                filelocation = location + '/' + filename + '.pkl'

                # Print a message indicating the saving process and save the object as a pickle file
                print('saving as pickle file to', filelocation)
                pd.to_pickle(self, filelocation)



    # Define a function Normalized_gait that takes 'self' (assuming it's a method in a class) and 'A' as arguments
    def Normalized_gait(self, A):
        # Generate an array 'x' with values from 0 to the number of columns in A
        x = np.arange(A.shape[-1])

        # Replace any NaN (Not a Number) values in array A with 0
        A = np.where(np.isnan(A) == 1, 0, A)

        # Interpolate values using cubic interpolation with 101 points
        # Interpolate the data along axis 0 (assuming x is the axis)
        Y = interpolate.interp1d(x, A, kind='cubic')(np.linspace(x.min(), x.max(), 101))

        # Return the interpolated values
        return Y

        # Define a function named ncycle_data that takes an object x as its parameter.
    def ncycle_data(self,x):
        # Create an empty dictionary Ncycle_data within the object x.
        x.Ncycle_data = {}

        # Iterate through each variable in the keys of the data attribute of object x.
        for var in x.data.keys():
            # Create an empty dictionary for each variable within the Ncycle_data dictionary.
            x.Ncycle_data[var] = {}

            # Assign the result of Normalized_gait function applied to the data of the current variable
            # to the corresponding entry in the Ncycle_data dictionary.
            x.Ncycle_data[var] = self.Normalized_gait(x.data[var])

        # Return the modified object x with the newly populated Ncycle_data dictionary.
        return x

    def process_subject_files(self,subject_list, file_list):
    # Iterate through each subject in the subject_list
        for sub in subject_list:
            # Use NumPy to filter file_list based on the presence of the subject in file names
            matching_files = file_list[np.char.find(file_list, sub) > 0]
            # Iterate through the matching files
            for fn in matching_files:
                # Read data from the pickle file using pandas
                x = pd.read_pickle(fn)

                # Apply the ncycle_data function to the data
                x = self.ncycle_data(x)

                # Print a message indicating the file is being saved
                print('saving file to', fn)

                # Save the modified data back to the pickle file
                pd.to_pickle(x, fn)


    def trimdata(self,x, y, Subject, window_size=40, stride=10):
        """
        Trim time series data into fixed-size windows with a specified stride.

        Parameters:
            x (numpy.ndarray): Input feature data of shape (num_samples, num_frames, num_features).
            y (numpy.ndarray): Output label data of shape (num_samples, num_frames, num_labels).
            Subject (numpy.ndarray): Array containing subject information for each sample.
            window_size (int): Size of the sliding window.
            stride (int): Stride between consecutive windows.

        Returns:
            numpy.ndarray, numpy.ndarray, numpy.ndarray: Trimmed feature data, trimmed label data, and corresponding subjects.
        """

        # Get the shape of the input feature data
        A = x.shape

        # Calculate the start and end frames for each window
        start_frame = [i for i in range(0, A[1] - window_size, stride) if i + window_size < A[1]]
        end_frame = [i + window_size for i in start_frame]

        # Initialize variables to store trimmed data
        x_trim = None
        y_trim = None
        nSubject = None

        # Iterate through each window and trim the data
        for i in range(0, len(start_frame)):
            if i == 0:
                # For the first window, directly assign the trimmed data
                x_trim = x[:, start_frame[i]:end_frame[i], :]
                y_trim = y[:, start_frame[i]:end_frame[i], :]
                nSubject = Subject
            else:
                # For subsequent windows, append the trimmed data
                A = x[:, start_frame[i]:end_frame[i], :]
                B = y[:, start_frame[i]:end_frame[i], :]
                x_trim = np.append(x_trim, A, axis=0)
                y_trim = np.append(y_trim, B, axis=0)
                nSubject = np.append(nSubject, Subject)

        # Return the trimmed feature data, trimmed label data, and corresponding subjects
        return x_trim, y_trim, nSubject
