from random import choice, randint
from entities.buildings import Stone, StoneWithCoal, StoneWithGold, StoneWithIron, Tree, WoodenCrate
from entities.item import ItemEntity
from entities.map import Map, SandTile, fill_map
from entities.player import Player
from items.items import Rock, Wood, WoodenAxe
from pygame_entities.game import Game
from pygame_entities.scenes import BaseScene
from pygame_entities.utils.math import Vector2


class MainScene(BaseScene):
    """Сцена самой игры как бы да ок"""

    CHUNK_SIZE = (10, 10)
    MAP_SIZE = (6, 6)

    BUILDINGS_COUNT = 80
    NATURAL_BUILDINGS = [
        Tree
    ]
    ITEMS_COUNT = 100
    NATURAL_ITEMS = [
        Wood, Rock
    ]

    MAP = None

    @classmethod
    def spawn_stones(cls, game: Game):
        STONE_CLUSTERS = 15
        MAX_STONE_SPAWN_OFFSET = 1000
        MIN_STONES_IN_CLUSTERS = 1
        MAX_STONES_IN_CLUSTERS = 7
        STONES = [
            Stone,
            StoneWithCoal,
            StoneWithGold,
            StoneWithIron
        ]

        # Choosing cluster
        pos_constraint = cls.MAP.get_map_size().get_integer_tuple()

        for cluster_i in range(STONE_CLUSTERS):
            stone = choice(STONES)
            cluster_pos = Vector2(
                randint(200, pos_constraint[0] -
                        MAX_STONE_SPAWN_OFFSET),
                randint(200, pos_constraint[1] -
                        MAX_STONE_SPAWN_OFFSET)
            )

            stones_in_cluster = randint(
                MIN_STONES_IN_CLUSTERS, MAX_STONES_IN_CLUSTERS)

            for i in range(stones_in_cluster):
                stone(cluster_pos + Vector2.from_tuple(
                    (
                        randint(0,
                                MAX_STONE_SPAWN_OFFSET),
                        randint(0,
                                MAX_STONE_SPAWN_OFFSET)
                    )
                )
                )

    @classmethod
    def spawn_buildings(cls, game: Game):
        pos_constraint = cls.MAP.get_map_size().get_integer_tuple()

        cls.spawn_stones(game)

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

        player = Player(cls.MAP.get_map_size() / 2)
        ItemEntity(player.position, WoodenAxe(1))
        ItemEntity(player.position, WoodenCrate.get_item_class()(5))
        game.camera_follow_entity(player)

        cls.spawn_buildings(game)

        game.run()

    @classmethod
    def on_end(cls, game: Game):
        pass
