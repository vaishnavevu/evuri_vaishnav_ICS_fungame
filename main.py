# This file was created by Vaishnav evuri
# Code inspired by Chris bradfield who was inspired by Notch
# Data types: boolean, JSON, strings,
# Input (events): Keyboard, mouse, right click, voice, power button, eye tracking, camera, gyroscoping,
# electrostatic, location, volume button, microphone,
# Process: Cursor position, position of the player, score, enemy position,
# Aim in FPS,
# Output: Graphics - things are drawn, sound: jump, walking, power up,
# haptics
# load pygame, the player code, and the game settings
import pygame as pg
from os import path
from settings import *
from sprites import *
# load the map tools
from utils import *
 
# keep the game setup and main actions together
class Game:
    # set up the game when a game object is created
    def __init__(self):
        # start pygame and its sound system
        pg.init()
        pg.mixer.init()
        # create the game window using the chosen size and title
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        print("game initialized...")
        pg.display.set_caption(TITLE)
        # track whether the game and the current round are running
        self.running = True
        self.playing = True
        # create a clock to control the frame rate
        self.clock = pg.time.Clock()
    # find the game folders and load the map file
    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        self.img_dir = path.join(self.game_dir, 'images')
        self.snd_dir = path.join(self.game_dir, 'audio')
        # load the sound that plays when a coin is collected
        self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir, 'pickup.wav'))
        self.map = Map(path.join(self.game_dir, map))
    # start a round with sprite groups and the player at the map's P
    def new(self):
        self.load_data('level1.txt')
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        # create a group to keep track of the coins left on the map
        self.all_coins = pg.sprite.Group()
        # create a group for the enemies
        self.all_mobs = pg.sprite.Group()
        # keep track of the particles created when coins are collected
        self.all_particles = pg.sprite.Group()
        self.wall = Wall(self, 10, 0)
 
        # create a wall for each 1 in the map
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                # create an enemy for each M in the map
                if tile == "M":
                    Mob(self, col, row)
                # create a coin for each C in the map
                if tile == "C":
                    Coin(self, col, row)
        # create the player after the walls so it draws on top
        # map spawning and wall collisions are adapted from Chris Cozort
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "P":
                    self.player = Player(self, col, row)
        # repeat the classroom background music while the round is running
        pg.mixer.music.load(path.join(self.snd_dir, 'Juhani Junkala_Stage 1.ogg'))
        pg.mixer.music.play(loops=-1)
    # repeat the main game steps while the round is active
    def run(self):
        self.playing = True
        while self.playing:
            # limit the frame rate and measure the time between frames in seconds
            self.dt = self.clock.tick(FPS) / 1000
            # handle input, move sprites, and draw the next frame
            self.events()

            self.update()
            self.draw()
    # check for window events, such as clicking the close button
    def events(self):
        for event in pg.event.get():
            # stop the round and the game when the window is closed
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
    # draw text centered at the chosen position on the screen
    def draw_text(self, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.all_sprites.draw(self.screen)
        # show the measured frame rate without dividing by zero
        self.draw_text(f"Frames per second:{self.clock.get_fps():.0f}", 24, WHITE, WIDTH/2, HEIGHT/4)
        # draw the coin count last so it shows on top of the game
        self.draw_text(f"Coins:{self.player.coins}", 24, WHITE, WIDTH/2, HEIGHT/7)
        pg.display.flip()
    # run the update method for every sprite in the group
    def update(self):
        self.all_sprites.update()
# create the game when this file is run directly
if __name__ == "__main__":
    g = Game()
 
    # start and run rounds until the game is closed
    while g.running:
        g.new()
        g.run()
    # close pygame after the game window is closed
    pg.quit()
