import pygame
pygame.init()
from pygame_entities.game import Game
from scenes import MainScene


RESOLUTION = (1200, 1000)
FRAMERATE = 60
VOID_COLOR = (50, 50, 50)  # Цвет фона


def on_quit_event(event: pygame.event.Event):
    """
    Нужна для выхода из игры по крестику окна.
    """
    Game.get_instance().running = False


def main() -> None:
    game = Game.get_instance(RESOLUTION, FRAMERATE, VOID_COLOR)
    game.subscribe_for_event(on_quit_event, pygame.QUIT)

    # Устанавливаем дефолтную сцену
    game.set_scene(MainScene)
    game.run()


if __name__ == "__main__":
    main()
