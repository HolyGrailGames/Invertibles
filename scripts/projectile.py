import pygame
from pygame.sprite import Sprite

class Projectile(Sprite):
    """A class to manage projectiles fired from the hero"""

    def __init__(self, screen, hero, direc, current_spell):
        """Create a projectile object at the players current position"""
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen

        # Store which way the shot is fired
        self.direction = direc

        spells = [pygame.image.load('data/spells/Fire.png').convert_alpha(),
         pygame.image.load('data/spells/Water.png').convert_alpha(),
        pygame.image.load('data/spells/Air.png').convert_alpha(),
         pygame.image.load('data/spells/Dark.png').convert_alpha()]

        self.image = spells[current_spell]
        self.rect = self.image.get_rect()

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect.centerx = hero.rect.centerx
        self.rect.centery = hero.rect.centery

        self.name = 'projectile'
        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        self.speed_factor = 160

    def update(self, dt):
        """Move the projectile across the screen"""
        # Update the decimal position of the projectile.
        if self.direction == 'UP':
            self.y -= self.speed_factor * dt
        elif self.direction == 'DOWN':
            self.y += self.speed_factor * dt
        elif self.direction == 'RIGHT':
            self.x += self.speed_factor * dt
        elif self.direction == 'LEFT':
            self.x -= self.speed_factor * dt

        # Update the rect position.
        self.rect.y = self.y
        self.rect.x = self.x

    def change_sprite(self, which):
        if which == 1:
            self.image = self.fire
        elif which == 2:
            self.image == self.water
        elif which == 3:
            self.image == self.air
        elif which == 4:
            self.image == self.dark
