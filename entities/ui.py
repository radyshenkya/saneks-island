from types import FunctionType
from typing import List, Tuple

import pygame
from pygame_entities.entities.entity import Entity
from pygame_entities.entities.mixins import SpriteMixin
from pygame_entities.utils.math import Vector2
from pygame_entities.utils.drawable import FontSprite, FontSpriteWithCameraOffset, BaseSprite


UI_LAYER = 100000


class Image(SpriteMixin):
    def __init__(self, position: Vector2, image: pygame.Surface, layer=UI_LAYER, rescale_ratio=(1, 1)) -> None:
        super().__init__(position)
        new_image = pygame.transform.scale(image, (image.get_width(
        ) * rescale_ratio[0], image.get_height() * rescale_ratio[1]))

        print(position)

        self.sprite_init(BaseSprite(new_image, layer=layer))


class Button(SpriteMixin):
    def __init__(
            self, position: Vector2,
            text: str,
            font: pygame.font.Font,
            on_lbm_callback: FunctionType = None,
            on_rbm_callback: FunctionType = None,
            color: Tuple[int, int, int] = (255, 255, 255),
            color_on_hover: Tuple[int, int, int] = (150, 150, 150),
            layer=UI_LAYER) -> None:
        super().__init__(position)

        self.text = text
        self._lbm_callback = on_lbm_callback
        self._rbm_callback = on_rbm_callback

        self._color = color
        self._color_on_hover = color_on_hover

        self.sprite_init(FontSprite(text, color, font, layer))
        self.sprite: FontSprite

        self.collider_rect = pygame.Rect(
            self.position.x, self.position.y, self.sprite.image.get_width(), self.sprite.image.get_height())

        self.subscribe_on_update(self.on_hover)

        self.subscribe_for_event(
            self.on_mouse_click, pygame.MOUSEBUTTONDOWN)

        self._is_hovered = False

    def on_hover(self, _: float) -> None:
        self.collider_rect = pygame.Rect(
            self.position.x, self.position.y, self.sprite.image.get_width(), self.sprite.image.get_height())

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

        self.game.subscribe_for_event(self.on_key_pressed, pygame.KEYDOWN)

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
    def __init__(self, position: Vector2, text: str, font: pygame.font.Font, is_screen_position=True, delete_seconds=5, color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        super().__init__(position)
        if is_screen_position:
            self.sprite_init(FontSprite(text, color, font, UI_LAYER))
        else:
            self.sprite_init(FontSpriteWithCameraOffset(
                text, color, font, UI_LAYER))
        self.delete_second = delete_seconds
        self.timer = 0

        self.subscribe_on_update(self.on_update)

    def on_update(self, delta):
        self.timer += delta

        self.position -= Vector2(0, 1)

        if self.delete_second <= self.timer:
            self.destroy()


class UIElementsContainer(Entity):
    def __init__(self, position: Vector2):
        super().__init__(position)

        self.ui_elements: List[SpriteMixin] = list()
        self.subscribe_on_destroy(self.hide)
        self.is_visible = False

    def _pre_render(self):
        self.hide()
        self.is_visible = True

    def render(self):
        """
        Для реализации
        """
        self._pre_render()
        pass

    def add_element(self, new_elem: SpriteMixin, add_position=True):
        if add_position:
            new_elem.position += self.position
        self.ui_elements.append(new_elem)

    def hide(self):
        if not self.is_visible:
            return

        self.is_visible = False
        for el in self.ui_elements:
            el.destroy()

        self.ui_elements = []


class ActionsPanel(UIElementsContainer):
    def __init__(self, position: Vector2, panel_name: str, actions, font: pygame.font.Font, background_color=(200, 200, 200)):
        super().__init__(position)
        self.name = panel_name
        self.actions = actions
        self.font = font
        self.bg_color = background_color

        self.calculate_panel_box()
        self.game.subscribe_for_event(
            self.on_mouse_click, pygame.MOUSEBUTTONDOWN)

    def add_action(self, action_name, action_callback):
        def destroy_after_action_callback():
            action_callback()
            self.destroy()

        self.actions[action_name] = destroy_after_action_callback

    def calculate_panel_box(self):
        width = max([el.sprite.image.get_width()
                    for el in self.ui_elements] + [1])
        height = sum([el.sprite.image.get_height()
                     for el in self.ui_elements] + [1])

        self.calculated_panel_box = pygame.Rect(
            self.position.x, self.position.y, width, height)

    def render(self):
        super().render()

        self.add_element(
            Button(Vector2(), self.name, self.font, layer=UI_LAYER + 1)
        )

        for i, el in enumerate(self.actions.items()):
            self.add_element(
                Button(Vector2(0, (i + 1) * self.font.get_height()), el[0], self.font, el[1], layer=UI_LAYER + 1))

        self.calculate_panel_box()

        new_rect = SpriteMixin(
            Vector2().from_tuple(self.calculated_panel_box.size) / 2)
        new_rect.sprite_init(BaseSprite(pygame.Surface(
            self.calculated_panel_box.size), UI_LAYER))

        new_rect.sprite.image.fill(self.bg_color)

        self.add_element(new_rect)

    def on_mouse_click(self, event: pygame.event.Event) -> None:
        if not self.calculated_panel_box.collidepoint(event.pos):
            self.destroy()
