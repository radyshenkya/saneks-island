from functools import partial
from assets import FONT_PATH, Sprites
from entities.item import ItemEntity
from entities.living_entities import LivingEntity
from entities.map import Map
from entities.ui import ActionsPanel
from entities.util_entities import OnMapSpriteMixin

import pygame
from items import Inventory
from pygame_entities.utils.drawable import SpriteWithCameraOffset
from pygame_entities.entities.mixins import MouseEventMixin, CollisionMixin

from pygame_entities.utils.math import Vector2


class Building(LivingEntity, OnMapSpriteMixin, MouseEventMixin):
    IMAGE: pygame.Surface = None
    NAME = "BaseBuildingClass"
    HP = 1000
    IS_TRIGGER = False
    IS_USABLE = False

    def __init__(self, position: Vector2, map: Map) -> None:
        super().__init__(position, self.HP, map)

        self.sprite_init(SpriteWithCameraOffset(self.IMAGE), Vector2())

        self.collision_init(Vector2.from_tuple(
            self.IMAGE.get_size()) / 2, self.IS_TRIGGER, self.IS_USABLE)

        if self.IS_USABLE:
            self.mouse_events_init()

            def on_click(btn):
                if btn == 1:
                    self.use()

            self.subscribe_on_mouse_down(on_click)

    def use(self):
        raise NotImplementedError("Building's use() needs to be implemented")


class ChestEntity(Building):
    """Сущность сундука"""
    IMAGE = Sprites.CHEST
    NAME = "Chest"
    HP = 1000
    IS_TRIGGER = True
    IS_USABLE = True

    FONT_SIZE = 30
    FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)

    SLOT_COUNT = 10
    ITEMS_PICKUP_RADIUS = 64

    def __init__(self, position: Vector2, map: Map) -> None:
        super().__init__(position, map)
        self.inventory = Inventory(self.SLOT_COUNT)

    def use(self):
        action_list = ActionsPanel(
            Vector2.from_tuple(pygame.mouse.get_pos()), "Chest Actions", {}, self.FONT)

        action_list.add_action("Pick nearest items", self.pick_nearest_items)

        for i, item in enumerate(self.inventory.grid):
            if item is None:
                continue

            action_list.add_action(
                f"Drop {item.NAME} x{item.amount}", partial(self.drop_item, i))

        action_list.render()

    def pick_nearest_items(self):
        for ent in self.game.enabled_entities:
            if not type(ent) == ItemEntity or (ent.position - self.position).magnitude() > self.ITEMS_PICKUP_RADIUS:
                continue

            ent: ItemEntity
            ent.item = self.inventory.add_item(ent.item)

    def drop_item(self, slot_index: int):
        item = self.inventory.get_slot(slot_index)

        if item is None:
            return

        ItemEntity(self.position, self.inventory.swap_slot(slot_index, None))
