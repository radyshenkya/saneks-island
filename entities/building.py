from typing import List
from entities.living_entities import LivingEntity
from entities.util_entities import OnMapSpriteMixin

import pygame
from items.item import Item, UsableItem
from pygame_entities.entities.entity import Entity
from pygame_entities.utils.drawable import SpriteWithCameraOffset
from pygame_entities.entities.mixins import CollisionMixin, MouseEventMixin
from pygame_entities.utils.math import Vector2


class BuildingItem(UsableItem):
    BUILDING: "Building" = None

    @classmethod
    def get_name(cls) -> str:
        return cls.BUILDING.NAME

    @classmethod
    def get_image(cls) -> pygame.Surface:
        return pygame.transform.scale(cls.BUILDING.IMAGE, (Vector2.from_tuple(cls.BUILDING.IMAGE.get_size()) / 1.5).get_integer_tuple())

    @classmethod
    def get_building_class(cls) -> "Building":
        return cls.BUILDING

    def use(self, initiator: Entity):
        a: "Building" = self.get_building_class()(initiator.position)
        self.amount -= 1


class Building(LivingEntity, OnMapSpriteMixin, CollisionMixin):
    IMAGE: pygame.Surface = None
    NAME = "BaseBuildingClass"
    HP = 1000
    IS_TRIGGER = False
    IS_USABLE = False

    def __init__(self, position: Vector2) -> None:
        super().__init__(position, self.HP)

        self.sprite_init(SpriteWithCameraOffset(self.IMAGE), Vector2())

        self.collision_init(Vector2.from_tuple(
            self.IMAGE.get_size()) / 4, self.IS_TRIGGER, self.IS_USABLE)

    def use(self, initiator: Entity):
        raise NotImplementedError("Building's use() needs to be implemented")

    @classmethod
    def get_item_class(cls) -> BuildingItem:
        class NewBuildingItem(BuildingItem):
            BUILDING = cls

        return NewBuildingItem

    def get_loot(self) -> List["Item"]:
        return [self.get_item_class()(1)]
