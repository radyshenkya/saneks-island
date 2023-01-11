import pygame
from inspect import getsourcefile
import os.path as path
import sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

if True:
    from pygame_entities.utils.math import Vector2
    from pygame_entities.utils.drawable import BaseSprite, SpriteWithCameraOffset
    from pygame_entities.game import Game
    from pygame_entities.entities.mixins import SpriteMixin, BlockingCollisionMixin, VelocityMixin
    from assets import Sprites, FONT_PATH
    from entities.map import Map, SandTile, fill_map
    from entities.player import Player
    from entities.ui import Button

RESOLUTION = (0, 0)
FRAMERATE = 60
VOID_COLOR = (50, 50, 50)  # Цвет фона


def on_quit_event(event: pygame.event.Event):
    """
    Нужна для выхода из игры по крестику окна.
    """
    Game.get_instance().running = False


def main() -> None:
    game = Game.get_instance(RESOLUTION, FRAMERATE, VOID_COLOR)
    game.subsribe_for_event(on_quit_event, pygame.QUIT)

    # Создаем карту размерами 100x100 тайлов, с чанками 10x10
    tile_map = Map(Vector2(), (10, 10), (10, 10), SandTile)
    # Генерируем карту
    fill_map(tile_map, 1)
    player = Player(Vector2(100, 100), tile_map)

    # Добавляем кнопку
    def on_lbm_click():
        print("Кнопка нажата")

    def on_rbm_click():
        print("Другая кнопка нажата")

    Button(Vector2(100, 100), "hello rudolf", pygame.font.Font(
        FONT_PATH, 40), on_lbm_click, on_rbm_click)

    game.camera_follow_entity(player)

    game.run()


if __name__ == "__main__":
    main()
