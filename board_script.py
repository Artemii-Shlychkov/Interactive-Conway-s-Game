import numpy as np
"""
This script is used to create a random board for the Conway's game of life.
The board is a 3D numpy array with the following shape: (x, y, 2). The first two dimensions represent the board's size 
and the third dimension stores the current state and the neighbours count. The state is stored in the first layer and the
neighbours count is stored in the second layer. The state of a cell can be either 0 (dead) or 1 (alive). The neighbours
count is an integer that represents the number of alive cells around a given cell.
The board is initialized with random values, with 80% of the cells being dead and 20% being alive. This proportion can be
changed by modifying the p parameter in the np.random.choice function. The cells on the edges of the board are initialized
as dead. 
The cells on the edges of the board are initialized as dead. The function create_board receives two parameters, x and y,
which represent the size of the board. Size is determined in the main program given the screen resolution.
The function returns the initialized board and is used in the main program to create the initial state of the game.
"""

def create_board(x,y):
    """
    Function to create a random board for the Conway's game of life.
    Args:
        x (int): the width of the board
        y (int): the height of the board
    Returns:
        board (numpy.ndarray): the initialized board
    """

    states = 0
    counts = 1
    board = np.zeros((x, y, 2), dtype=int)
    board[:,:,states] = np.random.choice([0, 1], size=(x, y), p=[0.8, 0.2])
    board[0,:,states] = 0
    board[x-1,:,states] = 0
    board[:,0,states] = 0
    board[:,y-1,states] = 0
    return board