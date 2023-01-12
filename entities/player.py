"""
Тут хранится класс игрока, и все что с ним связано
"""
from typing import List
from entities.item import ItemEntity
from entities.living_entities import LivingEntity
from entities.ui import Button
from entities.util_entities import OnMapSpriteMixin
from entities.map import Map
from assets import FONT_PATH, Sprites, SPRITE_SIZE, SPRITESHEET_UPSCALE
from items import Inventory, Item
from pygame_entities.entities.entity import Entity

from pygame_entities.utils.drawable import AnimatedSpriteWithCameraOffset
from pygame_entities.utils.math import Vector2
from pygame_entities.entities.mixins import BlockingCollisionMixin, VelocityMixin

import pygame


class Player(LivingEntity, OnMapSpriteMixin, BlockingCollisionMixin, VelocityMixin):
    FRONT_IDLE_ANIM = [Sprites.PLAYER_FRONT_1]
    FRONT_MOVE_ANIM = [Sprites.PLAYER_FRONT_1, Sprites.PLAYER_FRONT_2,
                       Sprites.PLAYER_FRONT_3, Sprites.PLAYER_FRONT_4]
    BACK_MOVE_ANIM = [Sprites.PLAYER_BACK_1, Sprites.PLAYER_BACK_2,
                      Sprites.PLAYER_BACK_3, Sprites.PLAYER_BACK_4]
    LEFT_MOVE_ANIM = [Sprites.PLAYER_LEFT_1, Sprites.PLAYER_LEFT_2,
                      Sprites.PLAYER_LEFT_3, Sprites.PLAYER_LEFT_4]
    RIGHT_MOVE_ANIM = [Sprites.PLAYER_RIGHT_1, Sprites.PLAYER_RIGHT_2,
                       Sprites.PLAYER_RIGHT_3, Sprites.PLAYER_RIGHT_4]

    COLLIDER_SIZE = Vector2(20, 20) * SPRITESHEET_UPSCALE

    # В тайл/сек.
    DEFAULT_SPEED = 3
    DEFAULT_HP = 10
    INVENTORY_SLOTS_COUNT = 10

    ITEMS_PICKUP_RADIUS = 128

    def __init__(self, position: Vector2, tile_map: Map) -> None:
        super().__init__(position, self.DEFAULT_HP, tile_map)
        self.set_speed(self.DEFAULT_SPEED)

        self.sprite_init(AnimatedSpriteWithCameraOffset(
            self.FRONT_IDLE_ANIM, 0.2), Vector2())

        self.last_animation = self.FRONT_IDLE_ANIM

        self.inventory: Inventory = Inventory(
            slots_count=self.INVENTORY_SLOTS_COUNT)

        self.collision_init(self.COLLIDER_SIZE)
        self.velocity_init(False, 0.1)

        self.inventory_panel = InventoryPanelUI(self.inventory)

        self.subscribe_on_update(self.move_player)
        self.subscribe_on_update(self.animate)
        self.game.subsribe_for_event(self.keys_handler, pygame.KEYDOWN)

    def move_player(self, delta_time: float):
        keys = pygame.key.get_pressed()

        direction = Vector2()

        if keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1

        self.velocity = direction.normalized() * self.speed * delta_time

    def keys_handler(self, event: pygame.event.Event):
        if event.key == pygame.K_f:
            self.pickup_nearest_items()

    def pickup_nearest_items(self):
        for ent in self.game.enabled_entities:
            if not type(ent) == ItemEntity or (ent.position - self.position).magnitude() > self.ITEMS_PICKUP_RADIUS:
                continue

            ent: ItemEntity
            ent.item = self.inventory.add_item(ent.item)

        self.inventory_panel.render_panel()

    def animate(self, delta_time: float):
        if self.velocity.x > 0:
            self.last_animation = self.LEFT_MOVE_ANIM
        elif self.velocity.x < 0:
            self.last_animation = self.RIGHT_MOVE_ANIM
        elif self.velocity.y > 0:
            self.last_animation = self.FRONT_MOVE_ANIM
        elif self.velocity.y < 0:
            self.last_animation = self.BACK_MOVE_ANIM
        else:
            self.last_animation = self.FRONT_IDLE_ANIM

        if self.sprite.frames != self.last_animation:
            self.sprite.frames = self.last_animation

    def get_loot(self) -> List[Item]:
        return [item for item in self.inventory.grid if not item is None]

    def set_speed(self, tiles_in_second: float) -> None:
        self.speed = tiles_in_second * SPRITE_SIZE[0]
        print(self.speed)


class InventoryPanelUI(Entity):
    """
    Рендерит панельку инвентаря
    """
    SCREEN_PANEL_OFFSET = Vector2(100, 100)

    def __init__(self, inventory_ref: Inventory) -> None:
        super().__init__(Vector2())

        self.ui_elems = list()
        self.inventory = inventory_ref

    def render_panel(self):
        [el.destroy() for el in self.ui_elems]
        self.ui_elems = list()

        font = pygame.font.Font(FONT_PATH, 40)

        for i, item in enumerate(self.inventory.grid):
            if item is None:
                continue

            item_btn = Button(self.SCREEN_PANEL_OFFSET +
                              Vector2(0, i * 50), f"{item.NAME} x{item.amount}", font)
            self.ui_elems.append(item_btn)

    def hide_panel(self):
        pass
