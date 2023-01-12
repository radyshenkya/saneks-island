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


# TODO: он исчезает почему то когда в его начало наводишься, если текста нет, надо бы пофиксить, но чет сейчас леньы
class InputField(Button):
    def __init__(self,
                 position: Vector2,
                 text: str,
                 font: pygame.font.Font,
                 max_length: int = 20,
                 placeholder_text: str = "",
                 color: Tuple[int, int, int] = (255, 255, 255),
                 color_on_hover: Tuple[int, int, int] = (150, 150, 150),
                 active_color: Tuple[int, int, int] = (200, 200, 200)) -> None:
        super().__init__(position, text, font, self.on_click,
                         self.on_click, color, color_on_hover)

        self.text_color = color
        self.placeholder_text = placeholder_text
        self.placeholder_color = color_on_hover
        self.active_color = active_color
        self.max_length = max_length
        self.is_focused = False

        self.game.subsribe_for_event(self.on_key_pressed, pygame.KEYDOWN)

        self.text_update()

    def on_click(self):
        self.set_focus(True)

    def on_key_pressed(self, event: pygame.event.Event):
        if not self.is_focused:
            return

        elif event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE:
            self.set_focus(False)
            return

        elif event.key == pygame.K_BACKSPACE:
            if len(self.text) > 0:
                self.text = self.text[:-1]
                self.text_update()

        elif len(self.text) < self.max_length:
            self.text += event.unicode
            self.text_update()

    def set_focus(self, state: bool):
        if not state:
            self.is_focused = False
            self._color = self.text_color
            self.text_update()
            return

        self.is_focused = True
        self._color = self.active_color

        self.text_update()

    def text_update(self):
        if len(self.text) == 0:
            self._color_on_hover = self.placeholder_color
            self.sprite.set_text(self.placeholder_text, self.placeholder_color)
        else:
            self.sprite.set_text(self.text, self._color)

        self.collider_rect = pygame.Rect(
            self.position.x, self.position.y, self.sprite.image.get_width(), self.sprite.image.get_height())


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
