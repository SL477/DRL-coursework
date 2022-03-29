# This is just to store the maps
# Imports
import numpy as np

def key() -> dict:
    """What the numbers mean. More for informational purposes than anything else."""
    return {
        0: {'desc': "Empty space", 'reward': 0},
        1: {'desc': "A wall", 'reward': 0},
        2: {'desc': "A door", 'reward': 0},
        3: {'desc': "The primary goal (the reactor control panel)", 'reward': 50},
        4: {'desc': "The secondary goal (the escape route)", 'reward': 30},
        5: {'desc': "The agent", 'reward': 0},
        6: {'desc': "A trap", 'reward': -10},
        7: {'desc': "An enemy which bobs up and down", 'reward': -10},
        8: {'desc': 'An enemy which bobs side to side', 'reward': -10}
    }

def basic_map() -> np.array:
    """This is the basic game map"""
    return np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 4, 2, 0, 0, 0, 2, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 6, 0, 0, 0, 6, 0, 1],
        [1, 2, 1, 1, 1, 2, 1, 2, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 3, 0, 0, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ])

def adv_map() -> np.array:
    """Get the advanced map"""
    # reads the Advanced map csv file and converts it into a numpy array (I found the function from stackoverflow, but used numpy's 'help' to grab the delimiter)
    return np.genfromtxt("helpers/AdvancedMap.csv", delimiter = ",")

if __name__ == "__main__":
    #print(basic_map())
    print(adv_map())