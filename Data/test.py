import pandas as pd
import numpy as np
import random
import string
import pickle

# Function to generate random strings
def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

# Function to generate a random DataFrame
def generate_random_dataframe(rows, cols):
    data = {}
    for col in range(cols):
        col_name = 'Column_' + str(col)
        data[col_name] = [generate_random_string(5) for _ in range(rows)]
    return pd.DataFrame(data)

# Generating random DataFrames
num_dataframes = 3
rows = 5
cols = 4
dataframes = [generate_random_dataframe(rows, cols) for _ in range(num_dataframes)]

# Saving DataFrames to pickle file
pickle_file = 'W:/dataPi-2afc/random_allTrialsDF'
with open(pickle_file, 'wb') as f:
    pickle.dump(dataframes, f)

print(f"Random DataFrames saved to '{pickle_file}'")