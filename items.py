import pickle
import os
from assets import Sprites


class Item:
    NAME = "BaseItemClass"

    def __init__(self, amount: int) -> None:
        self.amount = amount


class UsableItem(Item):
    def __init__(self, amount: int, durability: float) -> None:
        self.amount = amount
        self.durability = durability

    def use(self):
        self.durability -= 0


class ConsumableItem(Item):
    def __init__(self, amount: int) -> None:
        self.amount = amount

    def use(self):
        self.amount -= 1


class PlaceableItem(Item):
    def __init__(self, amount: int) -> None:
        self.amount = amount

    def use(self):
        self.amount -= 1


class Inventory:
    def __init__(self, slots_count: int = 10) -> None:
        self.slots = slots_count
        self.grid = [None for _ in range(self.slots)]

    def save(self):
        with open('inventory.inv', 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load():
        try:
            with open('inventory.inv', 'rb') as f:
                return pickle.load(f)
        except Exception:
            return Inventory()

    def add_item(self, item: Item) -> Item:
        """
        Добавляет предмет в инвентарь. Возвращает None,
        если поместилось все количество,
        иначе возвращает оставшиеся предметы.
        """
        for elem, index in zip(self.grid, range(len(self.grid))):
            if elem is None:
                self.grid[index] = item
                return None
            if elem.NAME == item.NAME:
                free_space = elem.MAX_AMOUNT - elem.amount
                if item.amount <= free_space:
                    elem.amount += item.amount
                    return None
                else:
                    elem.amount = elem.MAX_AMOUNT
                    item.amount -= free_space
            if item.amount == 0:
                return None
        return item

    def set_slot(self, item: Item, index: int):
        self.grid[index] = item

    def get_slot(self, index: int) -> Item:
        return self.grid[index]

    def swap_slot(self, slot_index: int, item: Item) -> Item | None:
        previous_item = self.grid[slot_index]
        self.grid[slot_index] = item
        return previous_item


class Wood(Item):
    NAME = 'Wood'
    MAX_AMOUNT = 10
    IMAGE = Sprites.WOOD


class Leaves(Item):
    NAME = 'Leaves'
    MAX_AMOUNT = 10
    IMAGE = Sprites.LEAVES


class Rock(Item):
    NAME = 'Rock'
    MAX_AMOUNT = 10
    IMAGE = Sprites.ROCK


class Coal(Item):
    NAME = 'Coal'
    MAX_AMOUNT = 10
    IMAGE = Sprites.COAL


class Iron(Item):
    NAME = 'Iron'
    MAX_AMOUNT = 10
    IMAGE = Sprites.IRON


class Gold(Item):
    NAME = 'Gold'
    MAX_AMOUNT = 10
    IMAGE = Sprites.GOLD


class IronIngot(Item):
    NAME = 'Iron Ingot'
    MAX_AMOUNT = 10
    IMAGE = Sprites.IRON_INGOT


class GoldIngot(Item):
    NAME = 'Gold Ingot'
    MAX_AMOUNT = 10
    IMAGE = Sprites.GOLD_INGOT


class Amethyst(Item):
    NAME = 'Amethyst'
    MAX_AMOUNT = 10
    IMAGE = Sprites.AMETHYST


class Feather(Item):
    NAME = 'Feather'
    MAX_AMOUNT = 10
    IMAGE = Sprites.BAG  # TODO: add feather image


class String(Item):
    NAME = 'String'
    MAX_AMOUNT = 10
    IMAGE = Sprites.STRING


class Arrow(Item):
    NAME = 'Arrow'
    MAX_AMOUNT = 10
    IMAGE = Sprites.ARROW


class RawMeat(ConsumableItem):
    NAME = 'Raw Meat'
    MAX_AMOUNT = 10
    IMAGE = Sprites.RAW_MEAT


class CookedMeat(ConsumableItem):
    NAME = 'Cooked Meat'
    MAX_AMOUNT = 10
    IMAGE = Sprites.COOKED_MEAT


class WoodenSword(UsableItem):
    pass


class StoneSword(UsableItem):
    pass


class IronSword(UsableItem):
    pass


class GoldenSword(UsableItem):
    pass


class AmethystSword(UsableItem):
    pass


class Bow(UsableItem):
    pass
