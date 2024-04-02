# Interactive-Conway-s-Game

## Description

The Conway’s Game of Life is a classic example of cellular automaton devised by mathematician John Conway in 1970. It’s a zero-player game, meaning its evolution is determined by its initial state, requiring no further input. The game is played on a two-dimensional grid where each cell can be either alive or dead. The state of each cell evolves over discrete time steps based on simple rules:
1. Any live cell with fewer than two live neighbors dies, as if by underpopulation.
2. Any live cell with two or three live neighbors lives on to the next generation.
3. Any live cell with more than three live neighbors dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbors becomes a live cell, as if by reproduction.
These rules create complex patterns from simple initial configurations. The game has found ap- plications in various fields such as computer science, biology, and even art due to its emergent properties and ability to model complex systems.
## Package contents Main file:
• Interactive_Conways_game.py
Supplementary scripts:
• Objects.py

• glider_gun_script.py

• pulsar_script.py

• board_script.py

• bar_oscillator_script.py

• soba_script.py 
## Other files: 
• requirements.txt

• Minecraft.ttf

See further description in text below
## Prerequisites
First of all, necessary libraries need to be installed. This can be done from requirments.txt (running pip install -r requirements.txt). Make sure to have the following libraries installed: 
- numpy
- pygame
- matplotlib
- sys 
- datetime 
- screeninfo
- importlib
Also (albeit optionally) install the following fonts (or have the font files in the same directory as this file): - Minecraft, which can be found e.g. at: https://www.dafont.com/minecraft.font
## Program overview
The core of the program is a 2D playing field, called ‘board’, which consists of black and white squares: white ones denote living cells and the black ones represent dead cells. The board is coded as a 3D numpy array with the following shape: (x, y, 2). The first two dimensions represent the board’s size and the third dimension stores the current state and the neighbours count. The state is stored in the first layer and the neighbours count is stored in the second layer. The state of a cell can be either 0 (dead) or 1 (alive). The neighbours count is an integer that represents the number of alive cells around a given cell. When the board is initialized with random values, with 80% of the cells being dead and 20% being alive. This proportion can be changed by modifying the p parameter in the np.random.choice function. The cells on the edges of the board are initialized as dead (boundary condition). The function create_board() receives two parameters, x and y, which represent the size of the board. Size in the pygame build is determined given the screen resolution or manually.


## Interactive Conway’s Game
The build consits of several files. Main program is represented by Interac- tive_Conways_game.py file. Additionally there is a supplementary file, called Objects.py, which contains classes and functions, needed to build interactive in-game menu, dialog boxes, prompts and so on. Finally, there are several scripts, containing numpy arrays or strings, which initialize the board randomly as well as some interesting patterns of the Conway’s game, namely: Bar oscillator, Glider gun, Pulsar, Soba Spaceship and so on. The scripts are named correspondingly. In the main file user may adjust the user_screen variable according to his/her screen resolution or leave it as None – then the program will detect the resolution automatically. Then the program will promt a user to choose if he/she wants to run the program in full screen or absolutely ruin the ultimate gaming experience by running the program in the window mode. Albeit, make sure to reserve at least 1450 pixels for width, or reduce the prompts font size in the code, as the prompts will not fit the screen and the corresponding error will popup.

Based on the resolution, the program will create an appropriate playing field with red boundaries, initialize the board randomly the same way as above, but from a separate board_script.py script, display the cursor as a red dot, the interactive menu on the left-hand side and some prompts on the right-hand side
Main screen of the game below:
Menu and prompts are quite self-explanatory. User can interact with the game by clicking the left mouse button to bring cells to life and the right mouse button to kill cells within the playing field.

Note, that attempting to place a cell in dead space if the game is not paused will not yield any visible effect as it will die straight away, however placing another cell adjacent to static patterns can produce interesting effects. Menu options: 
1. The game can be restarted by clicking the ‘Restart’ button in the menu.
2. The board can be cleared by clicking the ‘Clear’ button in the menu. Clearing the playing field is recommended if user wants to try out the patterns below.
3. The user can draw a bar oscillator by clicking the ‘Oscillator’ button in the menu.
4. The user can draw a glider gun by clicking the ‘Draw gun’ button in the menu.
5. The user can draw a pulsar by clicking the ‘Pulsar’ button in the menu.
6. The user can draw a spaceship by clicking the ‘Spaceship’ button in the menu
7. The user can take a screenshot of the game by clicking the ‘Screenshot’ button in the menu. The screenshot will be saved in the same directory as this file. Additionally, an imshow matplotlib plot of the current board state will be saved in the same directory as this file.
8. The user can pause updating the board. At this point user can safely add living cells or whole patterns to the board
9. The user can exit the game by clicking the ‘Exit’ button in the menu or pressing esc button on the keyboard. A dialog box will appear to confirm if the user wants to exit the game.
The game will also be closed if the ‘x’ button is clicked.
When choosing the patterns, their mockup will be drawn at the cursor position and placed in playing field once LMB is clicked within its boundaries

These interesting patterns are initialized in supplementary scripts. In order to use more patterns in the game one would implement the following two easy steps: 
1. create such a script file with an initialization of the corresponding pattern. The pattern can be given as strings of dots and 0 (i.e. taken from https://conwaylife.com/wiki/, see example below) or in form of a numpy array itself. The script must contain the function create_pattern() which will return the pattern (str or np.array). If the pattern is str, the pattern_from_str() function of the main program will convert it to an array anyway.
2. add an additional entry in the Menu dictionary, analogous to other patterns.
After that the option should display in the menu in the game and be able to load just like other patterns.

The Menu dictionary. First element of the list for each key is used to render the corresponding button on the display and is set to None by default. The second entry defines if the button is clicked (and therefore remains clicked, until its function is done or selection is undone by RMB). The third entry contains the name of the corresponding script (where applicable) and should be accurate.

Please see the README.pdf file if further interested

