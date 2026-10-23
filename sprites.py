# load pygame, the sprite tools, and the game settings
import pygame as pg
from settings import *
from pygame.sprite import Sprite
# load the helper that cuts character frames out of a sprite sheet
from utils import Spritesheet, Cooldown
# choose random directions for the small coin particles
from random import randint
 
from os import path
 
# use vectors to store position and movement
vec = pg.math.Vector2

# wall collision helpers adapted from Chris Cozort's classroom game
def collide_hit_rect(one, two):
    # check the smaller player rectangle against the wall rectangle
    return one.hit_rect.colliderect(two.rect)

def collide_with_walls(sprite, group, direction):
    # resolve one direction at a time so the player can slide along walls
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    for wall in hits:
        if direction == 'x':
            if sprite.vel.x > 0:
                sprite.hit_rect.right = wall.rect.left
            elif sprite.vel.x < 0:
                sprite.hit_rect.left = wall.rect.right
        if direction == 'y':
            if sprite.vel.y > 0:
                sprite.hit_rect.bottom = wall.rect.top
            elif sprite.vel.y < 0:
                sprite.hit_rect.top = wall.rect.bottom
    if hits:
        # keep the position and movement lined up with the collision rectangle
        if direction == 'x':
            sprite.pos.x = sprite.hit_rect.centerx
            sprite.vel.x = 0
        if direction == 'y':
            sprite.pos.y = sprite.hit_rect.centery
            sprite.vel.y = 0
 
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
        # load the mushroom that changes between red and green
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, 'mushroom_sheet.png'))
        self.load_images()
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        # start each round with no coins collected
        self.coins = 0
        self.image = self.idle_frames[self.current_frame]
        self.rect = self.image.get_rect()
        # start with no movement in either direction
        self.vel = vec(0,0)
        # convert the starting tile position into pixels
        self.pos = vec(x*TILESIZE + TILESIZE/2, y*TILESIZE + TILESIZE/2)
        # give each player its own collision rectangle at its starting position
        self.hit_rect = PLAYER_HIT_RECT.copy()
        self.hit_rect.center = self.pos
        self.rect.center = self.pos

        # print a startup message and the rectangle position for checking
        print("player initialized")
        print(self.rect.x)
        print(self.rect.y)
    # check which movement keys are held down
    def get_keys(self):

        # reset movement so the player stops when no keys are held
        self.vel = vec(0, 0)
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
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.7071

    # animation adapted from Chris Cozort's classroom game
    def load_images(self):
        # take the red mushroom first and the green mushroom second
        self.idle_frames = [
            self.spritesheet.get_image(0, 0, TILESIZE, TILESIZE),
            self.spritesheet.get_image(TILESIZE, 0, TILESIZE, TILESIZE)
        ]

    def animate(self):
        # change frames every 350 milliseconds without moving the player
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            center = self.rect.center
            self.image = self.idle_frames[self.current_frame]
            self.rect = self.image.get_rect(center=center)

    # update the player position each frame
    def update(self):
        self.get_keys()
        self.animate()
        # use time since the last frame to keep movement speed steady
        # move the drawing rectangle to the new horizontal position
        self.pos.x += self.vel.x * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        # move the drawing rectangle to the new vertical position
        self.pos.y += self.vel.y * self.game.dt
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center
        # remove any coins the player touches after moving
        hits = pg.sprite.spritecollide(self, self.game.all_coins, True)
        # count every coin collected, even if two are touched together
        self.coins += len(hits)
        # create a small burst at each collected coin
        for coin in hits:
            for _ in range(10):
                Particle(self.game, coin.rect.centerx, coin.rect.centery)
        # play the pickup sound only when a coin was touched
        if hits:
            self.game.pickup_snd.play()

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
 
# coin pickup adapted from Chris Cozort's classroom game
class Coin(Sprite):
    def __init__(self, game, x, y):
        # add the coin to the drawing group and the coin group
        self.groups = game.all_sprites, game.all_coins
        Sprite.__init__(self, self.groups)
        self.game = game
        # load the two coin frames from the classroom sprite sheet
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, 'classroom_sheet.png'))
        self.idle_frames = [self.spritesheet.get_image(64, 0, TILESIZE, TILESIZE),
                            self.spritesheet.get_image(96, 0, TILESIZE, TILESIZE)]
        for frame in self.idle_frames:
            frame.set_colorkey(BLACK)
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        self.image = self.idle_frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x*TILESIZE, y*TILESIZE))

    def update(self):
        # switch coin frames every 350 milliseconds and keep the same position
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            self.image = self.idle_frames[self.current_frame]

# enemy chasing and animation adapted from Chris Cozort's classroom game
class Mob(Sprite):
    def __init__(self, game, x, y):
        # keep enemies in both the drawing group and the enemy group
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.spritesheet = Spritesheet(path.join(self.game.img_dir, 'classroom_sheet.png'))
        # use the classroom enemy frames while keeping the player's mushroom
        self.idle_frames = [self.spritesheet.get_image(64, 0, TILESIZE, TILESIZE),
                            self.spritesheet.get_image(96, 0, TILESIZE, TILESIZE)]
        for frame in self.idle_frames:
            frame.set_colorkey(BLACK)
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        self.image = self.idle_frames[self.current_frame]
        self.pos = vec(x*TILESIZE + TILESIZE/2, y*TILESIZE + TILESIZE/2)
        self.rect = self.image.get_rect(center=self.pos)
        # give each enemy its own rectangle for checking walls
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.pos
        self.speed = 100
        self.vel = vec(0, 0)

    def chase(self, obj):
        # move toward the player without stepping past them in one frame
        offset = obj.pos - self.pos
        self.vel = vec(0, 0)
        if self.game.dt > 0:
            self.vel.x = max(-self.speed, min(self.speed, offset.x / self.game.dt))
            self.vel.y = max(-self.speed, min(self.speed, offset.y / self.game.dt))

    def update(self):
        # change enemy frames on the same timer as the coins
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
            self.image = self.idle_frames[self.current_frame]
        self.chase(self.game.player)
        # check each direction separately so enemies cannot pass through walls
        self.pos.x += self.vel.x * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.all_walls, 'x')
        self.pos.y += self.vel.y * self.game.dt
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.all_walls, 'y')
        self.rect.center = self.hit_rect.center


# particles adapted from Chris Cozort's particles and cooldown lesson
class Particle(Sprite):
    def __init__(self, game, x, y):
        # draw and update particles with the other sprites
        self.groups = game.all_sprites, game.all_particles
        Sprite.__init__(self, self.groups)
        self.game = game
        # make a small white square at the coin's position in pixels
        self.image = pg.Surface((TILESIZE//8, TILESIZE//8))
        self.image.fill(WHITE)
        self.pos = vec(x, y)
        self.rect = self.image.get_rect(center=self.pos)
        self.speed = 25
        # remove the particle after three seconds
        self.countdown = Cooldown(3000)

    def update(self):
        # stop updating and drawing the particle when its timer finishes
        if self.countdown.ready():
            self.kill()
            return
        # scatter in random directions using the time between frames
        self.pos.x += self.speed * randint(-5, 5) * self.game.dt
        self.pos.y += self.speed * randint(-5, 5) * self.game.dt
        self.rect.center = self.pos
