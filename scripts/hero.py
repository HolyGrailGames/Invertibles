import pygame
import os.path

from pygame.time import get_ticks

class Hero(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_down = pygame.image.load('data/ninja/ninja_down_idle.png').convert_alpha()
        self.image_up = pygame.image.load('data/ninja/ninja_up_idle.png').convert_alpha()
        self.image_right = pygame.image.load('data/ninja/ninja_right_idle.png').convert_alpha()
        self.image_left = pygame.image.load('data/ninja/ninja_left_idle.png').convert_alpha()
        self.image = self.image_down
        self.name = 'hero'
        self.velocity = [0, 0]
        self._position = [0, 0]
        self._old_position = self.position
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * .5, 8)
        self.last_step = pygame.time.get_ticks()

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def change_sprite(self, key):
        if key == pygame.K_DOWN:
            self.image = self.image_down
        if key == pygame.K_UP:
            self.image = self.image_up
        if key == pygame.K_RIGHT:
            self.image = self.image_right
        if key == pygame.K_LEFT:
            self.image = self.image_left

    def update(self, dt):
        self._old_position = self._position[:]
        self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self, dt):
        """ If called after an update, the sprite can move back"""
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom
