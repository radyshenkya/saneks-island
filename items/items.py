from assets import Sprites
from items.item import Item, UsableItem


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


class RawMeat(UsableItem):
    NAME = 'Raw Meat'
    IMAGE = Sprites.BAG  # TODO: add image


class CookedMeat(UsableItem):
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
