"""
Тут хранится класс игрока, и все что с ним связано
"""
from entities.living_entities import LivingEntity
from entities.util_entities import OnMapSpriteMixin
from entities.map import Map
from assets import Sprites, SPRITE_SIZE, SPRITESHEET_UPSCALE
from items import Inventory

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

    def __init__(self, position: Vector2, tile_map: Map) -> None:
        super().__init__(position, self.DEFAULT_HP, tile_map)
        self.set_speed(self.DEFAULT_SPEED)

        self.sprite_init(AnimatedSpriteWithCameraOffset(
            self.FRONT_IDLE_ANIM, 0.2), Vector2())

        self.last_animation = self.FRONT_IDLE_ANIM

        self.inventory = Inventory(slots_count=self.INVENTORY_SLOTS_COUNT)

        self.collision_init(self.COLLIDER_SIZE)
        self.velocity_init(False, 0.1)

        self.subscribe_on_update(self.move_player)
        self.subscribe_on_update(self.animate)

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

    def set_speed(self, tiles_in_second: float) -> None:
        self.speed = tiles_in_second * SPRITE_SIZE[0]
        print(self.speed)
