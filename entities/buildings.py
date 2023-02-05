from functools import partial
from random import randint
from typing import List

import pygame
from assets import SPRITE_SIZE, Sprites, FONT_30 as FONT
from entities.building import Building
from entities.item import ItemEntity
from entities.ui import ActionsPanel, Popup
from items.items import BaseAxe, BasePickaxe, Coal, Gold, GoldIngot, GoldenAxe, GoldenPickaxe, GoldenSword, Iron, IronAxe, IronIngot, IronPickaxe, IronSword, Rock, StoneAxe, Wood, WoodenAxe, WoodenPickaxe, WoodenSword, StoneSword, StonePickaxe
from items.recipes import Recipe
from items.inventory import Inventory
from items.item import Item
from pygame_entities.entities.entity import Entity
from pygame_entities.utils.math import Vector2

BUILDINGS_ITEMS_PICKUP_RADIUS = 128

WORKBENCH_RECIPES = [
    Recipe("Wooden Pickaxe", {Wood: 3}, {WoodenPickaxe: 1}),
    Recipe("Wooden Sword", {Wood: 3}, {WoodenSword: 1}),
    Recipe("Wooden Axe", {Wood: 3}, {WoodenAxe: 1}),
    Recipe("Stone Pickaxe", {Wood: 1, Rock: 2}, {StonePickaxe: 1}),
    Recipe("Stone Sword", {Wood: 1, Rock: 2}, {StoneSword: 1}),
    Recipe("Stone Axe", {Wood: 1, Rock: 2}, {StoneAxe: 1}),
    Recipe("Iron Pickaxe", {Wood: 1, IronIngot: 2}, {IronPickaxe: 1}),
    Recipe("Iron Sword", {Wood: 1, IronIngot: 2}, {IronSword: 1}),
    Recipe("Iron Axe", {Wood: 1, IronIngot: 2}, {IronAxe: 1}),
    Recipe("Golden Pickaxe", {Wood: 1, GoldIngot: 2}, {GoldenPickaxe: 1}),
    Recipe("Golden Sword", {Wood: 1, GoldIngot: 2}, {GoldenSword: 1}),
    Recipe("Golden Axe", {Wood: 1, GoldIngot: 2}, {GoldenAxe: 1})
]

FURNACE_RECIPES = [
    Recipe("Iron Ingot", {Iron: 1, Coal: 1}, {IronIngot: 1}),
    Recipe("Gold Ingot", {Gold: 1, Coal: 1}, {GoldIngot: 1}),
]


class Chest(Building):
    """Сущность сундука"""
    IMAGE = Sprites.CHEST
    NAME = "Chest"
    HP = 5
    IS_TRIGGER = False
    IS_USABLE = True

    ON_HURT_PARTICLE_IMAGE = Sprites.WOOD_PARTICLE

    SLOT_COUNT = 10
    ITEMS_PICKUP_RADIUS = BUILDINGS_ITEMS_PICKUP_RADIUS

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


WORKBENCH_RECIPES.append(
    Recipe("Chest", {Wood: 1, IronIngot: 1}, {Chest.get_item_class(): 1}))


class WoodenCrate(Building):
    """Коробка. Просто коробка"""

    IMAGE = Sprites.CRATE_WOOD
    NAME = "Wooden Crate"
    HP = 20

    IS_USABLE = False
    IS_TRIGGER = False

    ON_HURT_PARTICLE_IMAGE = Sprites.WOOD_PARTICLE


WORKBENCH_RECIPES.append(
    Recipe('Wooden Crate', {Wood: 5}, {WoodenCrate.get_item_class(): 1})
)


class Workbench(Building):
    """Верстак. Так же от него можно наследовать другие строения для крафтов."""

    IMAGE = Sprites.WORKBENCH
    NAME = "Workbench"
    HP = 5

    ON_HURT_PARTICLE_IMAGE = Sprites.WOOD_PARTICLE

    IS_TRIGGER = False
    IS_USABLE = True

    ITEMS_PICKUP_RADIUS = BUILDINGS_ITEMS_PICKUP_RADIUS

    RECIPES = WORKBENCH_RECIPES

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
                self.position, f"Not enough {needs_ingr.get_name()}. Needed amount - {amount}", FONT, False)
            return

        res, _ = recipe.craft(nearby_items)

        [el.update_item() for el in nearby_item_ents]

        for result_item in res:
            ItemEntity(self.position, result_item)

        Popup(
            self.position, f"{recipe.name}", FONT, False)

    def count_nearby_items(self) -> List["ItemEntity"]:
        return [ent for ent in self.game.enabled_entities
                if type(ent) == ItemEntity and
                (ent.position - self.position).magnitude() <= self.ITEMS_PICKUP_RADIUS
                ]


