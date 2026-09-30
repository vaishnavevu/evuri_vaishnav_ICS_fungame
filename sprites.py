# load pygame, the sprite tools, and the game settings
import pygame as pg
from settings import *
from pygame.sprite import Sprite
 
from os import path
 
# use vectors to store position and movement
vec = pg.math.Vector2
 
# define the player and how it moves
class Player(Sprite):
    # set up the player when it is created
    def __init__(self, game, x, y):
        # add the player to the group that updates and draws sprites
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        # make a white square and a rectangle to track its position
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        # start with no movement in either direction
        self.vel = vec(0,0)
        # convert the starting tile position into pixels
        self.pos = vec(x,y)

        # print a startup message and the rectangle position for checking
        print("player initialized")
        print(self.rect.x)
        print(self.rect.y)
    # check which movement keys are held down
    def get_keys(self):

        # reset movement so the player stops when no keys are held
        self.vx, self.vy = 0, 0
        # read the keyboard so held keys keep the player moving
        keys = pg.key.get_pressed()
        # left arrow or a moves the player left
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        # right arrow or d moves the player right
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        # up arrow or w moves the player up
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        # down arrow or s moves the player down
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        # reduce the movement speed when moving diagonally
        if self.vel != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    # update the player position each frame
    def update(self):
        self.get_keys()
        self.rect.center = self.pos
        #      self.rect.right = hits(0).rect.left
        # use time since the last frame to keep movement speed steady
        # move the drawing rectangle to the new horizontal position
        # move the drawing rectangle to the new vertical position
        self.pos += self.vel * self.game.dt

class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_walls
        Sprite.__init__(self, self.groups)
        self.game = game
        # make a white square and a rectangle to track its position
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        # start with no movement in either direction
        self.x = x * TILESIZE
        # convert the starting tile position into pixels
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y
 
# define the enemy and how it moves
class Mob(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.speed = 1
        self.vx, self.vy = 500,0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        # print a startup message and the rectangle position for checking
        print("player initialized")
        self.rect.x = self.x
        self.rect.y = self.y
 
    def update(self):
        # turn the enemy around and move it down when it leaves the screen
        if self.rect.x > WIDTH or self.rect.x < 0:
            print("I've broken out of my cage")
            self.speed *= -1
            self.y += TILESIZE
        self.x += self.vx * self.game.dt * self.speed
        self.rect.x = self.x

        self.rect.y = self.y
