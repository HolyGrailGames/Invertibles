import os.path
import pygame
import pyscroll
import pyscroll.data
import random
import sys
from random import randint
from pygame.sprite import Group
from pygame.locals import *
from pytmx.util_pygame import load_pygame
from pyscroll.group import PyscrollGroup

from scripts.text import Text
from scripts.npc import NPC
from scripts.projectile import Projectile
from scripts.hero import Hero
from scripts.sounds import Sounds
from scripts.dialog_box import DialogBox
from scripts.elementals import Elementals

# define configuration variables here
RESOURCES_DIR = 'data'

# Choose map
#MAP_FILENAME = 'dungeon.tmx'
#MAP_FILENAME = 'house_1.tmx'
MAP_FILENAME = 'town.tmx'

# simple wrapper to keep the screen resizeable
def init_screen(width, height):
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    return screen

# make loading maps a little easier
def get_map(filename):
    return os.path.join(RESOURCES_DIR, filename)

class Invertibles(object):
    filename = get_map(MAP_FILENAME)

    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 1, 4096)
        pygame.init()
        pygame.font.init()
        self.screen = init_screen(800, 600)
        pygame.display.set_caption('Polaria')

        # Music channel
        self.music_channel = pygame.mixer.Channel(1)
        self.sounds = Sounds()

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
        self.heroes = list()
        self.heroes.append(self.hero)

        # Spawn an npc
        self.npc = NPC()
        self.npc.position = self.map_layer.map_rect.move(544, 592).topleft
        self.group.add(self.npc)
        self.npcs = list()
        self.npcs.append(self.npc)

        # Spawn an elemental below the house
        self.spawn_elementals()

        # Spawn the hero outside his house
        self.hero.position = self.map_layer.map_rect.move(528, 592).topleft

        # add our hero to the group
        self.group.add(self.hero)


        self.projectile_skin = 0 # Which spell the user has selected
        self.clock = pygame.time.Clock()

        # Dictionary to hold onto what keys are being held down
        self.movement_keys = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}

    def draw(self, surface, text=None):

        # center the map/screen on our Hero
        self.group.center(self.hero.rect.center)

        # draw the map and all sprites

        self.group.draw(surface)
        #self.projectiles.draw(self.screen)

        score = Text(self.screen, str(len(self.elementals)) + " dark elementals remaining", (0,0,0), 650, 10)
        score.blitme()

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
                self.check_keydown_events(event)
            elif event.type == KEYUP:
                self.check_keyup_events(event)
            self.move_hero()

            if not self.running:
                break

            # this will be handled if the window is resized
            elif event.type == VIDEORESIZE:
                init_screen(event.w, event.h)
                self.map_layer.set_size((event.w, event.h))

            event = poll()

    def reset_movement_keys(self):
        """Reset movement keys to False."""
        self.movement_keys = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}

    def check_keydown_events(self, event):
        """Check for keypresses and respond to them."""
        if event.key == K_ESCAPE or event.key == K_q:
            self.running = False

        # Set movement key flags
        if event.key == K_a:
            self.reset_movement_keys()
            self.hero.reset_velocity()
            self.movement_keys['LEFT'] = True
        elif event.key == K_d:
            self.reset_movement_keys()
            self.hero.reset_velocity()
            self.movement_keys['RIGHT'] = True
        elif event.key == K_w:
            self.reset_movement_keys()
            self.hero.reset_velocity()
            self.movement_keys['UP'] = True
        elif event.key == K_s:
            self.reset_movement_keys()
            self.hero.reset_velocity()
            self.movement_keys['DOWN'] = True

        # Cast spells
        if event.key == K_UP:
            new_projectile = Projectile(self.screen, self.hero, 'UP', self.projectile_skin)
            self.group.add(new_projectile)
            self.sounds.fireball.play()
        elif event.key == K_LEFT:
            new_projectile = Projectile(self.screen, self.hero, 'LEFT', self.projectile_skin)
            self.group.add(new_projectile)
            self.sounds.fireball.play()
        elif event.key == K_RIGHT:
            new_projectile = Projectile(self.screen, self.hero, 'RIGHT', self.projectile_skin)
            self.group.add(new_projectile)
            self.sounds.fireball.play()
        elif event.key == K_DOWN:
            new_projectile = Projectile(self.screen, self.hero, 'DOWN', self.projectile_skin)
            self.group.add(new_projectile)
            self.sounds.fireball.play()

        # Change spells
        if event.key == K_1:
            self.projectile_skin = 0
            self.sounds.select_spell.play()
        elif event.key == K_2:
            self.projectile_skin = 1
            self.sounds.select_spell.play()
        elif event.key == K_3:
            self.projectile_skin = 2
            self.sounds.select_spell.play()
        elif event.key == K_4:
            self.projectile_skin = 3
            self.sounds.select_spell.play()

    def check_keyup_events(self, event):
        """Check for keyreleases and respond to them."""
        # Set movement key flags
        if event.key == K_a:
            self.movement_keys['LEFT'] = False
        if event.key == K_d:
            self.movement_keys['RIGHT'] = False
        if event.key == K_w:
            self.movement_keys['UP'] = False
        if event.key == K_s:
            self.movement_keys['DOWN'] = False

    def move_hero(self):
        """Only move hero if one movement key is being pressed."""
        count = 0
        key_pressed = ''
        for key, pressed in self.movement_keys.items():
            if pressed:
                key_pressed = key
                count += 1
        if count == 1:
            self.hero.set_direction(key_pressed)
        else:
            self.hero.set_idle()

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
                elif sprite.feet.collidelist(self.elementals) > -1:
                    sprite.move_back(dt)
                elif sprite.feet.collidelist(self.npcs) > -1:
                    sprite.move_back(dt)
            elif sprite.name == 'elemental':
                if sprite.feet.collidelist(self.walls) > -1:
                    sprite.move_back(dt)
                elif sprite.feet.collidelist(self.heroes) > -1:
                    sprite.move_back(dt)


            elif sprite.name == 'projectile':
                collide_elemental = sprite.rect.collidelist(self.elementals)
                if sprite.rect.collidelist(self.walls) > -1:
                    self.group.remove(sprite)
                elif collide_elemental > -1:
                    self.group.remove(sprite)
                    self.group.remove(self.elementals[collide_elemental])
                    self.elementals.pop(collide_elemental)
                    self.sounds.monster_kill.play()



    def run(self):
        """ Run the game loop"""

        self.running = True
        self.music_channel.play(self.sounds.town_theme, -1)

        text = ['We, the people of Polaria have summoned thee, the Lord of Light!\n\nPress enter to continue.',
                'Our beloved town has been overrun by evil dark elementals! Their dark magic can only be fought with the magic of Light!\n\nPress Enter to continue.',
                'Use WASD to move around and the arrow keys to cast your spells. You can switch spells with keys 1-4.\n\nPress Enter to continue.',
                'Good luck! And may the power of Light be with you!\n\nPress enter to continue.']
        self.run_dialog(text)

        while self.running:
            dt = self.clock.tick(60) / 1000.

            self.handle_input()
            self.update(dt)
            if len(self.elementals) <= 0:
                self.run_dialog(["Congratulations! You saved our town! Polaria is safe once more!"])
                self.running = False
            else:
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

    def spawn_elementals(self):
        """Spawn elementals in random positions on the map."""
        self.elementals = list()
        count = 0
        while count < 100:
            x = randint(0, 1120)
            y = randint(0, 1120)
            elemental = Elementals()
            elemental.position = self.map_layer.map_rect.move(x, y).topleft
            elemental.set_rect(x, y)
            if elemental.rect.collidelist(self.walls) == -1:
                self.elementals.append(elemental)
                self.group.add(elemental)
                count += 1

    def handle_dialog_box_input(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True
                if event.key == K_ESCAPE or event.key == K_q:
                    sys.exit()
            if event.type == VIDEORESIZE:
                init_screen(event.w, event.h)
                self.map_layer.set_size((event.w, event.h))
