from typing import TYPE_CHECKING
import pygame
from assets import Sprites
from entities.json_parser import register_json
from entities.util_entities import OnMapSpriteMixin
from items.item import Item, UsableItem
from pygame_entities.entities.entity import Entity
from pygame_entities.entities.mixins import SpriteMixin
from pygame_entities.utils.drawable import AnimatedSpriteWithCameraOffset
from pygame_entities.utils.math import Vector2
# from entities.living_entities import LivingEntity


@register_json
class Wood(Item):
    NAME = 'Wood'
    IMAGE = Sprites.WOOD


@register_json
class Leaves(Item):
    NAME = 'Leaves'
    IMAGE = Sprites.LEAVES


@register_json
class Rock(Item):
    NAME = 'Rock'
    IMAGE = Sprites.ROCK


@register_json
class Coal(Item):
    NAME = 'Coal'
    IMAGE = Sprites.COAL


@register_json
class Iron(Item):
    NAME = 'Iron'
    IMAGE = Sprites.IRON


@register_json
class Gold(Item):
    NAME = 'Gold'
    IMAGE = Sprites.GOLD


@register_json
class IronIngot(Item):
    NAME = 'Iron Ingot'
    IMAGE = Sprites.IRON_INGOT


@register_json
class GoldIngot(Item):
    NAME = 'Gold Ingot'
    IMAGE = Sprites.GOLD_INGOT


@register_json
class Amethyst(Item):
    NAME = 'Amethyst'
    IMAGE = Sprites.AMETHYST


@register_json
class Feather(Item):
    NAME = 'Feather'
    IMAGE = Sprites.BAG  # TODO: add image


@register_json
class String(Item):
    NAME = 'String'
    IMAGE = Sprites.STRING


@register_json
class Arrow(Item):
    NAME = 'Arrow'
    IMAGE = Sprites.BAG  # TODO: add image


@register_json
class RawMeat(UsableItem):
    NAME = 'Raw Meat'
    IMAGE = Sprites.RAW_MEAT


@register_json
class CookedMeat(UsableItem):
    NAME = 'Cooked Meat'
    IMAGE = Sprites.COOKED_MEAT


class SplashAttackEntity(SpriteMixin):
    # TODO: Нужно убрать это отсюда, но я не нашел куда
    ANIMATION_FRAMES = [
        Sprites.SPLASH_1,
        Sprites.SPLASH_2,
        Sprites.SPLASH_3,
        Sprites.SPLASH_4,
        Sprites.SPLASH_5
    ]

    ANIMATION_SPEED = 0.05
    # Через сколько нужно убить эту сущность
    KILL_TIMEOUT = (len(ANIMATION_FRAMES) + 1) * ANIMATION_SPEED

    def __init__(self, position: Vector2) -> None:
        super().__init__(position)

        self.sprite_init(AnimatedSpriteWithCameraOffset(
            self.ANIMATION_FRAMES, self.ANIMATION_SPEED, 10000), Vector2())

        # self.sprite.rotation = 180

        self.kill_timer = 0
        self.subscribe_on_update(self.kill_animation)

    def kill_animation(self, delta: float):
        self.kill_timer += delta

        if self.kill_timer >= self.KILL_TIMEOUT:
            self.destroy()


class BaseDamagingItem(UsableItem):
    NAME = 'BaseDamagingItem'
    IMAGE = Sprites.BAG
    MAX_AMOUNT = 1
    ATTACK_RANGE = 100
    DAMAGE = 1
    COOLDOWN = 1  # in seconds

    def __init__(self, amount: int) -> None:
        super().__init__(amount)

        self.last_time_used = 0

    def use(self, initiator: Entity):
        if initiator.game.scene_passed_time - self.last_time_used < self.COOLDOWN:
            return

        self.last_time_used = initiator.game.scene_passed_time

        mouse_pos = initiator.game.from_screen_to_world_point(
            Vector2.from_tuple(pygame.mouse.get_pos()))

        attack_direction = (
            mouse_pos - initiator.position).normalized() * self.ATTACK_RANGE
        attack_point = attack_direction + initiator.position

        SplashAttackEntity(attack_point)

        # TODO: вот этот hasattr вызов просто ужасен, но мне лень решать проблему с циклическими импортами, так что и так сойдет
        attacked_entities = filter(
            lambda x: hasattr(x, "add_hp") and (
                x.position - attack_point).magnitude() <= self.ATTACK_RANGE and x.id != initiator.id,
            initiator.game.enabled_entities
        )

        for ent in attacked_entities:
            ent.add_hp(-self.DAMAGE, self)


@register_json
class WoodenSword(BaseDamagingItem):
    NAME = 'Wooden Sword'
    IMAGE = Sprites.SWORD_WOOD
    MAX_AMOUNT = 1
    ATTACK_RANGE = 100
    DAMAGE = 1


@register_json
class StoneSword(BaseDamagingItem):
    NAME = 'Stone Sword'
    IMAGE = Sprites.SWORD_STONE
    DAMAGE = 2


@register_json
class IronSword(BaseDamagingItem):
    NAME = 'Iron Sword'
    IMAGE = Sprites.SWORD_IRON
    DAMAGE = 4


@register_json
class GoldenSword(BaseDamagingItem):
    NAME = 'Golden Sword'
    IMAGE = Sprites.SWORD_GOLD
    DAMAGE = 7


@register_json
class BasePickaxe(BaseDamagingItem):
    """Базовый класс кирок, что бы копать камень"""
    NAME = 'BasePickaxe'
    IMAGE = Sprites.BAG
    DAMAGE = 1
    POWER = 1


@register_json
class WoodenPickaxe(BasePickaxe):
    NAME = 'Wooden Pickaxe'
    IMAGE = Sprites.PICKAXE_WOOD
    DAMAGE = 1


@register_json
class StonePickaxe(BasePickaxe):
    NAME = 'Stone Pickaxe'
    IMAGE = Sprites.PICKAXE_STONE
    DAMAGE = 2
    POWER = 2


@register_json
class IronPickaxe(BasePickaxe):
    NAME = 'Iron Pickaxe'
    IMAGE = Sprites.PICKAXE_IRON
    DAMAGE = 3
    POWER = 3


@register_json
class GoldenPickaxe(BasePickaxe):
    NAME = 'Golden Pickaxe'
    IMAGE = Sprites.PICKAXE_GOLD
    DAMAGE = 4
    POWER = 4


@register_json
class BaseAxe(BaseDamagingItem):
    """Базовый класс топоров, что бы рубить дерево"""
    NAME = 'BaseAxe'
    IMAGE = Sprites.BAG
    DAMAGE = 1
    POWER = 1


@register_json
class WoodenAxe(BaseAxe):
    NAME = "Wooden Axe"
    IMAGE = Sprites.AXE_WOOD
    DAMAGE = 1
    POWER = 1


@register_json
class StoneAxe(BaseAxe):
    NAME = "Stone Axe"
    IMAGE = Sprites.AXE_STONE
    DAMAGE = 2
    POWER = 2


@register_json
class IronAxe(BaseAxe):
    NAME = "Iron Axe"
    IMAGE = Sprites.AXE_IRON
    DAMAGE = 4
    POWER = 3


@register_json
class GoldenAxe(BaseAxe):
    NAME = "Golden Axe"
    IMAGE = Sprites.AXE_GOLD
    DAMAGE = 5
    POWER = 4


@register_json
class Bow(UsableItem):
    pass
