"""
Classes for drawing sprites/sprite animations/etc
"""
from typing import List, Tuple, Union

from ..game import Game
from ..utils.math import Vector2

import pygame


class BaseSprite(pygame.sprite.Sprite):
    """
    Base sprite class.

    Used for showing images with on screen coords.

    Every sprite in game should inherit from this class.

    Automatically registering new sprite in game
    """

    def __init__(self, image: pygame.Surface, layer=0, start_position=(0, 0)) -> None:
        """
        Initializing new sprite.

        Sprites with bigger layer will be rendered on top of sprites with small layers.
        """
        pygame.sprite.Sprite.__init__(self)
        self._layer = layer

        self._original_image = image

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = start_position
        self.game = Game.get_instance()
        self._visibility = True

        # Transform vars
        self._rotation = 0.0

        # Registering sprite
        self.game.add_sprite(self)

    @property
    def center_position(self) -> Tuple[int, int]:
        """
        Center of sprite in world
        """
        return self.rect.center

    @center_position.setter
    def center_position(self, position: Tuple[int, int]):
        self.rect.center = position

    @property
    def rotation(self) -> float:
        """
        Rotation of image.

        Using pygame.transform.rotate() function
        """
        return self._rotation

    @rotation.setter
    def rotation(self, new_rotation: float):
        self._rotation = new_rotation
        self.image = pygame.transform.rotate(
            self._original_image, new_rotation)

    def reset_image_to_original(self):
        """
        Resets image to original image.

        Used in transformations methods
        """
        self.image = self._original_image

    def update_image_transformation(self):
        """
        Updates image with new transformations.

        Used in transformations methods
        """
        self.reset_image_to_original()
        self.image = pygame.transform.rotate(self.image, self._rotation)

    @property
    def layer(self) -> Union[int, float]:
        """
        Layer of sprite.

        Sprites with bigger layer will be rendered on top of sprites with small layers.
        """
        return self._layer

    @layer.setter
    def layer(self, value: Union[int, float]):
        self.game.set_sprite_layer(self, value)

    @property
    def visible(self) -> bool:
        """
        Visibility of sprite.
        """
        return self._visibility

    @visible.setter
    def visible(self, is_visible: bool):
        if is_visible:
            self.show()
        else:
            self.hide()

    def hide(self):
        """
        Hiding sprite
        """
        if not self._visibility:
            return
        self._visibility = False
        self.kill()

    def show(self):
        """
        Showing sprite
        """
        if self._visibility:
            return
        self._visibility = True
        self.game.add_sprite(self)


class SpriteWithCameraOffset(BaseSprite):
    """
    Combining position of sprite and camera position.

    Based on BaseSprite
    """

    def __init__(self, image, layer=0, start_position=(0, 0)) -> None:
        super().__init__(image, layer, start_position)
        self.base_position = start_position

    def update(self) -> None:
        """
        Updates sprite position depending on camera position
        """
        super().update()

        self.rect.center = (
            Vector2(self.base_position[0], self.base_position[1])
            - self.game._camera_position
        ).get_integer_tuple()

    @property
    def center_position(self) -> Tuple[int, int]:
        return self.base_position

    @center_position.setter
    def center_position(self, position: Tuple[int, int]):
        self.base_position = position


class FontSprite(BaseSprite):
    """
    Sprite for printing text
    """

    def __init__(self, text: str, color: Tuple[int, int, int], font: pygame.font.Font, layer=0, start_position=(0, 0)) -> None:
        super().__init__(pygame.Surface((0, 0)), layer, start_position)
        self.font = font

        self.set_text(text, color)

    def set_text(self, new_text: str, new_color: Tuple[int, int, int]):
        """
        Sets text of this sprite
        """
        # Getting size of surface
        text_size = self.font.size(new_text)

        # Creating new surface
        new_text_surface = pygame.Surface(text_size, pygame.SRCALPHA)
        new_text_surface.blit(self.font.render(
            new_text, 0, new_color), (0, 0))

        self.image = new_text_surface

    def set_font(self, new_font: pygame.font.Font):
        """
        Sets font of this spritee
        """
        self.font = new_font


class FontSpriteWithCameraOffset(FontSprite, SpriteWithCameraOffset):
    """
    Combined FontSprite and SpriteWithCameraOffset
    """

    def __init__(self, text: str, color: Tuple[int, int, int], font: pygame.font.Font, layer=0, start_position=(0, 0)) -> None:
        super().__init__(text, color, font, layer, start_position)


class AnimatedSprite(BaseSprite):
    """
    Sprite with looped changing images by delays.
    """

    def __init__(self, frames: List[pygame.Surface], frame_change_delay: float, layer=0, start_position=(0, 0)) -> None:
        """
        frame_change_delay - in seconds
        """

        super().__init__(frames[0], layer, start_position)

        self._frames = frames
        self._current_frame_index = 0
        self._frames_count = len(frames)
        self.frame_change_delay = frame_change_delay
        self._timer = 0.0

    @property
    def frames(self) -> List[pygame.Surface]:
        return self._frames

    @frames.setter
    def frames(self, new_value: List[pygame.Surface]):
        self._frames = new_value
        self._frames_count = len(new_value)
        self._current_frame_index = 0

    def update(self) -> None:
        super().update()

        self._timer += self.game.delta_time

        if self._timer >= self.frame_change_delay:
            self._timer = 0.0
            self._current_frame_index = (
                self._current_frame_index + 1) % self._frames_count

            self._original_image = self._frames[self._current_frame_index]
            self.update_image_transformation()


class AnimatedSpriteWithCameraOffset(AnimatedSprite, SpriteWithCameraOffset):
    """
    Combined AnimatedSprite and SpriteWithCameraOffset
    """

    def __init__(self, frames: List[pygame.Surface], frame_change_delay: float, layer=0, start_position=(0, 0)) -> None:
        super().__init__(frames, frame_change_delay, layer, start_position)

        self.base_position = start_position

    def update(self) -> None:
        super().update()
