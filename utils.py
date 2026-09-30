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
