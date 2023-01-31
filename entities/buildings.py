from functools import partial
from typing import List

import pygame
from assets import FONT_PATH, Sprites
from entities.building import Building
from entities.item import ItemEntity
from entities.ui import ActionsPanel, Popup
from items.items import IronIngot, Wood
from items.recipes import Recipe
from items.inventory import Inventory
from items.item import Item
from pygame_entities.entities.entity import Entity
from pygame_entities.utils.math import Vector2

FONT = pygame.font.Font(FONT_PATH, 30)


class Chest(Building):
    """Сущность сундука"""
    IMAGE = Sprites.CHEST
    NAME = "Chest"
    HP = 1000
    IS_TRIGGER = True
    IS_USABLE = True

    SLOT_COUNT = 10
    ITEMS_PICKUP_RADIUS = 64

    def __init__(self, position: Vector2) -> None:
        self.inventory = Inventory(self.SLOT_COUNT)
        super().__init__(position)

    def use(self, _: Entity):
        action_list = ActionsPanel(
            Vector2.from_tuple(pygame.mouse.get_pos()), "Chest Actions", {}, FONT)

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

    def get_loot(self) -> List["Item"]:
        return super().get_loot() + list(filter(lambda x: not x is None, self.inventory.grid))


class Workbench(Building):
    """Верстак. Так же от него можно наследовать другие строения для крафтов."""

    IMAGE = Sprites.WORKBENCH
    NAME = "Workbench"
    HP = 1000

    IS_TRIGGER = True
    IS_USABLE = True

    ITEMS_PICKUP_RADIUS = 64

    RECIPES = [
        Recipe("Chest", {Wood: 1, IronIngot: 1}, {Chest.get_item_class(): 1}),
        Recipe("Transform wood to iron ingot", {
               Wood: 1}, {IronIngot: 1})
    ]

    def use(self, _: Entity):
        action_list = ActionsPanel(
            Vector2.from_tuple(pygame.mouse.get_pos()), f"{self.NAME} Crafts", {}, FONT)

        for recipe in self.RECIPES:
            action_list.add_action(
                f"{recipe.name}", partial(self.craft, recipe))

        action_list.render()

    def craft(self, recipe: Recipe):
        nearby_item_ents = self.count_nearby_items()
        nearby_items = [el.item for el in nearby_item_ents]

        is_valid, needs_ingr, amount = recipe.is_enough_ingredients(
            nearby_items)

        if not is_valid:
            Popup(
                self.position, f"Not enough {needs_ingr.get_name()}. Needed amount - {amount}", FONT)
            return

        res, _ = recipe.craft(nearby_items)

        [el.update_item() for el in nearby_item_ents]

        for result_item in res:
            ItemEntity(self.position, result_item)

        Popup(
            self.position, f"{recipe.name}", FONT)

    def count_nearby_items(self) -> List["ItemEntity"]:
        return [ent for ent in self.game.enabled_entities
                if type(ent) == ItemEntity and
                (ent.position - self.position).magnitude() <= self.ITEMS_PICKUP_RADIUS
                ]
