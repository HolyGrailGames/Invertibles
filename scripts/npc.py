import pygame
import os.path

from pygame.time import get_ticks

class NPC(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('data/npcs/npc_1_down_idle.png').convert_alpha()
        self.name = 'NPC'
        self._position = [0, 0]
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * .5, 8)

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def update(self, dt):
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self, dt):
        """ If called after an update, the sprite can move back"""
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom
