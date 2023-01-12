"""
Main Game class.

Needs to be in every game builded with this pygame_entities library
"""

from types import FunctionType, MethodType
from typing import Dict, List, Tuple, Union, TYPE_CHECKING
if TYPE_CHECKING:
    from .entities.entity import Entity
    from .utils.drawable import BaseSprite
from .utils.math import Vector2

import pygame


class Game:
    """
    Main class of game.

    This class is builded like singleton pattern, 

    To create/get Game object use Game.get_instance method.

    Do not use initialization.
    """

    _instance = None

    def get_instance(screen_resolution=(0, 0), frame_rate=60, void_color=(0, 0, 0)) -> "Game":
        """
        Get instance of Game class.
        """
        if Game._instance is None:
            Game._instance = Game(screen_resolution, frame_rate, void_color)

        return Game._instance

    def __init__(self, screen_resolution=(0, 0), frame_rate=60, void_color=(0, 0, 0)) -> None:
        """
        Do not use this.

        Instead call Game.get_instance()
        """
        if not Game._instance is None:
            raise Exception("Game class instantiated 2 times.")

        pygame.init()

        # Public fields
        self.framerate: int = frame_rate
        self.void_color: Tuple[int, int, int] = void_color
        self.delta_time = 1 / self.framerate

        self._screen_resolution: Tuple[int, int] = screen_resolution
        self._screen = pygame.display.set_mode(self._screen_resolution)
        self._clock = pygame.time.Clock()
        self.running = True
        self._sprites = pygame.sprite.LayeredUpdates()

        # Using dict, because with dict we can remove entities from game in O(1) time
        self._entity_counter = 0
        self._entities_for_delete = list()
        self._enabled_entities = dict()
        self._disabled_entities = dict()

        # For camera
        self.camera_follow_smooth_coefficient = 0.1
        self._camera_position = Vector2(0, 0)
        self._camera_follow_object = None

        # for event system
        self._subscribed_events: Dict[int, List[FunctionType]] = dict()

    @property
    def screen(self) -> pygame.Surface:
        """
        Screen surface.

        Can be changed to another pygame.Surface object.
        """
        return self._screen

    @screen.setter
    def screen(self, value: pygame.Surface):
        self._screen = value
        self._screen_resolution = value.get_size()

    @property
    def screen_resolution(self) -> Tuple[int, int]:
        """
        Resolution of screen surface
        """
        return self._screen_resolution

    @property
    def enabled_entities(self) -> List["Entity"]:
        """
        List of enabled entities
        """
        return list(self._enabled_entities.values())

    @property
    def disabled_entities(self) -> List["Entity"]:
        """
        List of disabled entities
        """
        return self._disabled_entities.values()

    def camera_follow_entity(self, entity: Union["Entity", None]):
        """
        Sets camera to follow some entity
        """
        self._camera_follow_object = entity

    def set_sprite_layer(self, sprite: "BaseSprite", layer: Union[int, float]):
        """
        Sets sprite layer.

        Sprite need to be a BaseSprite class or childs of this class
        """
        self._sprites.change_layer(sprite, layer)

    def _update_events(self):
        """
        Gets all pygame events and calling subscribers of each event type that returned.
        """
        for event in pygame.event.get():
            for func in self._subscribed_events.get(event.type, []):
                func(event)

    def subsribe_for_event(self, function: Union[MethodType, FunctionType], event_type: int):
        """
        Subscribe a function for pygame event.

        This function will be called when new event with type event_type will be received
        """
        subscribers = self._subscribed_events.get(event_type, [])
        subscribers.append(function)
        self._subscribed_events[event_type] = subscribers

    def run(self):
        """
        Starts main loop of game.

        All configurations need to be created before calling this method
        """
        while self.running:
            self._screen.fill(self.void_color)

            # Updating systems
            self._update_events()
            self._update_entities()
            self._sprites.update()
            self._delete_entities()
            self._camera_follow()

            self._sprites.draw(self._screen)
            pygame.display.flip()
            self.delta_time = self._clock.tick(self.framerate) / 1000

    def _update_entities(self):
        """
        Updates all enabled entities

        """
        for entity in self.enabled_entities:
            entity._update(self.delta_time)

    def _camera_follow(self):
        """
        Moves camera towards entity for following that was set by method camera_follow_entity.

        If follow entity is None, camera will remain in the same position
        """
        if not self._camera_follow_object is None:
            self._camera_position = Vector2.lerp(
                self._camera_position,
                self._camera_follow_object.position
                - Vector2(
                    self._screen.get_width() /
                    2, self._screen.get_height() / 2
                ),
                self.camera_follow_smooth_coefficient,
            )

    @property
    def camera_center_position(self) -> Vector2:
        """
        Returns center point of camera in world
        """
        return self._camera_position + Vector2(
            self.screen_resolution[0] /
            2, self.screen_resolution[1] / 2
        )

    def add_sprite(self, sprite: pygame.sprite.Sprite):
        """
        Adding sprite to render
        """
        self._sprites.add(sprite)

    def add_entity(self, entity):
        """
        Adding entity in game
        """
        self._enabled_entities[self._entity_counter] = entity
        entity.id = self._entity_counter
        self._entity_counter += 1

    def disable_entity(self, entity):
        """
        Disabling entity.

        After calling this function entity will not recieve update() method calls
        """
        if entity.id in self._enabled_entities.keys():
            self._disabled_entities[entity.id] = self._enabled_entities[entity.id]
            del self._enabled_entities[entity.id]

    def enable_entity(self, entity):
        """
        Enabling entity.

        After calling this function entity will recieve update() method calls
        """
        if entity.id in self._disabled_entities.keys():
            self._enabled_entities[entity.id] = self._disabled_entities[entity.id]
            del self._disabled_entities[entity.id]

    def delete_entity(self, entity_id: int):
        """
        Adds entity into pool for deleting
        """
        if entity_id not in self._entities_for_delete:
            self._entities_for_delete.append(entity_id)

    def _delete_entities(self):
        """
        Deleting all entities that in delete pool
        """
        for entity_id in self._entities_for_delete:
            if entity_id in self._enabled_entities.keys():
                del self._enabled_entities[entity_id]
            else:
                del self._disabled_entities[entity_id]

        self._entities_for_delete = list()

    def from_screen_to_world_point(self, on_screen_point: Vector2) -> Vector2:
        return on_screen_point + self._camera_position

    def from_world_point_to_screen(self, world_point: Vector2) -> Vector2:
        return world_point - self._camera_position
