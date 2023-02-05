import pygame
from assets import FONT_PATH
from entities.json_parser import json_dict_into_object, register_json
from items import Item
from entities.ui import Popup
from pygame_entities.entities.mixins import SpriteMixin
from pygame_entities.utils.math import Vector2
from pygame_entities.utils.drawable import SpriteWithCameraOffset


@register_json
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

    def to_json(self) -> dict:
        return {'type': self.__class__.__name__, 'position': self.position.get_tuple(), 'item': self.item.to_json()}

    @classmethod
    def from_json(cls, json_dict: dict) -> "ItemEntity":
        return cls(Vector2.from_tuple(json_dict['position']), json_dict_into_object(json_dict['item']))
