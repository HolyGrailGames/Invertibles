import pygame
from scripts.text import Text

class TextRectException:
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

class DialogBox(pygame.sprite.Sprite):

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.image = pygame.image.load('data/dialog_box.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (800, 192))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.bottom = 600

        self.font = pygame.font.Font('data/game_boy.ttf', 22)
        self.text_color = (255, 255, 255)
        self.background_color = (65,131,148)
        self.textarea_rect = pygame.Rect(25, 430, 750, 150)

    def blitme(self):
        self.screen.blit(self.image, self.rect)


    def render_textrect(self, text, justification=0):
        """Returns a surface containing the passed text string, reformatted
        to fit within the given rect, word-wrapping as necessary. The text
        will be anti-aliased.

        Takes the following arguments:

        string - the text you wish to render. \n begins a new line.
        font - a Font object
        rect - a rectstyle giving the size of the surface requested.
        text_color - a three-byte tuple of the rgb value of the
                     text color. ex (0, 0, 0) = BLACK
        background_color - a three-byte tuple of the rgb value of the surface.
        justification - 0 (default) left-justified
                        1 horizontally centered
                        2 right-justified

        Returns the following values:

        Success - a surface object with the text rendered onto it.
        Failure - raises a TextRectException if the text won't fit onto the surface.
        """

        final_lines = []

        requested_lines = text.splitlines()

        # Create a series of lines that will fit on the provided
        # rectangle.

        for requested_line in requested_lines:
            if self.font.size(requested_line)[0] > self.textarea_rect.width:
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if self.font.size(word)[0] >= self.textarea_rect.width:
                        raise TextRectException("The word " + word + " is too long to fit in the rect passed.")
                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.
                    if self.font.size(test_line)[0] < self.textarea_rect.width:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)

        # Let's try to write the text out on the surface.

        surface = pygame.Surface(self.textarea_rect.size)
        surface.fill(self.background_color)

        accumulated_height = 0
        for line in final_lines:
            if accumulated_height + self.font.size(line)[1] >= self.textarea_rect.height:
                raise TextRectException("Once word-wrapped, the text string was too tall to fit in the rect.")
            if line != "":
                tempsurface = self.font.render(line, False, self.text_color)
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface, ((self.textarea_rect.width - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface, (self.textarea_rect.width - tempsurface.get_width(), accumulated_height))
                else:
                    raise TextRectException("Invalid justification argument: " + str(justification))
            accumulated_height += self.font.size(line)[1]

        return surface
