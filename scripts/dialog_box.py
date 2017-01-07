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

"""
    def drawText(self, surface, text, color, rect, font, aa=False, bkg=None):
        # draw some text into an area of a surface
        # automatically wraps words
        # returns any text that didn't get blitted

        rect = pygame.Rect(rect)
        y = rect.top
        lineSpacing = -2

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)

            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return text"""
