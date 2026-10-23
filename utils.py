# load pygame, the game settings, and the math tools
import pygame as pg
from settings import *
from math import floor
 
# load the map and work out its size
class Map:
    def __init__(self, filename):
        self.data = []
        # read each row of the map from the text file
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
 
        # calculate the map size in tiles and pixels
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

# sprite sheet tools adapted from Chris Cozort's classroom game
class Spritesheet:
    def __init__(self, filename):
        # load the full picture once using the game window's color format
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # copy one frame out of the larger picture
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        # hide the black background around the character
        image.set_colorkey(BLACK)
        return image


# cooldown timer adapted from Chris Cozort's particles and cooldown lesson
class Cooldown:
    def __init__(self, time):
        # store the duration in milliseconds and start the timer now
        self.time = time
        self.start()

    def start(self):
        # restart the timer so it can be used again
        self.start_time = pg.time.get_ticks()
        self.current_time = self.start_time
        self.delta = 0

    def ticking(self):
        # keep track of how many seconds have passed since the timer started
        self.current_time = pg.time.get_ticks()
        self.delta = (self.current_time - self.start_time) / 1000

    def ready(self):
        # check the elapsed milliseconds against the chosen duration
        self.ticking()
        return self.current_time - self.start_time >= self.time
