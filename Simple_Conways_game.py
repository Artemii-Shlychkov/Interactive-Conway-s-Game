import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import glider_gun_script
"""
This is a simple implementation of the Conway's game of life.
The board is a 3D numpy array with the following shape: (x, y, 2). The first two dimensions represent the board's size 
and the third dimension stores the current state and the neighbours count. The state is stored in the first layer and the
neighbours count is stored in the second layer. The state of a cell can be either 0 (dead) or 1 (alive). The neighbours
count is an integer that represents the number of alive cells around a given cell.
The board can be initialized with random values, with 80% of the cells being dead and 20% being alive. This proportion can be
changed by modifying the p parameter in the np.random.choice function. The cells on the edges of the board are initialized
as dead. 
The board can also be initialized with patternd by calling the corresponding function from the pattern scripts.
Pattern scripts must be imported first.
The cells on the edges of the board are initialized as dead. The function create_board receives two parameters, x and y,
which represent the size of the board.
The game is displayed using endless matplotlib FuncAnimation. The update function is called at each frame to update the board's
state and display the new state.

"""

option = int(input("Enter the pattern you want to use: \n1. Random Board\n 2. Glider Gun\n3. Pulsar\n4.Oscillator\n" ))


# Initialize the board
x, y = 100, 100

states, counts = 0, 1

board = np.zeros((x, y, 2), dtype=int)



if option == 2:
    pattern = glider_gun_script.create_pattern()
    #print (np.shape(pattern)[1])
    board[50:50+np.shape(pattern)[0],50:50+np.shape(pattern)[1],states] = pattern[:,:,0]



    """
    for i in range(0,np.shape(pattern)[0]):
        for j in range(0,np.shape(pattern)[1]):
            board[i+50,j+50,states] = pattern[i,j]
    """

elif option == 1:
    board[:, :, states] = np.random.choice([0, 1], size=(x, y), p=[0.8, 0.2])

    board[0, :, states] = 0
    board[x - 1, :, states] = 0
    board[:, 0, states] = 0
    board[:, y - 1, states] = 0


# Function to update the board state
def update(frame):
    ax.clear()
    # Compute counts
    board[:,:,counts] = np.zeros((x,y),dtype=int)
    for di in [-1,0,1]:
        for dj in [-1,0,1]:
            if di != 0 or dj != 0:
                board[1:x-1,1:y-1,counts] += board[1+di:x-1+di,1+dj:y-1+dj,states]
    """
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            board[i, j, counts] = np.sum(board[i - 1:i + 2, j - 1:j + 2, states]) - board[i, j, states]
    # Update states based on counts
    """


    board[np.where(board[1:x-1,1:y-1,counts] > 3)[0]+1,np.where(board[1:x-1,1:y-1,counts] > 3)[1]+1,states] = 0

    board[np.where(board[1:x-1,1:y-1,counts] < 2)[0]+1,np.where(board[1:x-1,1:y-1,counts] < 2)[1]+1,states] = 0

    board[np.where(board[1:x-1,1:y-1,counts] == 3)[0]+1,np.where(board[1:x-1,1:y-1,counts] == 3)[1]+1,states] = 1


    """
    for i in range(1, x - 1):
        for j in range(1, y - 1):
            if board[i, j, counts] == 3:
                board[i, j, states] = 1
            elif board[i, j, counts] < 2 or board[i, j, counts] > 3:
                board[i, j, states] = 0
            elif board[i, j, counts] == 2:
                board[i, j, states] = board[i, j, states]
    """
    # Plot the board
    ax.imshow(board[:, :, states], cmap='gray', origin='upper')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f'Time = {frame}')
fig, ax = plt.subplots()
ani = FuncAnimation(fig, update, frames=None, repeat=False)

plt.show()



