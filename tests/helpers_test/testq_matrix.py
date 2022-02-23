from helpers.q_matrix import q_matrix
from helpers.map import basic_map
import numpy as np

def test_q_matrix():
    assert q_matrix(basic_map()) == np.zeros(81)