class BasicWorkbench(Workbench):
    """Базовый стол крафта, что бы можно было скрафтить верстак"""
    IMAGE = Sprites.WOOD_LOG_LAYING
    NAME = 'Crafting Log'
    ITEMS_PICKUP_RADIUS = BUILDINGS_ITEMS_PICKUP_RADIUS
    HP = 1
    COLLISION_BOX = Vector2.from_tuple(SPRITE_SIZE) / 1.5
    RECIPES = [
        Recipe('Workbench', {Wood: 3}, {Workbench.get_item_class(): 1})
    ]


class Furnace(Workbench):
    IMAGE = Sprites.FURNACE
    NAME = 'Furnace'
    ITEMS_PICKUP_RADIUS = BUILDINGS_ITEMS_PICKUP_RADIUS
    RECIPES = FURNACE_RECIPES
    IS_TRIGGER = False

    ON_HURT_PARTICLE_IMAGE = Sprites.STONE_PARTICLE


WORKBENCH_RECIPES.append(
    Recipe("Furnace", {Rock: 5}, {Furnace.get_item_class(): 1}))


# NATURAL BUILDINGS


class Tree(Building):
    """Дерево"""
    IMAGE = Sprites.PALMTREE_2
    NAME = "Palm Tree"
    HP = 5

    ON_HURT_PARTICLE_IMAGE = Sprites.WOOD_PARTICLE

    IS_TRIGGER = False
    IS_USABLE = False

    MIN_AXE_POWER = 1

    COLLISION_BOX = Vector2.from_tuple(SPRITE_SIZE) / 2

    # Включаем урон только от кирки
    def add_hp(self, hp: int, initiator: Entity):
        if not isinstance(initiator, BaseAxe):
            return

        if initiator.POWER < self.MIN_AXE_POWER:
            return

        super().add_hp(hp)

    def get_loot(self) -> List["Item"]:
        return [
            Wood(1) for _ in range(randint(1, 6))
        ] + [
            BasicWorkbench.get_item_class()(1) for _ in range(randint(0, 1))
        ]


class Stone(Building):
    """Камень"""
    IMAGE = Sprites.STONE
    NAME = "Stone"
    HP = 5

    ON_HURT_PARTICLE_IMAGE = Sprites.STONE_PARTICLE

    IS_TRIGGER = False
    IS_USABLE = False

    MIN_PICKAXE_POWER = 1

    # Включаем урон только от кирки
    def add_hp(self, hp: int, initiator: Entity):
        if not isinstance(initiator, BasePickaxe):
            return

        if initiator.POWER < self.MIN_PICKAXE_POWER:
            return

        super().add_hp(hp)

    def get_loot(self) -> List["Item"]:
        return [
            Rock(1) for _ in range(randint(1, 6))
        ]


class StoneWithIron(Stone):
    IMAGE = Sprites.STONE_WITH_IRON_2
    NAME = "Stone with Iron"
    HP = 7
    MIN_PICKAXE_POWER = 2

    def get_loot(self) -> List["Item"]:
        return [
            Rock(1) for _ in range(randint(1, 3))
        ] + [
            Iron(1) for _ in range(randint(1, 3))
        ]


class StoneWithGold(Stone):
    IMAGE = Sprites.STONE_WITH_GOLD
    NAME = "Stone with Gold"
    HP = 7
    MIN_PICKAXE_POWER = 2

    def get_loot(self) -> List["Item"]:
        return [
            Rock(1) for _ in range(randint(1, 3))
        ] + [
            Gold(1) for _ in range(randint(1, 3))
        ]


class StoneWithCoal(Stone):
    IMAGE = Sprites.STONE_WITH_COAL
    NAME = "Stone with Coal"
    HP = 7
    MIN_PICKAXE_POWER = 2

    def get_loot(self) -> List["Item"]:
        return [
            Rock(1) for _ in range(randint(1, 3))
        ] + [
            Coal(1) for _ in range(randint(1, 3))
        ]
