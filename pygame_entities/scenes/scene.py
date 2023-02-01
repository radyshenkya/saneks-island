from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..game import Game


class BaseScene:
    """Base scene class"""

    @classmethod
    def on_load(cls, game: "Game"):
        """Called by game object on start of this scene"""
        pass

    @classmethod
    def on_end(cls, game: "Game"):
        """Called on end of this scene"""
        pass
