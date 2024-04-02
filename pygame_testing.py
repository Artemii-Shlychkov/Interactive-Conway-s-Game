"""Draw text to the screen."""
import pygame
from pygame.locals import QUIT


def restart():
    print('Restarting')

def quit():
    print('Quitting')

def save():
    print('Saving')

BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
WHITE = (255, 255, 255)


screen = pygame.display.set_mode((500, 500))

from Archive import archive_objects as ms

buttons = ['Restart', 'Quit']

Menu = {'Restart': [None, restart],
        'Quit': [None, quit],
        'Save': [None, save]
}




pygame.init()



font = pygame.font.SysFont('Minecraft', 24)
word = font.render('Restart', True, WHITE)
text_box = word.get_rect(x=50, y=50)
frame = text_box.inflate(20, 20)
frame.center=(text_box.center)




button = ms.buttons()


running = True
background = GRAY

while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(background)
    screen.blit(word, text_box)
    pygame.draw.rect(screen, RED, frame, width =2)
    # create Menu

    for i, key in enumerate(Menu.keys()):
        Menu[key][0] = button.render(key, 50, 50*(i+1), screen)
        if button.is_clicked(Menu[key][0]):
            background = RED
            Menu[key][1]()








    pygame.display.update()

pygame.quit()