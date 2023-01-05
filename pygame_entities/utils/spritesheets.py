from typing import Tuple

import pygame


class SpriteSheet:
    """
    Class for getting images from spritesheets
    """

    def __init__(self, sprite_width: int, sprite_height: int, spritesheet_surface: pygame.Surface) -> None:
        """
        sprite_width - width of 1 sprite in spritesheet

        sprite_height - height of 1 sprite in spritesheet

        spritesheet_surface - pygame.Surface object with your spritesheet (may be loaded by pygame.image.load() function)
        """
        self.sprite_width = sprite_width
        self.sprite_height = sprite_height
        self._spritesheet = spritesheet_surface

    def image_at(self, sprite_xy: Tuple[int, int], size=(1, 1)) -> pygame.Surface:
        """
        Returning pygame.Surface with image from spritesheet at certain position

        sprite_xy - tuple with row number and column number of desired sprites

        size - tuple with size of desired sprite. (Not in pixels, it sayng to method amount of sprites from spritesheet to combine)
        """
        rect = pygame.Rect(
            (sprite_xy[0] * self.sprite_width,
             sprite_xy[1] * self.sprite_height),
            (sprite_xy[0] + size[0] * self.sprite_width,
             sprite_xy[1] + size[1] * self.sprite_height)
        )
        image = pygame.Surface(
            (size[0] * self.sprite_width, size[1] * self.sprite_height), pygame.SRCALPHA)
        image.blit(self._spritesheet, (0, 0), rect)

        return image
