from typing import List
from entities.living_entities import LivingEntity
from entities.ui import Popup
from entities.util_entities import OnMapSpriteMixin
import assets

import pygame
from items.item import Item, UsableItem
from pygame_entities.entities.entity import Entity
from pygame_entities.utils.drawable import SpriteWithCameraOffset
from pygame_entities.entities.mixins import CollisionMixin, MouseEventMixin
from pygame_entities.utils.math import Vector2


def snap_position_to_grid(position: Vector2) -> Vector2:
    return ((position) + (Vector2.from_tuple(assets.SPRITE_SIZE) // 2)) // \
        assets.SPRITE_SIZE[0] * \
        assets.SPRITE_SIZE[0]


class BuildingItem(UsableItem):
    BUILDING: "Building" = None
    MAX_BUILDING_RANGE = assets.SPRITE_SIZE[0] * 3

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
        """Создает выбранную постройку на месте курсора"""
        spawn_position = snap_position_to_grid(initiator.game.from_screen_to_world_point(
            Vector2.from_tuple(pygame.mouse.get_pos())))

        if (initiator.position - spawn_position).magnitude() > self.MAX_BUILDING_RANGE:
            Popup(spawn_position, "Too far!", assets.FONT_30, False)
            return

        if any(map(lambda x: (x.position - spawn_position).magnitude() <= assets.SPRITE_SIZE[0] / 1.5, filter(lambda x: isinstance(x, CollisionMixin), initiator.game.enabled_entities))):
            Popup(spawn_position, "Need more space to build!",
                  assets.FONT_30, False)
            return

        a: "Building" = self.get_building_class()(spawn_position)
        self.amount -= 1


class Building(LivingEntity, OnMapSpriteMixin, CollisionMixin):
    IMAGE: pygame.Surface = None
    NAME = "BaseBuildingClass"
    HP = 1000
    IS_TRIGGER = False
    IS_USABLE = False

    COLLISION_BOX = None

    def __init__(self, position: Vector2) -> None:
        super().__init__(position, self.HP)

        self.sprite_init(SpriteWithCameraOffset(self.IMAGE), Vector2())

        self.collision_init((Vector2.from_tuple(
            self.IMAGE.get_size()) / 2 if self.COLLISION_BOX is None else self.COLLISION_BOX), self.IS_TRIGGER, self.IS_USABLE)

    def use(self, initiator: Entity):
        raise NotImplementedError("Building's use() needs to be implemented")

    @ classmethod
    def get_item_class(cls) -> BuildingItem:
        class NewBuildingItem(BuildingItem):
            BUILDING = cls

        return NewBuildingItem

    def get_loot(self) -> List["Item"]:
        return [self.get_item_class()(1)]
