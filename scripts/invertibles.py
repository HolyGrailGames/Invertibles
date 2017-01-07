import os.path
import pygame
import pyscroll
import pyscroll.data

from scripts.projectile import Projectile
from scripts.hero import Hero
from pygame.sprite import Group
from scripts.dialog_box import DialogBox
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from pyscroll.group import PyscrollGroup



# define configuration variables here
RESOURCES_DIR = 'data'
HERO_MOVE_SPEED = 80  # pixels per second
MAP_FILENAME = 'dungeon.tmx'

# simple wrapper to keep the screen resizeable
def init_screen(width, height):
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen

# make loading maps a little easier
def get_map(filename):
    return os.path.join(RESOURCES_DIR, filename)

class Invertibles(object):
    """ This class is a basic game.

    This class will load data, create a pyscroll group, a hero object.
    It also reads input and moves the Hero around the map.
    Finally, it uses a pyscroll group to render the map and Hero.
    """
    filename = get_map(MAP_FILENAME)

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = init_screen(800, 600)
        pygame.display.set_caption('Invertibles.')

        # Store projectiles in a group
        self.projectiles = Group()

        # true while running
        self.running = False

        # load data from pytmx
        tmx_data = load_pygame(self.filename)

        # setup level geometry with simple pygame rects, loaded from pytmx
        self.walls = list()
        for object in tmx_data.objects:
            self.walls.append(pygame.Rect(
                object.x, object.y,
                object.width, object.height))

        # create new data source for pyscroll
        map_data = pyscroll.data.TiledMapData(tmx_data)

        # create new renderer (camera)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 3.75

        # pyscroll supports layered rendering.  our map has 3 'under' layers
        # layers begin with 0, so the layers are 0, 1, and 2.
        # since we want the sprite to be on top of layer 1, we set the default
        # layer for sprites as 2
        self.group = PyscrollGroup(map_layer=self.map_layer, default_layer=3)
        self.hero = Hero()

        # put the hero in the center of the map
        self.hero.position = self.map_layer.map_rect.center

        # add our hero to the group
        self.group.add(self.hero)

        self.projectile_skin = 0 # Which spell the user has selected
        self.clock = pygame.time.Clock()

    def draw(self, surface, text=None):

        # center the map/screen on our Hero
        self.group.center(self.hero.rect.center)

        # draw the map and all sprites

        self.group.draw(surface)
        #self.projectiles.draw(self.screen)

        if text:
            dialogbox = DialogBox(self.screen)
            dialogbox.blitme()

            rendered_text = dialogbox.render_textrect(text)
            if rendered_text:
                self.screen.blit(rendered_text, dialogbox.textarea_rect)

    def handle_input(self):
        """ Handle pygame input events """
        poll = pygame.event.poll

        event = poll()
        while event:
            if event.type == QUIT:
                self.running = False
                break

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE or event.key == K_q:
                    self.running = False
                    break

                elif event.key == K_EQUALS:
                    self.map_layer.zoom += .25

                elif event.key == K_MINUS:
                    value = self.map_layer.zoom - .25
                    if value > 0:
                        self.map_layer.zoom = value

                # Cast spells
                elif event.key == K_UP:
                    new_projectile = Projectile(self.screen, self.hero, 'UP', self.projectile_skin)
                    self.group.add(new_projectile)
                elif event.key == K_LEFT:
                    new_projectile = Projectile(self.screen, self.hero, 'LEFT', self.projectile_skin)
                    self.group.add(new_projectile)
                elif event.key == K_RIGHT:
                    new_projectile = Projectile(self.screen, self.hero, 'RIGHT', self.projectile_skin)
                    self.group.add(new_projectile)
                elif event.key == K_DOWN:
                    new_projectile = Projectile(self.screen, self.hero, 'DOWN', self.projectile_skin)
                    self.group.add(new_projectile)


            # this will be handled if the window is resized
            elif event.type == VIDEORESIZE:
                init_screen(event.w, event.h)
                self.map_layer.set_size((event.w, event.h))

            event = poll()

        # Move up or down
        pressed = pygame.key.get_pressed()
        if pressed[K_w]:
            self.hero.velocity[1] = -HERO_MOVE_SPEED
            self.hero.change_sprite(pygame.K_UP)
        elif pressed[K_s]:
            self.hero.velocity[1] = HERO_MOVE_SPEED
            self.hero.change_sprite(pygame.K_DOWN)
        else:
            self.hero.velocity[1] = 0

        # Move left or right
        if pressed[K_a]:
            self.hero.velocity[0] = -HERO_MOVE_SPEED
            self.hero.change_sprite(pygame.K_LEFT)
        elif pressed[K_d]:
            self.hero.velocity[0] = HERO_MOVE_SPEED
            self.hero.change_sprite(pygame.K_RIGHT)
        else:
            self.hero.velocity[0] = 0

        # Change spells

        if pressed[K_1]:
            self.projectile_skin = 0
        elif pressed[K_2]:
            self.projectile_skin = 1
        elif pressed[K_3]:
            self.projectile_skin = 2
        elif pressed[K_4]:
            self.projectile_skin = 3



    def update_projectiles(self):
        """Update position of projectiles and get rid of old bullets."""
        # Update projectile positions
        self.projectiles.update()


        # Get rid of projectiles that have gone off screen
        for projectile in self.projectiles.copy():
            if projectile.rect.bottom <= 0:
                self.projectiles.remove(projectile)


    def update(self, dt):
        """ Tasks that occur over time should be handled here"""
        self.group.update(dt)
        self.update_projectiles()

        # check if the sprite's feet are colliding with wall
        # sprite must have a rect called feet, and move_back method,
        # otherwise this will fail

        for sprite in self.group.sprites():
            if sprite.name == 'hero':
                if sprite.feet.collidelist(self.walls) > -1:
                    sprite.move_back(dt)
            if sprite.name == 'projectile':
                if sprite.rect.collidelist(self.walls) > -1:
                    self.group.remove(sprite)

    def run(self):
        """ Run the game loop"""

        self.running = True

        text = ['Welcome Adventurer to the crazy world of the Polar Opposites! You will find many perils ahead that can be vanquished with your mighty magic abilities! May the power of the poles be with you!']
        self.run_dialog(text)

        while self.running:
            dt = self.clock.tick(60) / 1000.

            self.handle_input()
            self.update(dt)
            self.draw(self.screen)
            pygame.display.update()

    def run_dialog(self, text):
        self.update(0)
        while text:
            self.clock.tick(60)
            self.draw(self.screen, text[0])
            if self.handle_dialog_box_input():
                text.remove(text[0])
            pygame.display.update()

    def handle_dialog_box_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
