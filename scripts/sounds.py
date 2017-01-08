from pygame.mixer import Sound

class Sounds():
    """A class to store all sounds in Invertibles."""

    def __init__(self):
        """Initialize sounds."""
        # Music
        self.town_theme = Sound('data/sounds/TownTheme.ogg')

        # Sound Effects
        self.fireball = Sound('data/sounds/fireball-whoosh.ogg')
        self.select_spell = Sound('data/sounds/metal-small1.ogg')


    def set_volume(self):
        """Set volume of Sounds."""
        self.town_theme.set_volume(.75)
