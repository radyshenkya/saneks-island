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
    from assets import Sprites
    from entities.map import Map, SandTile, fill_map
    from entities.player import Player
    from entities.item import ItemEntity
    from items import Wood, Iron, GoldIngot

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
    tile_map = Map(Vector2(), (10, 10), (2, 2), SandTile)

    # Генерируем карту
    fill_map(tile_map, 1)

    player = Player(Vector2(100, 100), tile_map)

    # генерируем айтемсы
    for x in range(10):
        for y in range(10):
            ItemEntity(Vector2(x * 100, y * 100), Wood(1))

    game.camera_follow_entity(player)

    game.run()


if __name__ == "__main__":
    main()
