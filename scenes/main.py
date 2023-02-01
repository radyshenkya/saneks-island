from random import choice, randint
from entities.buildings import Stone, StoneWithCoal, StoneWithGold, StoneWithIron
from entities.item import ItemEntity
from entities.map import Map, SandTile, fill_map
from entities.player import Player
from items.items import Rock, Wood
from pygame_entities.game import Game
from pygame_entities.scenes import BaseScene
from pygame_entities.utils.math import Vector2


class MainScene(BaseScene):
    """Сцена самой игры как бы да ок"""

    CHUNK_SIZE = (10, 10)
    MAP_SIZE = (10, 10)

    BUILDINGS_COUNT = 50
    NATURAL_BUILDINGS = [
        Stone, StoneWithCoal, StoneWithGold, StoneWithIron
    ]
    ITEMS_COUNT = 100
    NATURAL_ITEMS = [
        Wood, Rock
    ]

    MAP = None

    @classmethod
    def spawn_buildings(cls, game: Game):
        pos_constraint = cls.MAP.get_map_size().get_integer_tuple()

        for _ in range(cls.BUILDINGS_COUNT):
            building_class = choice(cls.NATURAL_BUILDINGS)
            pos = Vector2(
                randint(100, pos_constraint[0]),
                randint(100, pos_constraint[1])
            )

            building_class(pos)

    @classmethod
    def spawn_items(cls, game: Game):
        pos_constraint = cls.MAP.get_map_size().get_integer_tuple()

        for _ in range(cls.ITEMS_COUNT):
            item_class = choice(cls.NATURAL_ITEMS)
            pos = Vector2(
                randint(100, pos_constraint[0]),
                randint(100, pos_constraint[1])
            )

            ItemEntity(pos, item_class(1))

    @classmethod
    def on_load(cls, game: Game):
        # Создаем карту размерами 100x100 тайлов, с чанками 10x10
        cls.MAP = Map(Vector2(), cls.CHUNK_SIZE, cls.MAP_SIZE, SandTile)

        # Генерируем карту
        fill_map(cls.MAP, 1)

        player = Player(Vector2(100, 100))
        game.camera_follow_entity(player)

        cls.spawn_buildings(game)
        cls.spawn_items(game)

        game.run()

    @classmethod
    def on_end(cls, game: Game):
        pass
