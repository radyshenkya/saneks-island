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
    from entities.ui import Button, Popup, InputField

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
    game.subscribe_for_event(on_quit_event, pygame.QUIT)

    # Создаем карту размерами 100x100 тайлов, с чанками 10x10
    tile_map = Map(Vector2(), (10, 10), (10, 10), SandTile)
    # Генерируем карту
    fill_map(tile_map, 1)
    player = Player(Vector2(100, 100), tile_map)

    # Добавляем кнопку
    popup_font = pygame.font.Font(FONT_PATH, 20)

    def on_lbm_click():
        Popup(Vector2.from_tuple(pygame.mouse.get_pos()),
              "ЛКМ Нажата.", popup_font)

    def on_rbm_click():
        Popup(Vector2.from_tuple(pygame.mouse.get_pos()),
              "ПКМ Нажата.", popup_font, 1)

    normal_font = pygame.font.Font(FONT_PATH, 40)

    Button(Vector2(100, 100), "тестовая кнопка",
           normal_font, on_lbm_click, on_rbm_click)
    InputField(Vector2(100, 300), "aboba",
               normal_font, 20, "Place Holder Text")

    game.camera_follow_entity(player)

    game.run()


if __name__ == "__main__":
    main()
