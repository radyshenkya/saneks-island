from json import dumps
import os
from random import choice, randint
from entities.buildings import Stone, StoneWithCoal, StoneWithGold, StoneWithIron, Tree, WoodenCrate
from entities.building import snap_position_to_grid
from entities.item import ItemEntity
from entities.map import Map, SandTile, fill_map
from entities.player import Player
from entities.json_parser import registered_classes
from items.items import Rock, Wood, WoodenAxe
from pygame_entities.game import Game
from pygame_entities.scenes import BaseScene
from pygame_entities.utils.math import Vector2

SAVES_FOLDER = './saves'

isExist = os.path.exists(SAVES_FOLDER)
if not isExist:
    os.makedirs(SAVES_FOLDER)

# FIXME: плеер не сбрасывается...


class GameGenerationScene(BaseScene):
    """Здесь генерируется игра, и сохраняется в файл"""

    CHUNK_SIZE = (10, 10)
    MAP_SIZE = (6, 6)
    SAVE_NAME = "unknown game"

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
                stone(snap_position_to_grid(cluster_pos + Vector2.from_tuple(
                    (
                        randint(0,
                                MAX_STONE_SPAWN_OFFSET),
                        randint(0,
                                MAX_STONE_SPAWN_OFFSET)
                    )
                ))
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

            building_class(snap_position_to_grid(pos))

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
    def dump_to_json(cls, game: Game) -> str:
        json_dict = {'entities': []}

        for ent in game.enabled_entities:
            if ent.__class__.__name__ not in registered_classes.keys():
                continue

            json_dict['entities'].append(ent.to_json())

        return dumps(json_dict)

    @classmethod
    def on_load(cls, game: Game):
        cls.MAP = Map(Vector2(), cls.CHUNK_SIZE, cls.MAP_SIZE, SandTile)
        fill_map(cls.MAP, 0)

        player = Player(cls.MAP.get_map_size() / 2)
        game.camera_follow_entity(player)
        ItemEntity(player.position, WoodenAxe(1))
        ItemEntity(player.position, WoodenCrate.get_item_class()(5))
        cls.spawn_buildings(game)

        saved_json = cls.dump_to_json(game)

        with open(f'{cls.SAVE_NAME}', 'w', encoding='utf-8') as f:
            f.write(saved_json)
            f.flush()

    @classmethod
    def on_end(cls, game: Game):
        pass
