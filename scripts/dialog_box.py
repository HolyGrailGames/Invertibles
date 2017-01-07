import pygame
from scripts.text import Text

class DialogBox(pygame.sprite.Sprite):

    def __init__(self, screen, text):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.text = text
        self.image = pygame.image.load('data/dialog_box.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (800, 192))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.bottom = 600

    def blitme(self):
        self.screen.blit(self.image, self.rect)
