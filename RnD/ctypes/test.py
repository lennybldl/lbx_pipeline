# optimize_with_ctypes.py

import ctypes

# Load the shared library
lib = ctypes.CDLL("./sum_of_squares.so")

# Define the function prototype
lib.sum_of_squares.argtypes = (ctypes.POINTER(ctypes.c_double), ctypes.c_int)
lib.sum_of_squares.restype = ctypes.c_double


def sum_of_squares(numbers):
    # Convert the Python list to a C array
    num_array = (ctypes.c_double * len(numbers))(*numbers)
    # Call the C function
    result = lib.sum_of_squares(num_array, len(numbers))
    return result


# Test the optimized function
numbers = [1, 2, 3, 4, 5]
print("Sum of squares:", sum_of_squares(numbers))
