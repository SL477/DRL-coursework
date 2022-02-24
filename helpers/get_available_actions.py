# originally from the lab available_actions = np.where(~np.isnan(R[s]))[0]

import numpy as np

def get_available_actions(r_matrix: np.array, current_state: int) -> list:
    """Get the actions available for this state"""
    return np.where(~np.isnan(r_matrix[current_state]))[0]