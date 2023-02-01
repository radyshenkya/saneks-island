"""
Тест построечек

Можно подбирать предметы на клавишу F

Так же можно убить игрока на клавишу K (из него выпадут все реси)
"""
import sys
import os.path as path
from inspect import getsourcefile
from random import choice
import pygame

pygame.init()


current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

if True:
    from pygame_entities.entities.entity import Entity
    from pygame_entities.utils.math import Vector2
    from pygame_entities.game import Game
    from assets import Sprites
    from entities.map import Map, SandTile, fill_map
    from entities import Chest, Workbench, Popup, ItemEntity, Player, Stone, StoneWithIron, StoneWithCoal, StoneWithGold
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

    player = Player(Vector2(100, 100))

    # тест для убыйства игрока
    def kill_player(event):
        if event.key == pygame.K_k:
            game.camera_follow_entity(None)
            player.set_hp(0)

    game.subscribe_for_event(kill_player, pygame.KEYDOWN)

    # генерируем айтемсы
    for x in range(3):
        for y in range(3):
            ItemEntity(Vector2(x * 100, y * 100),
                       Wood(1))

    ItemEntity(Vector2(300, 300), Chest.get_item_class()(3))
    ItemEntity(Vector2(400, 400), Workbench.get_item_class()(1))

    Stone(Vector2(350, 350))
    Stone(Vector2(550, 350))
    Stone(Vector2(750, 350))
    StoneWithCoal(Vector2(350, 550))
    StoneWithCoal(Vector2(550, 550))
    StoneWithCoal(Vector2(750, 550))
    StoneWithIron(Vector2(350, 750))
    StoneWithIron(Vector2(550, 750))
    StoneWithIron(Vector2(750, 750))
    StoneWithGold(Vector2(350, 950))
    StoneWithGold(Vector2(550, 950))
    StoneWithGold(Vector2(750, 950))

    game.camera_follow_entity(player)

    game.run()


if __name__ == "__main__":
    main()
