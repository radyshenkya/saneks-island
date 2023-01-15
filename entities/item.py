import pygame
from assets import FONT_PATH
from items import Item
from entities.ui import Popup
from entities.util_entities import OnMapSpriteMixin
from pygame_entities.utils.math import Vector2
from pygame_entities.utils.drawable import SpriteWithCameraOffset


class ItemEntity(OnMapSpriteMixin):

    def __init__(self, position: Vector2, item: Item) -> None:
        super().__init__(position)

        self._item = item
        self.sprite_init(SpriteWithCameraOffset(self.item.IMAGE), Vector2())

    @property
    def item(self) -> Item:
        return self._item

    @item.setter
    def item(self, new_value: Item | None):
        if new_value is None:
            self.destroy()
            Popup(self.position, f"{self._item.NAME}",
                  pygame.font.Font(FONT_PATH, 25), False, 2)

        self._item = new_value
