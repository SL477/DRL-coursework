# Here we take the map from map and transform it from a 9 by 9 matrix 
# into an 81 length array

# imports
import numpy as np

def states(map: np.array) -> list:
    """Return the states from a map"""
    len_rows = len(map)
    if len_rows > 0:
        len_cols = len(map[0])
        return [x for x in range(len_rows * len_cols)]
    else:
        return []
