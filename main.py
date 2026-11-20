# Pocket Mine design goals
# 1. map and collisions: explore grass above ground and dig tunnels through dirt.
# 2. mining controls: face a block with the arrows and press space to mine it.
# 3. scoring and feedback: collect ore, update counters, and show cracks and particles.
# goal: collect coal and gold to increase the score and beat the saved high score.
# rules: dirt takes one press, coal takes three hits, and stone walls cannot break.
# rules: coal gives five points and gold gives one point after its dirt is cleared.
# feedback: mining sounds, coal cracks, gold particles, and counters show progress.
# freedom: choose where to dig and which ore to collect without a time limit.
# beta plans: add a five-piece bag, a shop, and rarer ores deeper underground.
# project by Vaishnav Evuri, adapted from Chris Cozort's classroom engine.
# original tutorial credit: Chris Bradfield at Kids Can Code.
# class source: https://github.com/ccozort/cozort_chris_ICP_featherblade

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
        pg.display.set_caption(TITLE)
        # track whether the game and the current round are running
        self.running = True
        self.playing = True
        # create a clock to control the frame rate
        self.clock = pg.time.Clock()
        # track the current score and the best score from earlier games
        self.score = 0
        self.high_score = 0
    # find the game folders and load the map file
    def load_data(self, map):
        self.game_dir = path.dirname(__file__)
        # keep the saved high score in the game folder
        self.game_save_file = path.join(self.game_dir, "highscore.txt")
        self.img_dir = path.join(self.game_dir, 'images')
        self.snd_dir = path.join(self.game_dir, 'audio')
        # load the sound that plays when a coin is collected
        self.pickup_snd = pg.mixer.Sound(path.join(self.snd_dir, 'pickup.wav'))
        self.map = Map(path.join(self.game_dir, map))
        self.load_high_score()
    # score saving adapted from Chris Cozort's classroom game
    def load_high_score(self):
        # use zero when there is no saved score or the file is not a number
        try:
            with open(self.game_save_file, 'r', encoding='utf-8') as file:
                self.high_score = max(0, int(file.read()))
        except (OSError, ValueError):
            self.high_score = 0

    def save_high_score(self):
        # replace the saved record only when the current score is higher
        if self.score > self.high_score:
            try:
                with open(self.game_save_file, 'w', encoding='utf-8') as file:
                    file.write(str(self.score))
            except OSError as error:
                # let the game close normally if the score file cannot be saved
                print(f"high score could not be saved: {error}")
            else:
                self.high_score = self.score

    # start a round with sprite groups and the player at the map's P
    def new(self):
        self.load_data('level1.txt')
        # start the new round with no points
        self.score = 0
        self.all_sprites = pg.sprite.Group()
        self.all_walls = pg.sprite.Group()
        # keep dirt and coal together for the spacebar mining check
        self.all_mineable = pg.sprite.Group()
        # create a group to keep track of the coins left on the map
        self.all_coins = pg.sprite.Group()
        # keep track of the particles created when coins are collected
        self.all_particles = pg.sprite.Group()
 
        # create a wall for each 1 in the map
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    Wall(self, col, row)
                # create breakable dirt for each D in the map
                if tile == "D":
                    Dirt(self, col, row)
                # place coal wherever the map has a K
                if tile == "K":
                    Coal(self, col, row)
                # place gold inside dirt so it has to be dug out
                if tile == "C":
                    Dirt(self, col, row)
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
                # save a new record before closing the game
                self.save_high_score()
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
        # keep the top quarter grassy and the tunnels dark brown
        pg.draw.rect(self.screen, (66, 119, 48), (0, 0, WIDTH, HEIGHT/4))
        # draw a few short grass marks across the surface
        for x in range(32, WIDTH - 32, 64):
            pg.draw.line(self.screen, (96, 151, 64), (x, 110), (x + 3, 102), 2)
            pg.draw.line(self.screen, (96, 151, 64), (x + 20, 175), (x + 23, 167), 2)
        self.all_sprites.draw(self.screen)
        # keep the counters on a dark strip above the play area
        pg.draw.rect(self.screen, BGCOLOR, (32, 32, WIDTH - 64, 56))
        self.draw_text(f"Score:{self.score}", 22, WHITE, 130, 34)
        self.draw_text(f"High Score:{self.high_score}", 22, WHITE, 330, 34)
        self.draw_text(f"Gold nuggets:{self.player.coins}", 22, WHITE, 570, 34)
        self.draw_text(f"Coal:{self.player.coal_count}", 22, WHITE, 780, 34)
        # remind the player how to move and dig
        self.draw_text("Arrow keys: move and face a block    Space: mine", 18, WHITE, WIDTH/2, 62)
        self.draw_text(f"FPS:{self.clock.get_fps():.0f}", 16, WHITE, 925, 38)
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
