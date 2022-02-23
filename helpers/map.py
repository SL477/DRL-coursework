# This is just to store the maps
# Imports
import numpy as np

def key() -> dict:
    """What the numbers mean"""
    return {
        0: "Empty space",
        1: "A wall",
        2: "A door",
        3: "The primary goal (the reactor control panel)",
        4: "The secondary goal (the escape route)",
        5: "The agent"
    }

def basic_map() -> np.array:
    """This is the basic game map"""
    return np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 4, 2, 0, 0, 0, 2, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 2, 1, 1, 1, 2, 1, 2, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 3, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ])

if __name__ == "__main__":
    print(basic_map())