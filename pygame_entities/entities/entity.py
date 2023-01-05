"""
Base entity class.
"""

from types import FunctionType, MethodType
from typing import Union
from ..utils.math import Vector2
from ..game import Game


class Entity:
    """
    Base entity class.

    Has only position and id fields.

    Every entity in your game must be inherited from this class
    """

    def __init__(self, position: Vector2) -> None:
        """
        Initializing new entity.

        When overriding this method need to put 'super().__init__(self, position)' on top of method
        """
        self.position = position

        self._on_update = list()
        self._on_destroy = list()

        # Registering entity
        self.id = 0
        self.game = Game.get_instance()
        self.game.add_entity(self)
        self._enabled = True

    def subscribe_on_update(self, function: Union[FunctionType, MethodType]):
        """
        Subscribes function for updates.

        Subscribed function will be called every frame
        """
        self._on_update.append(function)

    def subscribe_on_destroy(self, function: Union[FunctionType, MethodType]):
        """
        Subscribes function for destroy of this entity.

        Subscribed function will be called on destroy() method
        """
        self._on_destroy.append(function)

    def _update(self, delta_time: float):
        """
        This method will be called every frame
        """
        for method in self._on_update:
            method(delta_time)

    def destroy(self):
        """
        This method will be called on destroy of this entity
        """
        for method in self._on_destroy:
            method()
        self.game.delete_entity(self.id)

    def enable(self):
        """
        Enabling entity
        """
        self.game.enable_entity(self)
        self._enabled = True

    def disable(self):
        """
        Disabling entity (Turning off updates)
        """
        self.game.disable_entity(self)
        self._enabled = False

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, is_enabled: bool):
        """
        Set enabled for entity
        """
        if is_enabled and not self._enabled:
            self.enable()
        elif not is_enabled and self._enabled:
            self.disable()
