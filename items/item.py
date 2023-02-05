from typing import Dict
import pygame
from pygame_entities.entities.entity import Entity
from pygame_entities.entities.mixins import SpriteMixin
from pygame_entities.utils.math import Vector2


class Item:
    NAME = "BaseItemClass"
    IMAGE = None
    MAX_AMOUNT = 10

    def __init__(self, amount: int) -> None:
        self.amount = amount

    def is_valid(self) -> bool:
        if self.amount >= 1:
            return True

        return False

    @classmethod
    def get_max_amount(cls) -> str:
        return cls.MAX_AMOUNT

    @classmethod
    def get_name(cls) -> str:
        return cls.NAME

    @classmethod
    def get_image(cls) -> pygame.Surface:
        return pygame.transform.scale(cls.IMAGE, (Vector2.from_tuple(cls.IMAGE.get_size()) / 1.5).get_integer_tuple())

    def to_json(self) -> dict:
        return {'type': self.__class__.__name__, 'amount': self.amount}

    @classmethod
    def from_json(cls, json_dict: dict) -> "Item":
        return cls(json_dict['amount'])


class UsableItem(Item):
    def use(self, initiator: Entity):
        raise NotImplementedError("use() method needs to be implemented")
