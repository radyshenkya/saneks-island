from functools import partial

import pygame
from assets import FONT_PATH, Sprites
from entities.building import Building, BuildingItem
from entities.item import ItemEntity
from entities.ui import ActionsPanel
from items.inventory import Inventory
from pygame_entities.entities.entity import Entity
from pygame_entities.utils.math import Vector2


class Chest(Building):
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

    def __init__(self, position: Vector2) -> None:
        self.inventory = Inventory(self.SLOT_COUNT)
        super().__init__(position)

    def use(self, _: Entity):
        action_list = ActionsPanel(
            Vector2.from_tuple(pygame.mouse.get_pos()), "Chest Actions", {}, self.FONT)

        action_list.add_action("Pick nearest items", self.pick_nearest_items)

        for i, item in enumerate(self.inventory.grid):
            if item is None:
                continue

            action_list.add_action(
                f"Drop {item.get_name()} x{item.amount}", partial(self.drop_item, i))

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


class ChestItem(BuildingItem):
    BUILDING = Chest
