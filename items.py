import pickle
from assets import Sprites


class Item:
    NAME = "BaseItemClass"
    IMAGE = Sprites.BAG
    MAX_AMOUNT = 10

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
        for slot, item_in_inv in enumerate(self.grid):
            if type(item) is type(item_in_inv):
                fill_amount = min(item_in_inv.MAX_AMOUNT -
                                  item_in_inv.amount, item.amount)
                item_in_inv.amount += fill_amount
                item.amount -= fill_amount

                if item.amount <= 0:
                    break
            elif item_in_inv is None:
                self.grid[slot] = item
                break
        else:
            return item

        return None

    def set_slot(self, item: Item | None, index: int):
        self.grid[index] = item

    def get_slot(self, index: int) -> Item | None:
        return self.grid[index]

    def swap_slot(self, slot_index: int, item: Item | None) -> Item | None:
        previous_item = self.get_slot(slot_index)
        self.set_slot(item, slot_index)
        return previous_item


class Wood(Item):
    NAME = 'Wood'
    IMAGE = Sprites.WOOD


class Leaves(Item):
    NAME = 'Leaves'
    IMAGE = Sprites.LEAVES


class Rock(Item):
    NAME = 'Rock'
    IMAGE = Sprites.ROCK


class Coal(Item):
    NAME = 'Coal'
    IMAGE = Sprites.COAL


class Iron(Item):
    NAME = 'Iron'
    IMAGE = Sprites.IRON


class Gold(Item):
    NAME = 'Gold'
    IMAGE = Sprites.GOLD


class IronIngot(Item):
    NAME = 'Iron Ingot'
    IMAGE = Sprites.IRON_INGOT


class GoldIngot(Item):
    NAME = 'Gold Ingot'
    IMAGE = Sprites.GOLD_INGOT


class Amethyst(Item):
    NAME = 'Amethyst'
    IMAGE = Sprites.AMETHYST


class Feather(Item):
    NAME = 'Feather'
    IMAGE = Sprites.BAG  # TODO: add image


class String(Item):
    NAME = 'String'
    IMAGE = Sprites.STRING


class Arrow(Item):
    NAME = 'Arrow'
    IMAGE = Sprites.BAG  # TODO: add image


class RawMeat(ConsumableItem):
    NAME = 'Raw Meat'
    IMAGE = Sprites.BAG  # TODO: add image


class CookedMeat(ConsumableItem):
    NAME = 'Cooked Meat'
    IMAGE = Sprites.BAG  # TODO: add image


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
