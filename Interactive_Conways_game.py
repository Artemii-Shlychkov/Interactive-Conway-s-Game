import importlib
import matplotlib.pyplot as plt
import numpy as np
import pygame
import sys
import time
from datetime import datetime
from screeninfo import get_monitors

import Objects
import board_script

"""
Interactive implementation of Conway's game of life using Pygame.
Make sure to have the following libraries installed (you can install them using requirements.txt):
- numpy
- pygame
- matplotlib
- sys
- datetime
- screeninfo
- importlib
Also (albeit optionally) install the following fonts (or have the font files in the same directory as this file):
- Minecraft, which can be found e.g. at: https://www.dafont.com/minecraft.font
Make sure to have the following files in the same directory as this file:
- glider_gun_script.py
- pulsar_script.py
- soba_script_converted.py
- board_script.py
- bar_oscillator_script.py
- Objects.py
Set up the screen resolution as desired in line 55 as ( , ) or leave it as None.
The game will prompt the user if they want to run the game in full screen mode.
Playing field or Board is the region where the cells will be displayed and the game happens.
Board and cell size are calculated based on the screen resolution.
White cells are alive and black cells are dead.
User can interact with the game by clicking the left mouse button to bring cells to life and the right mouse button 
to kill cells.
The game can be restarted by clicking the 'Restart' button in the menu.
The board can be cleared by clicking the 'Clear' button in the menu.
The user can draw a bar oscillator by clicking the 'Oscillator' button in the menu.
The user can draw a glider gun by clicking the 'Draw gun' button in the menu.
The user can draw a pulsar by clicking the 'Pulsar' button in the menu.
The user can draw a spaceship by clicking the 'Spaceship' button in the menu.
The user can take a screenshot of the game by clicking the 'Screenshot' button in the menu. The screenshot will be 
saved in the same directory as this file. Additionally, a plot of the current board state will be saved in the same
directory as this file.
The user can pause updating the board. At this point user can safely add living cells or whole patterns to the board
The user can exit the game by clicking the 'Exit' button in the menu or pressing esc button on the keyboard. A dialog 
box will appear to confirm if the user wants to exit the game.
The game will be closed if the 'x' button is clicked.
See more documentation in the Juptyer notebook.
"""

# FOR USER INPUT #
user_screen = None # your screen resolution

# WELCOME SCREEN #
full_screen = Objects.welcome_screen()


# GAME SETTINGS #

# Screen settings
def get_primary_resolution():
    primary_monitor = get_monitors()[0]  # Assuming the primary monitor is the first one in the list
    resolution = (primary_monitor.width, primary_monitor.height)
    print(f"Primary monitor resolution: {resolution}")
    return resolution


if user_screen is None:
    user_screen = get_primary_resolution()

SCREEN_X, SCREEN_Y = user_screen  # your screen resolution
WIDTH, HEIGHT = SCREEN_X // 1, SCREEN_Y // 1  # be aware of monitor scaling on windows (150%)

# Colors

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

prompts_list = ["Press 'esc' to close the game", "Press LMB to bring cells to life", "Press RMB to kill cells",
                "Press 's' to take a screenshot",
                "Press 'P' to pause the game"]  # List of prompts to be displayed on the screen

# parameter that controls the running of the game
running = True

# Size of the cell in the game
cell_size = HEIGHT // 120

# Size and zero coordinates of the board
length = 100 * cell_size
zero_x = (WIDTH - length) // 2
zero_y = (HEIGHT - length) // 2

# list to store the board states
board_list = []

# Initialize Pygame
pygame.init()

# initialize the screen in pygame
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN if full_screen else 0)
pygame.display.set_caption("Conway's Game")

# initialize the clock
clock = pygame.time.Clock()

# Initialize the board
x, y = length // cell_size, length // cell_size  # size of the board
states, counts = 0, 1

# load the board from the board_script.py

latest_click_time = 0


# GAME FUNCTIONS #

# restart the game of life by generating a new board

