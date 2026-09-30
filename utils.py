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
