from types import FunctionType
from typing import Tuple

import pygame
from pygame_entities.entities.mixins import SpriteMixin
from pygame_entities.utils.math import Vector2
from pygame_entities.utils.drawable import FontSprite


UI_LAYER = 100000


class Button(SpriteMixin):
    def __init__(
            self, position: Vector2,
            text: str,
            font: pygame.font.Font,
            on_lbm_callback: FunctionType = None,
            on_rbm_callback: FunctionType = None,
            color: Tuple[int, int, int] = (255, 255, 255),
            color_on_hover: Tuple[int, int, int] = (150, 150, 150)) -> None:
        super().__init__(position)

        self.text = text
        self._lbm_callback = on_lbm_callback
        self._rbm_callback = on_rbm_callback

        self._color = color
        self._color_on_hover = color_on_hover

        self.sprite_init(FontSprite(text, color, font, UI_LAYER))
        self.sprite: FontSprite

        self.collider_rect = pygame.Rect(
            self.position.x, self.position.y, self.sprite.image.get_width(), self.sprite.image.get_height())

        self.subscribe_on_update(self.on_hover)

        self.game.subsribe_for_event(
            self.on_mouse_click, pygame.MOUSEBUTTONDOWN)

        self._is_hovered = False

    def on_hover(self, _: float) -> None:
        if self.collider_rect.collidepoint(pygame.mouse.get_pos()):
            if self._is_hovered:
                return
            self._is_hovered = True
            self.sprite.set_text(self.text, self._color_on_hover)
        else:
            if not self._is_hovered:
                return
            self._is_hovered = False
            self.sprite.set_text(self.text, self._color)

    def on_mouse_click(self, event: pygame.event.Event) -> None:
        if not self.collider_rect.collidepoint(event.pos):
            return

        if event.button == 1:
            if not self._lbm_callback is None:
                self._lbm_callback()

        elif event.button == 3:
            if not self._rbm_callback is None:
                self._rbm_callback()


class Popup(SpriteMixin):
    def __init__(self, position: Vector2, text: str, font: pygame.font.Font, delete_seconds=5, color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        super().__init__(position)
        self.sprite_init(FontSprite(text, color, font, UI_LAYER))
        self.delete_second = delete_seconds
        self.timer = 0

        self.subscribe_on_update(self.on_update)

    def on_update(self, delta):
        self.timer += delta

        self.position -= Vector2(0, 1)

        if self.delete_second <= self.timer:
            self.destroy()
