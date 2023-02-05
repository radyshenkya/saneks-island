from pygame_entities.game import Game
from pygame_entities.scenes import BaseScene


class NewGameScene(BaseScene):
    """Сцена создания новой игры"""

    @classmethod
    def on_load(cls, game: Game):
        pass

    @classmethod
    def on_end(cls, game: Game):
        pass
