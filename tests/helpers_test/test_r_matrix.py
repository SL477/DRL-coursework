from helpers.r_matrix import r_matrix
from helpers.map import basic_map
import numpy as np

def test_r_matrix():
    rmat = r_matrix(basic_map())
    assert rmat.shape == (81,81)

    # Check cell 10
    assert len(np.where(~np.isnan(rmat[10]))[0]) == 1

    # Check cell 11
    assert len(np.where(~np.isnan(rmat[11]))[0]) == 2