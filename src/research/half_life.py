import numpy as np

def calculate_half_life(theta: float):
    """
    Half-life of mean reversion.
    """
    return np.log(2) / theta
