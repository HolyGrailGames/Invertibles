from pygame.font import Font

class Text():
    """A class representing text."""

    def __init__(self, screen, settings, text, color, x, y):
        """Initialize text."""
        self.screen = screen
        self.settings = settings
        self.font = Font(self.settings.font, self.settings.font_size)
        self.image = self.font.render(text, False, color).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.y = y


    def blitme(self):
        """Draw the text at it's current position."""
        self.screen.blit(self.image, self.rect)
