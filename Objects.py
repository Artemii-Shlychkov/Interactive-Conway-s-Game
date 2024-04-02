import sys

import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)


class Objects:
    def __init__(self, font=None, font_size=None, text_color=None, obj_color=None):
        """
        Class to create text boxes objects in pygame
        Args:
            font (None or str): the font to be used in the text object. Default is 'Minecraft.ttf'
            font_size (None or int): the size of the font. Default is 30
            text_color (None or str): the color of the text. Default is white
            obj_color (None or str): the color of the text box frames. Default is black
        Attributes:
            font (pygame.font.Font): the font object. Default is 'Minecraft.ttf'
            font_size (int): the size of the font. Default is 30
            text_color (tuple): the color of the text. Default is white
            obj_color (tuple): the color of the text box frames. Default is black
        """

        colors = {'BLACK': (0, 0, 0),
                  'RED': (255, 0, 0),
                  'GREEN': (0, 255, 0),
                  'BLUE': (0, 0, 255),
                  'GRAY': (200, 200, 200),
                  'WHITE': (255, 255, 255)}

        self.font_size = 30 if font_size is None else font_size  # Default font size

        self.default_font = "Minecraft.ttf"  # Default font

        # Try to load the font, if it fails, use the default font
        try:
            self.font = pygame.font.Font(self.default_font, self.font_size) if font is None else pygame.font.SysFont(
                font, self.font_size)
        except:
            print('Font not found. Using default font')
            self.font = pygame.font.SysFont("Minecraft", self.font_size)

        self.obj_color = BLACK if obj_color is None else colors[obj_color]  # Default color of the text box frames
        self.text_color = WHITE if text_color is None else colors[text_color]  # Default color of the text
        self.inf_coeff = 20  # Coefficient to inflate the text box

    def draw_text_box(self, screen, text, x, y, align=None, frame_width=3):

        """
        Function to draw a text box in pygame
        Args:
            screen (pygame.Surface): the screen object
            text (str): the text to be displayed
            x (int): the x coordinate of the text box
            y (int): the y coordinate of the text box
            align (None or str): the alignment of the text box
            frame_width (int): the width of the text box frame; set to -1 to remove the frame, set to 0 to fill the text box
        Returns:
            frame (pygame.Rect): the rectangle object of the text box
        """

        pos = pygame.mouse.get_pos()
        text = self.font.render(text, True, self.text_color)  # Render the text
        text_box = text.get_rect(center=(x, y))  # Get the rectangle object of the text

        # Alignment the text box
        if align == 'center' or align is None:  # Default alignment
            text_box.center = x, y
        if align == 'bottomleft':
            text_box.bottomleft = x, y
        if align == 'bottomright':
            text_box.bottomright = x, y
        if align == 'midbottom':
            text_box.midbottom = x, y

        frame = text_box.inflate(self.inf_coeff, self.inf_coeff)  # Create the text box frame
        frame.center = text_box.center  # Center the text box frame

        if frame.collidepoint(pos):
            pygame.draw.rect(screen, RED, frame, frame_width, )  # Draw the text box frame

        else:
            pygame.draw.rect(screen, self.obj_color, frame, frame_width)  # Draw the text box frame
        screen.blit(text, text_box)  # Display the text

        # Check if the text box fits inside the screen

        if not self.check_inside_screen(frame):
            warning = Objects(text_color='BLACK')
            OK = warning.dialog_box(screen,
                                    'Some text objects are outside the screen. Try setting lower font or higher resolution',
                                    num_options=1)  # Display a warning dialog box
            if self.is_clicked(OK,pygame.mouse.get_pressed()[0]):  # Check if the OK button is clicked
                sys.exit()  # Exit the program

        return frame  # Return the rectangle object of the text box (needed for the is_clicked function)

    def dialog_box(self, screen, text, num_options=None):
        """
        Function to create a dialog box in pygame
        Args:
            screen (pygame.Surface): the screen object
            text (str): the text to be displayed
            num_options (None or int): the number of options in the dialog box
        Returns:
            option_1 (pygame.Rect): the rectangle object of the first option
            option_2 (pygame.Rect): the rectangle object of the second option
        """

        prompt = self.font.render(text, True, self.text_color)  # Render the text
        screen_width, screen_height = pygame.display.get_surface().get_size()  # Get the screen size
        prompt_box = prompt.get_rect(
            center=(screen_width // 2, screen_height // 2))  # Get the rectangle object of the text
        dialog_frame = prompt_box.inflate(50, 100)  # Create the dialog box frame

        # Align the prompt message of the dialog box

        x, y = eval("dialog_frame.midtop")
        prompt_box.midtop = x, y + 10
        pygame.draw.rect(screen, 'WHITE', dialog_frame)
        screen.blit(prompt, prompt_box)  # Display the text
        num_options = 2 if num_options is None else num_options  # Default number of options

        # Create the options of the dialog box
        if num_options == 2:
            x, y = eval("dialog_frame.midbottom")
            option_1 = self.draw_text_box(screen, 'Yes', x - self.inf_coeff - 10, y - self.inf_coeff - 10,
                                          'bottomright')

            option_2 = self.draw_text_box(screen, ' No ', x + self.inf_coeff + 10, y - self.inf_coeff - 10,
                                          'bottomleft')
            return option_1, option_2
        if num_options == 1:
            x, y = eval("dialog_frame.midbottom")
            option_1 = self.draw_text_box(screen, 'OK', x, y - self.inf_coeff - 10, 'midbottom')
            return option_1

    def on_cooldown(self):
        pass

    def is_clicked(self, frame, mouse_button):
        """
        Function to check if a text box is clicked
        Args:
            frame (pygame.Rect): the rectangle object of the text box
        Returns:
            True if the text box is clicked, False otherwise
        """

        pos = pygame.mouse.get_pos()
        if frame.collidepoint(pos) and mouse_button:  # Check if the mouse is clicked inside the text box
            return True
        else:
            return False

    def check_inside_screen(self, rectangle_object):

        """Function to check if the rectangle is inside the screen
        Args:
            rectangle_object (pygame.Rect): the rectangle object to be checked
        Returns:
            True if the rectangle is inside the screen, False otherwise
        """

        width, height = pygame.display.get_surface().get_size()  # Get the screen size
        screen_border = pygame.Rect(0, 0, width, height)  # Create a rectangle object of the screen
        return pygame.Rect.contains(screen_border, rectangle_object)  # Check if the rectangle is inside the screen

# welcome screen
def welcome_screen():
    pygame.init()
    welcome = True

    welcome_screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Welcome")
    full_screen=False

    #background = BLACK

    while welcome:
        LMB = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    LMB = True
        welcome_screen.fill(BLACK)
        header = Objects(text_color='WHITE', font_size=36)
        header.draw_text_box(welcome_screen,"Welcome to the Conway's", x=300,y=50, align='center')
        header.draw_text_box(welcome_screen, "Game of Life", x = 300, y = 100, align = 'center')
        prompt = Objects(text_color ='WHITE', font_size=30, obj_color='WHITE')
        prompt.draw_text_box(welcome_screen, 'Enable full screen?', x = 300, y = 250, frame_width=-1)
        yes = prompt.draw_text_box(welcome_screen, 'YES',x =200 ,y = 350, frame_width=3)
        no = prompt.draw_text_box(welcome_screen, ' NO ',x =400 ,y = 350, frame_width=3)
        if prompt.is_clicked(yes, LMB):
            full_screen = True
            welcome = False
        elif prompt.is_clicked(no,LMB):
            welcome = False

        exit = prompt.draw_text_box(welcome_screen, 'Exit', x=300, y=550, frame_width=3)
        if prompt.is_clicked(exit,LMB):
            sys.exit()

        pygame.display.update()

    pygame.quit()
    return(full_screen)



## TEST ENVIRONMENT ##
# The following code is used to test the buttons and dialog boxes classes in a test pygame environment
# The code should be hashed out when the module is used in the main program
"""
pygame.init()

def restart():
    print('Restarting')

def quit():
    print('Quitting')

def save():
    print('Saving')

exit_dialog = Objects(text_color='BLACK')
header = Objects(text_color='WHITE', font_size=40)
Menu = {'Restart': [None, restart],
        'Quit': [None, quit],
        'Save': [None, save]
}




screen = pygame.display.set_mode((700, 700))

running = True
background = WHITE

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    header.header(screen, 'Game of Life')

    yes, no = exit_dialog.dialog_box(screen, 'Are you sure you want to quit?')
    if exit_dialog.is_clicked(yes):
        running = False


    pygame.display.update()

pygame.quit()


"""




