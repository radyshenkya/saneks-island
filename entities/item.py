import pygame
from assets import FONT_PATH
from items import Item
from entities.ui import Popup
from pygame_entities.entities.mixins import SpriteMixin
from pygame_entities.utils.math import Vector2
from pygame_entities.utils.drawable import SpriteWithCameraOffset


class ItemEntity(SpriteMixin):
    def __init__(self, position: Vector2, item: Item) -> None:
        super().__init__(position)

        self._item = item
        self.sprite_init(SpriteWithCameraOffset(
            self.item.get_image(), 0), Vector2())

    @property
    def item(self) -> Item:
        return self._item

    @item.setter
    def item(self, new_value: Item | None):
        self._item = new_value
        self.update_item()

    def update_item(self):
        if self.item is None or self.item.amount <= 0:
            self.destroy()
            Popup(self.position, "Picked up!",
                  pygame.font.Font(FONT_PATH, 25), False, 2)
