"""
Mixins for entities (Based on Entity class)
"""
from types import FunctionType, MethodType
from typing import Union, List
from ..utils.drawable import BaseSprite
from ..utils.math import Vector2
from ..utils.collision_side import check_side, UP, DOWN, RIGHT, LEFT
from ..game import Game

from .entity import Entity

import pygame


class SpriteMixin(Entity):
    """
    Sprite render mixin

    Need to run sprite_init method for initialization
    """

    def sprite_init(self, sprite: BaseSprite, sprite_position_offset=Vector2()) -> None:
        """
        Initializating this mixin.

        Automatically adding sprite in game
        """
        self.sprite_offset = sprite_position_offset
        self.sprite = sprite
        self.sprite.center_position = (
            self.position + self.sprite_offset).get_integer_tuple()
        self.subscribe_on_update(self.sprite_update_position)
        self.subscribe_on_destroy(self.kill_sprite)

    def sprite_update_position(self, delta_time: float):
        """
        Runned every frame.

        Changing position of sprite.
        """
        self.sprite.center_position = (
            self.position + self.sprite_offset).get_integer_tuple()

    def kill_sprite(self):
        """
        Runned on destroy of entity.

        Deleting sprite from game
        """
        self.sprite.kill()

# TODO: Add function to cast with image polygons
# TODO: Add not rectangle collisions
# TODO: Separate CollisionMixin entities from all enabled_entities, to iterate on collision check only on entities with collision mixin


class CollisionMixin(Entity):
    """
    Mixin for collision callbacks

    Need to run collision_init method for initialization
    """

    def collision_init(
        self, collider_size: Vector2, is_trigger=False, is_check_collision=False
    ):
        """
        Initializing this mixin.

        If is_check_collisions=False subscribed functions on_collide and on_trigger will not be called.

        It is used for optimization.
        """
        self.collider_size: Vector2 = collider_size
        self.is_trigger: bool = is_trigger
        self.subscribe_on_update(self._check_collisions)
        self.is_check_collision: bool = is_check_collision
        self.on_collide_callbacks = list()
        self.on_trigger_callbacks = list()

    def subscribe_on_collide(self, function: Union[FunctionType, MethodType]):
        """
        Subscribes function for collisions.

        Subscribed function will be called every frame when colliding with another collider.

        Function will be called with entity argument like that: function(entity: CollisionMixin)
        """
        self.on_collide_callbacks.append(function)

    def subscribe_on_trigger(self, function: Union[FunctionType, MethodType]):
        """
        Subscribes function for collisions with triggers.

        Subscribed function will be called every frame when colliding with another collider.

        Function will be called with entity argument like that: function(entity: CollisionMixin)
        """
        self.on_trigger_callbacks.append(function)

    def _on_collide(self, entity, self_collider_rect: pygame.Rect, other_collider_rect: pygame.Rect):
        """
        Calls all subscribed functions for collisions
        """
        for method in self.on_collide_callbacks:
            method(entity, self_collider_rect, other_collider_rect)

    def _on_trigger(self, entity, self_collider_rect: pygame.Rect, other_collider_rect: pygame.Rect):
        """
        Calls all subscribed functions for collisions with trigger
        """
        for method in self.on_trigger_callbacks:
            method(entity, self_collider_rect, other_collider_rect)

    def _check_collisions(self, _):
        """
        Runned every frame.

        Checks collisions
        """
        if not self.is_check_collision:
            return

        for entity in CollisionMixin.cast_rect(self.collider_rect):
            if entity.id == self.id:
                continue

            if entity.is_trigger or self.is_trigger:
                self._on_trigger(entity, self.collider_rect,
                                 entity.collider_rect)
                continue
            self._on_collide(entity, self.collider_rect,
                             entity.collider_rect)

    @property
    def collider_rect(self) -> pygame.Rect:
        """
        Returning pygame.Rect of this collider.
        """
        return pygame.Rect(
            (self.position - self.collider_size / 2).get_integer_tuple(),
            self.collider_size.get_integer_tuple(),
        )

    @staticmethod
    def cast_rect(rect: pygame.Rect) -> List["CollisionMixin"]:
        """
        Casts a rect and returns all collided entities with CollisionMixin
        """
        collided_entities = list()
        for entity in Game.get_instance().enabled_entities:
            if not isinstance(entity, CollisionMixin):
                continue

            if rect.colliderect(entity.collider_rect):
                collided_entities.append(entity)

        return collided_entities


