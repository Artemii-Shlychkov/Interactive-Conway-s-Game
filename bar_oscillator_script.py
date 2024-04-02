import numpy as np
import matplotlib.pyplot as plt

"""
This script is used to create a simple bar oscillator pattern for the Conway's game of life.
The board is a 3D numpy array with the following shape: (x, y, 1). The first two dimensions represent the region 
where the gun is drawn and the third dimension stores the state (alife or dead).
The function returns the glider gun and is used in the main program upon calling the draw_pattern function.
The function must be called "create_pattern" and must return the array with the pattern in order to be used.
"""

def create_pattern():
    bar = np.zeros((7,7,1))
    bar[2:5,3,0] = 1
    return bar

