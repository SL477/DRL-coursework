"""Pick a random state to start in"""

# imports
import numpy as np
from .states_and_actions import states

def random_start(given_map: np.array, random_state=None) -> int:
    """Pick a random state to start in which is empty"""
    pos_states = states(given_map)
    
    height = len(given_map)
    width = len(given_map[0])
    
    value_of_s = 1
    num_states = len(pos_states)
    s = -1
    if random_state is None:
        while(value_of_s != 0) :
            s = np.random.randint(0, num_states)
            value_of_s = given_map[s // height, s % width]
    else:
        # this is to make sure the random numbers are random when this is working in parallel
        while value_of_s != 0:
            s = random_state.randint(0, num_states)
            value_of_s = given_map[s // height, s % width]
    return s