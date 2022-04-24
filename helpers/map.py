# This is just to store the maps
# Imports
import numpy as np
import os.path

def key(advanced=False) -> dict:
    """What the numbers mean. More for informational purposes than anything else."""
    return {
        0: {'desc': "Empty space", 'reward': 0, 'solid': False},
        1: {'desc': "A wall", 'reward': 0, 'solid': True},
        2: {'desc': "A door", 'reward': 0, 'solid': False},
        3: {'desc': "The primary goal (the reactor control panel)", 'reward': 1000 if advanced else 50, 'solid': False},
        4: {'desc': "The secondary goal (the escape route)", 'reward': 500 if advanced else 30, 'solid': False},
        5: {'desc': "The agent", 'reward': 0, 'solid': False},
        6: {'desc': "A trap", 'reward': -10, 'solid': False},
        7: {'desc': "An enemy which bobs up and down", 'reward': -10, 'solid': True},
        8: {'desc': 'An enemy which bobs side to side', 'reward': -10, 'solid': True}
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

    #return np.genfromtxt("helpers/AdvancedMap.csv", delimiter = ",")
    pth = os.path.abspath(os.path.dirname(__file__)) # from https://stackoverflow.com/questions/40416072/reading-file-using-relative-path-in-python-project
    pth = os.path.join(pth, "AdvancedMap.csv")
    return np.genfromtxt(pth, delimiter=',')

if __name__ == "__main__":
    #print(basic_map())
    print(adv_map())