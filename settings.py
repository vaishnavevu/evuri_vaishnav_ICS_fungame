import pygame as pg

# set the window width and height in pixels
WIDTH = 1024
HEIGHT = 768
# set the text shown at the top of the game window
TITLE = "Best game evah!!!"
# set the tile size and the size of the player square in pixels
TILESIZE = 32
# set the target number of frames per second
FPS = 30

# colors use red, green, and blue values from 0 to 255
BGCOLOR = (255, 100, 100)
# use white for the player square
WHITE = (255,255,255)
#used for green sqaure
GREEN = (0,120,0)
# use red for the enemy square
RED = (255,0,0)

# extra drawing colors from the classroom game's settings
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
SILVER = (192, 192, 192)
MAROON = (128, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
OLIVE = (128, 128, 0)
LIME = (50, 205, 50)
DARK_GREEN = (0, 100, 0)
TEAL = (0, 128, 128)
CYAN = (0, 255, 255)
SKY_BLUE = (135, 206, 235)
BLUE = (0, 0, 255)
NAVY = (0, 0, 128)
PURPLE = (128, 0, 128)
VIOLET = (238, 130, 238)
MAGENTA = (255, 0, 255)
PINK = (255, 192, 203)
BROWN = (139, 69, 19)
BEIGE = (245, 245, 220)

# set how many pixels the player moves per second along each axis
PLAYER_SPEED = 300
# use a slightly smaller rectangle when checking the player against walls
PLAYER_HIT_RECT = pg.Rect(0, 0, TILESIZE-5, TILESIZE-5)
