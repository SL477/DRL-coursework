# originally from the lab available_actions = np.where(~np.isnan(R[s]))[0]

import numpy as np
from collections import namedtuple

Action = namedtuple("Action", ["index", "x", "y", "shoot"])

def get_available_actions(r_matrix: np.array, current_state: int) -> list:
    """Get the actions available for this state"""
    return np.where(~np.isnan(r_matrix[current_state]))[0]

def adv_actions():
    """This is for the advanced map. left, right, up, down, fire gun"""
    
    return {name: Action(idx, x, y, shoot) for name, idx, x, y, shoot in [
        ('left', 0, -1, 0, False),
        ('right', 1, 1, 0, False),
        ('up', 2, 0, -1, False),
        ('down', 3, 0, 1, False),
        ('shoot', 4, 0, 0, True) # handle this one somewhere else, any enemy in the neighbouring cells are destroyed
    ]}

if __name__ == "__main__":
    print(adv_actions())