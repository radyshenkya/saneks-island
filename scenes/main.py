from json import loads, dumps
from assets import FONT_30
from entities.json_parser import json_dict_into_object
from entities.player import Player
from entities.ui import Button
from pygame_entities.game import Game
from pygame_entities.scenes import BaseScene
from entities.json_parser import registered_classes
from pygame_entities.utils.math import Vector2
from scenes.new_game_generating import GameGenerationScene


class MainScene(BaseScene):
    """Сцена самой игры как бы да ок"""

    FILE_TO_LOAD = "./saves/unknown_game"
    NEEDS_TO_BE_LOADED = True
    NEEDS_TO_BE_GENERATED = False
    QUIT_TO_SCENE = None

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
        def quit_to_main_menu():
            game.set_scene(cls.QUIT_TO_SCENE)

        Button(Vector2.from_tuple(game.screen_resolution) - Vector2(200, game.screen_resolution[1]),
               "Quit To Menu",
               FONT_30,
               quit_to_main_menu,
               color=(255, 200, 255))

        if cls.NEEDS_TO_BE_LOADED:
            try:
                json_dict = None

                with open(cls.FILE_TO_LOAD, 'r') as f:
                    json_dict = loads(f.read())

                for ent_dict in json_dict['entities']:
                    ent = json_dict_into_object(ent_dict)

                    if isinstance(ent, Player):
                        game.camera_follow_entity(ent)
            except:
                quit_to_main_menu()
                return

        if cls.NEEDS_TO_BE_GENERATED:
            GameGenerationScene.SAVE_NAME = cls.FILE_TO_LOAD
            GameGenerationScene.on_load(game)

    @classmethod
    def on_end(cls, game: Game):
        saved_json = cls.dump_to_json(game)

        with open(f'{cls.FILE_TO_LOAD}', 'w', encoding='utf-8') as f:
            f.write(saved_json)
            f.flush()
