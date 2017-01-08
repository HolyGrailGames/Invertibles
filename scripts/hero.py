import pygame
import os.path

from pygame.time import get_ticks

class Hero(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sprites =      {'DOWN':  [pygame.image.load('data/ninja/ninja_down_walk1.png').convert_alpha(),
                                       pygame.image.load('data/ninja/ninja_down_walk2.png').convert_alpha(),
                                       pygame.image.load('data/ninja/ninja_down_idle.png').convert_alpha()],

                             'UP':    [pygame.image.load('data/ninja/ninja_up_walk1.png').convert_alpha(),
                                       pygame.image.load('data/ninja/ninja_up_walk2.png').convert_alpha(),
                                       pygame.image.load('data/ninja/ninja_up_idle.png').convert_alpha()],

                             'RIGHT': [pygame.image.load('data/ninja/ninja_right_walk1.png').convert_alpha(),
                                       pygame.image.load('data/ninja/ninja_right_walk2.png').convert_alpha(),
                                       pygame.image.load('data/ninja/ninja_right_idle.png').convert_alpha()],

                             'LEFT':  [pygame.image.load('data/ninja/ninja_left_walk1.png').convert_alpha(),
                                       pygame.image.load('data/ninja/ninja_left_walk2.png').convert_alpha(),
                                       pygame.image.load('data/ninja/ninja_left_idle.png').convert_alpha()]}

        self.current_sprites = self.sprites['DOWN']
        self.image = self.current_sprites[2]
        self.image_index = 0
        self.name = 'hero'
        self.velocity = [0, 0]
        self._position = [0, 0]
        self._old_position = self.position
        self.rect = self.image.get_rect()
        self.feet = pygame.Rect(0, 0, self.rect.width * .5, 8)


        self.time_of_last_step = pygame.time.get_ticks()
        self.step_frequency = 200
        self.moving = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}
        self.speed = 50

    @property
    def position(self):
        return list(self._position)

    @position.setter
    def position(self, value):
        self._position = list(value)

    def set_direction(self, direction):
        """Set the direction of the hero."""
        if direction == 'UP':
            self.velocity[1] = -self.speed
        elif direction == 'DOWN':
            self.velocity[1] = self.speed
        elif direction == 'LEFT':
            self.velocity[0] = -self.speed
        elif direction == 'RIGHT':
            self.velocity[0] = self.speed
        self.current_sprites = self.sprites[direction]
        self.reset_movement()
        self.moving[direction] = True

    def reset_movement(self):
        """Reset movement flags to False."""
        self.moving = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}

    def reset_velocity(self):
        """Reset velocity to zero."""
        self.velocity[0] = 0
        self.velocity[1] = 0

    def update(self, dt):
        self._old_position = self._position[:]
        self._position[0] += self.velocity[0] * dt
        self._position[1] += self.velocity[1] * dt
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom

        # If moving in any direction, animate walk sequence.
        if any(self.moving.values()):
            current_time = pygame.time.get_ticks()
            if current_time - self.time_of_last_step > self.step_frequency:
                self.image = self.current_sprites[self.image_index]
                self.image_index ^= 1
                self.time_of_last_step = current_time

    def set_idle(self):
        self.reset_movement()
        self.velocity[0] = 0
        self.velocity[1] = 0
        self.image = self.current_sprites[2]

    def move_back(self, dt):
        """ If called after an update, the sprite can move back"""
        self._position = self._old_position
        self.rect.topleft = self._position
        self.feet.midbottom = self.rect.midbottom
