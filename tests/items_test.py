"""
Тест игрока и предметов

Можно подбирать предметы на клавишу F

Так же можно убить игрока на клавишу K (из него выпадут все реси)
"""
from random import choice
import pygame
from inspect import getsourcefile
import os.path as path
import sys


current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

if True:
    from pygame_entities.entities.entity import Entity
    from pygame_entities.utils.math import Vector2
    from pygame_entities.utils.drawable import BaseSprite, SpriteWithCameraOffset
    from pygame_entities.game import Game
    from pygame_entities.entities.mixins import SpriteMixin, BlockingCollisionMixin, VelocityMixin
    from assets import Sprites
    from entities.map import Map, SandTile, fill_map
    from entities.player import Player
    from entities.item import ItemEntity
    from entities.ui import Popup
    from items import Wood, Iron, GoldIngot, UsableItem

RESOLUTION = (800, 800)
FRAMERATE = 60
VOID_COLOR = (50, 50, 50)  # Цвет фона


class TestUsableItem(UsableItem):
    NAME = "TEST USABLE ITEM"
    IMAGE = Sprites.BAG
    MAX_AMOUNT = 20

    def use(self, initiator: Entity):
        from assets import FONT_PATH
        from pygame import font

        new_item = choice([Wood, Iron, GoldIngot, self.__class__])(1)

        ItemEntity(initiator.position, new_item)
        Popup(initiator.position, f"TestItemUsed", font.Font(
            FONT_PATH, 40), False)

        self.amount -= 1


def on_quit_event(event: pygame.event.Event):
    """
    Нужна для выхода из игры по крестику окна.
    """
    Game.get_instance().running = False


def main() -> None:
    game = Game.get_instance(RESOLUTION, FRAMERATE, VOID_COLOR)
    game.subscribe_for_event(on_quit_event, pygame.QUIT)

    # Создаем карту размерами 100x100 тайлов, с чанками 10x10
    tile_map = Map(Vector2(), (10, 10), (2, 2), SandTile)

    # Генерируем карту
    fill_map(tile_map, 1)

    player = Player(Vector2(100, 100), tile_map)

    # тест для убыйства игрока
    def kill_player(event):
        if event.key == pygame.K_k:
            game.camera_follow_entity(None)
            player.set_hp(0)

    game.subscribe_for_event(kill_player, pygame.KEYDOWN)

    # генерируем айтемсы
    for x in range(10):
        for y in range(10):
            ItemEntity(Vector2(x * 128, y * 128),
                       TestUsableItem(2))

    game.camera_follow_entity(player)

    game.run()


if __name__ == "__main__":
    main()