class VelocityMixin(Entity):
    """
    Mixin for smooth moving of entity

    Change self.velocity for moving
    """

    def velocity_init(self, is_kinematic=True, velocity_regress_strength=0.0):
        """
        Initializing this mixin.

        velocity_redress_strength used for smooth changing velocity to Vector(0, 0)
        """
        self.is_kinematic: bool = is_kinematic

        self.velocity_regress_strength: float = velocity_regress_strength
        self.velocity: Vector2 = Vector2(0, 0)

        self.subscribe_on_update(self._update_velocity_and_pos)

    def _update_velocity_and_pos(self, _):
        """
        Called every frame.

        Changing position of entity
        """
        self.position += self.velocity

        if not self.is_kinematic:
            self.velocity = Vector2.lerp(
                self.velocity, Vector2(0, 0), self.velocity_regress_strength
            )


class BlockingCollisionMixin(CollisionMixin):
    """
    Blocking position of entity in another colliders.

    Based on CollisiongMixin
    """

    def collision_init(self, collider_size: Vector2, is_trigger=False):
        super().collision_init(collider_size, is_trigger, True)
        self.subscribe_on_collide(self._move_back_on_colliding)

    def _move_back_on_colliding(self, _, self_collider: pygame.Rect, other_collider: pygame.Rect):
        """
        Runned every frame.

        Moving back entity from another collider.
        """
        side = check_side(self_collider, other_collider)

        if side == UP:
            self_new_y = other_collider.top - (self_collider.height / 2)
            self.position = Vector2(self.position.x, self_new_y)
        elif side == DOWN:
            self_new_y = other_collider.bottom + (self_collider.height / 2)
            self.position = Vector2(self.position.x, self_new_y)
        elif side == RIGHT:
            self_new_x = other_collider.right + (self_collider.width / 2)
            self.position = Vector2(self_new_x, self.position.y)
        else:
            self_new_x = other_collider.left - (self_collider.width / 2)
            self.position = Vector2(self_new_x, self.position.y)


class MouseEventMixin(CollisionMixin):
    """
    Mixin for handling clicks / hovering above this entity.

    Based on CollisionMixin.

    WARNING: Needs to be initialized after collision_init method.
    """

    def mouse_events_init(self):
        """
        Initializing this mixin
        """
        self._on_mouse_down = list()
        self._on_mouse_up = list()
        self._on_mouse_motion = list()
        self.game.subsribe_for_event(
            self._mouse_events, pygame.MOUSEBUTTONDOWN)
        self.game.subsribe_for_event(self._mouse_events, pygame.MOUSEBUTTONUP)
        self.game.subsribe_for_event(self._mouse_events, pygame.MOUSEMOTION)

    def subscribe_on_mouse_down(self, function: Union[MethodType, FunctionType]):
        """
        Subscribing function on every pygame.MOUSEBUTTONDOWN event when cursor is over collider of this entity.

        Subscribed function will be called with button parameter like that: function(event.button)
        """
        self._on_mouse_down.append(function)

    def subscribe_on_mouse_up(self, function: Union[MethodType, FunctionType]):
        """
        Subscribing function on every pygame.MOUSEBUTTONUP event when cursor is over collider of this entity.

        Subscribed function will be called with button parameter like that: function(event.button)
        """
        self._on_mouse_up.append(function)

    def subscribe_on_mouse_motion(self, function: Union[MethodType, FunctionType]):
        """
        Subscribing function on every pygame.MOUSEMOTION event when cursor is over collider of this entity.

        Subscribed function will be called without parameters like that: function(event.button)
        """
        self._on_mouse_motion.append(function)

    def _mouse_events(self, event: pygame.event.Event):
        """
        Runned on every MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION events.

        Calling subscribed functions
        """
        # Checking, is mouse pointer is over object
        mouse_world_position = self.game.from_screen_to_world_point(
            Vector2.from_tuple(pygame.mouse.get_pos()))

        if not self.collider_rect.collidepoint(mouse_world_position.get_tuple()):
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            [f(event.button) for f in self._on_mouse_down]
        elif event.type == pygame.MOUSEBUTTONUP:
            [f(event.button) for f in self._on_mouse_up]
        elif event.type == pygame.MOUSEMOTION:
            [f() for f in self._on_mouse_motion]