class Game:
    def __init__(self):
        self.running = True
        self.cell_size = HEIGHT // 120
        self.length = 100 * self.cell_size
        self.zero_x = (WIDTH - self.length) // 2
        self.zero_y = (HEIGHT - self.length) // 2
        self.x, self.y = self.length // self.cell_size, self.length // self.cell_size
        self.board = None

        self.LMB = False
        self.RMB = False

        self.Menu = {'Restart': [None, False],
                     'Clear': [None, False],
                     'Oscillator': [None, False, "bar_oscillator_script"],
                     'Glider gun': [None, False, "glider_gun_script"],
                     'Pulsar': [None, False, "pulsar_script"],
                     'Spaceship': [None, False, "soba_script"],
                     'Screenshot': [None, False],
                     'Play / Pause': [None, False],
                     'Exit': [None, False],
                     }

        pass

    def restart(self):
        """
        Restart the game of life by generating a new board.
        """

        if self.Menu['Restart'][1]:  # Check if the restart state in Menu dictionary is True
            print('restarting')
            self.board = board_script.create_board(x, y)
            self.Menu['Restart'][1] = False  # Set the restart state to False

    # clear the board by setting all cells to 0

    def clear(self):
        """
        Clear the board by setting all cells to 0.
        """

        if self.Menu['Clear'][1]:  # Check if the clear state in Menu dictionary is True
            print('clearing')
            self.board = np.zeros((x, y, 2), dtype=int)
            self.Menu['Clear'][1] = False  # Set the clear state to False

    # update the board state based on the number of neighbours

    def update(self):
        """
        Update the board state given the number of neighbors.
        """
        # Count the neighbours
        self.board[:, :, counts] = np.zeros((x, y), dtype=int)
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                if di != 0 or dj != 0:
                    self.board[1:x - 1, 1:y - 1, counts] += self.board[1 + di:x - 1 + di, 1 + dj:y - 1 + dj, states]
        time.sleep(0.1)  # to slow down the game

        # Update states based on number of neighbours
        self.board[np.where(self.board[1:x - 1, 1:y - 1, counts] > 3)[0] + 1,
                   np.where(self.board[1:x - 1, 1:y - 1, counts] > 3)[
                       1] + 1, states] = 0

        self.board[np.where(self.board[1:x - 1, 1:y - 1, counts] < 2)[0] + 1,
                   np.where(self.board[1:x - 1, 1:y - 1, counts] < 2)[
                       1] + 1, states] = 0

        self.board[np.where(self.board[1:x - 1, 1:y - 1, counts] == 3)[0] + 1,
                   np.where(self.board[1:x - 1, 1:y - 1, counts] == 3)[
                       1] + 1, states] = 1

    # bring cells to life or kill them by clicking the mouse

    def mouse_click(self):
        """
        Bring cells to life or kill them by clicking the mouse within the board
        """
        # Get the position of the mouse
        pos = pygame.mouse.get_pos()

        # get the corresponding cell coordinates in the board
        x, y = pos
        x = (x - zero_x) // cell_size
        y = (y - zero_y) // cell_size

        if border.collidepoint(pos):  # Check if the mouse is within the board
            if pygame.mouse.get_pressed()[0]:  # Check if the left mouse button is pressed
                self.board[x, y, states] = 1  # Bring the cell to life
            if pygame.mouse.get_pressed()[2]:  # Check if the right mouse button is pressed
                self.board[x, y, states] = 0  # Kill the cell

    # draw a red rectangle around the cell the cursor is currently on

    def cursor(self):
        """
        Draw a red rectangle around the cell the cursor is currently on.
        """
        pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, RED, (pos[0], pos[1], self.cell_size, self.cell_size), self.cell_size)

    # take a screenshot of the game

    def take_screenshot(self):
        """Take a screenshot of the game.
        The screenshot will be saved in the same directory as this file.
        Additionally, a plot of the current board state will be
        saved in the same directory as this file.
        """
        if self.Menu['Screenshot'][1]:  # Check if the screenshot state is True
            filename = f'game_of_life_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
            pygame.image.save(screen, filename)
            fig, ax = plt.subplots()
            plt.imshow(self.board[:, :, states], cmap='gray')
            ax.set_xticks([])
            ax.set_yticks([])
            plt.savefig(f'plot_{filename}')
            self.Menu['Screenshot'][1] = False

    # display a dialog box to confirm if the user wants to exit the game

    def exit_diag(self):
        """Display a dialog box to confirm if the user wants to exit the game.
        The dialog box is displayed when the Menu['Exit'][1] state is True.
        """

        if self.Menu['Exit'][1]:  # Check if the exit_window state is True
            dialog_box = Objects.Objects(text_color="BLACK")  # load the dialog box class from the archive_objects.py

            # Call the dialog box method to display the dialog box and get the yes and no buttons
            yes, no = dialog_box.dialog_box(screen, 'Do you really want to quit?')

            if dialog_box.is_clicked(yes, self.LMB):  # Call the is_clicked method to check if the yes button is clicked
                self.running = False
            if dialog_box.is_clicked(no, self.LMB):
                self.Menu['Exit'][1] = False

    # convert the pattern string to a numpy array

    def pattern_from_str(self, pattern_str):
        """
        Convert the pattern string to a numpy array.
        Args:
            pattern_str (str): the pattern string
        Returns:
            pattern_array (numpy.ndarray): the pattern as a numpy array
        """
        # Split the pattern string into lines and remove empty lines
        pattern_lines = pattern_str.strip().split('\n')
        for i in range(len(pattern_lines)):
            pattern_lines[i] = pattern_lines[i].strip()  # Remove leading and trailing whitespaces in each line
        # Determine the size of the pattern
        rows = len(pattern_lines)
        cols = len(pattern_lines[0])

        # Create a numpy array to store the pattern
        pattern_array = np.zeros((rows, cols), dtype=int)

        # Convert the pattern string to a numpy array
        for i, line in enumerate(pattern_lines):  # Loop through the pattern lines
            for j, char in enumerate(line):  # Loop through the characters in the line
                if char == 'O':  # Check if the character is 'O'
                    pattern_array[i, j] = 1  # Set the corresponding element in the numpy array to 1

        return np.rot90(pattern_array)

    # draw the pattern on the board

    def draw_pattern(self):
        """
        Checks if any pattern was selected from the menu and draws it.
        The pattern is drawn by calling the create_pattern function from the corresponding script.
        The pattern is displayed near the mouse position and can be placed on the playing field by clicking the left mouse
        button within the playing field.
        The choice can be undone by clicking the right mouse button.
        The pattern is placed on the board when the left mouse button is clicked within the board borders.
        """
        restricted = ['Clear', 'Restart', 'Exit', 'Screenshot',
                      'Play / Pause']  # List of commands that are not patterns
        for key in self.Menu.keys():  # Loop through the Menu dictionary keys
            if self.Menu[key][
                1] and key not in restricted:  # Check if any pattern is selected (i.e. second element in the list is True)
                script = importlib.import_module(self.Menu[key][
                                                     2])  # import the corresponding script from the Menu dictionary (using the third element in the list)

                pattern = script.create_pattern()  # Call the create_pattern function from the script

                # Check if the pattern is given as string lines
                if type(pattern) == str:
                    pattern = self.pattern_from_str(pattern)  # convert the pattern string to a numpy array

                # Display the pattern mockup near the mouse position
                pos = pygame.mouse.get_pos()
                for i in range(0, len(pattern)):
                    for j in range(0, len(pattern[0])):
                        if pattern[i][j] == 1:
                            pygame.draw.rect(screen, WHITE,
                                             (pos[0] + i * cell_size, pos[1] - j * self.cell_size, self.cell_size,
                                              self.cell_size))

                undo_prompt = Objects.Objects(text_color="RED",
                                              font_size=24)  # load the undo prompt class from the archive_objects.py with specific options
                undo_prompt.draw_text_box(screen, "Press RMB to undo your choice. Press LMB to place the pattern",
                                          WIDTH // 2, HEIGHT - 50, align='center',
                                          frame_width=-1)  # Display the undo prompt
                # Place the pattern on the board
                if border.collidepoint(pygame.mouse.get_pos()):  # Check if the mouse is within the board
                    if self.LMB:  # Check if the left mouse button is pressed

                        # convert the mouse position to the board coordinates
                        x, y = pos
                        x = (x - zero_x) // cell_size
                        y = (y - zero_y) // cell_size

                        # place the pattern on the board
                        for i in range(0, len(pattern)):
                            for j in range(0, len(pattern[0])):
                                self.board[x + i, y - j, states] = pattern[i][j]

                if self.RMB:  # Check if the right mouse button is pressed
                    self.Menu[key][1] = False  # Undo the choice

    def change_state(self, key, dict):
        """
        Changes state of the dictionary entry
        Args:
            key (str): key in the dictionary
            dict: name of the dictionary
        Returns:
            changed value
        """
        dict[key][1] = not dict[key][1]

    def paused(self):
        if self.Menu['Play / Pause'][1]:
            pause_prompt = Objects.Objects(text_color="RED",
                                           font_size=36)  # load the undo prompt class from the archive_objects.py with specific options
            pause_prompt.draw_text_box(screen, 'Game paused', (WIDTH - length) // 4, HEIGHT // 4, frame_width=-1)


# MAIN LOOP
menu_button = Objects.Objects(obj_color="WHITE", text_color="WHITE",
                              font_size=24)  # load the buttons class from the Objects.py with specific options
header = Objects.Objects(text_color='WHITE',
                         font_size=48)  # load the header class from the Objects.py with specific options
prompts = Objects.Objects(text_color="WHITE",
                          font_size=24)  # load the prompts class from the archive_objects.py with specific options

game = Game()
game.board = board_script.create_board(x, y)
while game.running:
    game.LMB, game.RMB = False, False
    screen.fill(BLACK)  # Fill the screen with black
    pygame.mouse.set_visible(False)  # Hide the mouse cursor
    border = pygame.draw.rect(screen, RED, (zero_x, zero_y, length, length), 2)  # Draw the borders
    header.draw_text_box(screen, "Conway's game of life", x=WIDTH // 2, y=50, frame_width=-1)  # Draw the title

    ## Core game functions ##
    # Plot the cells
    for k in range(1, x - 1):
        for j in range(1, y - 1):
            if game.board[k, j, states] == 1:
                pygame.draw.rect(screen, WHITE,
                                 (zero_x + k * cell_size, zero_y + j * game.cell_size, game.cell_size, game.cell_size))

    game.mouse_click()  # Bring cells to life or kill them by clicking the mouse

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Close the game by clicking the 'x' button
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                game.Menu['Screenshot'][1] = True  # Call the state_screenshot function from the Menu dictionary
            if event.key == pygame.K_ESCAPE:  # Press 'esc' to exit the game
                if not game.Menu['Exit'][1]:
                    game.Menu['Exit'][1] = True  # Call the exit function from the Menu dictionary
                else:
                    game.Menu['Exit'][1] = False
            if event.key == pygame.K_p:
                game.change_state('Play / Pause', game.Menu)
        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:
                game.LMB = True
            if event.button == 3:
                game.RMB = True

    ## Create Menu ##
    for i, key in enumerate(reversed(game.Menu.keys())):  # Loop through the Menu dictionary keys in reverse order

        # Draw the buttons by calling the render method from the buttons class from down to up
        game.Menu[key][0] = menu_button.draw_text_box(screen, key, (WIDTH - length) // 4,
                                                      (zero_y + length) - menu_button.font_size * 3 * i - 20)

        # Check if the button is clicked and no other button was clicked (except Play / Pause)

        if menu_button.is_clicked(game.Menu[key][0], game.LMB) and not any(
                game.Menu[entry][1] for entry in game.Menu.keys()
                if entry != key and entry != 'Play / Pause' and key != 'Exit'):
            game.change_state(key, game.Menu)

    # update the board
    if not game.Menu['Play / Pause'][1]:
        game.update()  # Update the board

    # menu functions
    game.draw_pattern()
    game.clear()
    game.restart()

    # Display the prompts
    for i, prompt in enumerate(prompts_list):  # Loop through the list of prompts
        prompts.draw_text_box(screen, prompt, (zero_x + length) + 10, HEIGHT // 2 + prompts.font_size * 2 * i,
                              align='bottomleft', frame_width=-1)  # Draw the prompts
    game.paused()
    game.exit_diag()  # Display the dialog box to confirm if the user wants to exit the game
    game.cursor()  # Draw a red rectangle around the cell the cursor is currently on
    game.take_screenshot()  # Take a screenshot if the state is True (i.e. if the 'Screenshot' button is clicked)

    pygame.display.flip()  # Update the display
    clock.tick(144)  # Set the frame rate to 144

print('game exited normally')
pygame.quit()  # Quit the game

sys.exit()
