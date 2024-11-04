import numpy as np

ini_array = np.array([[1, 2, 3], [45, 4, 7], [9, 6, 10]])

# printing initial array
print("initial_array : ", str(ini_array));

# Array to be added as row
row_to_be_added = np.array([1, 2, 3])

# Adding row to numpy array
result = np.r_[ini_array, [row_to_be_added]]

# printing result
print("resultant array", str(result))