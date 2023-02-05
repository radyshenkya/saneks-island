from functools import partial
import os
import pygame
from assets import FONT_30
from entities.ui import Button, InputField, Popup
from pygame_entities.game import Game
from pygame_entities.scenes import BaseScene
from pygame_entities.utils.math import Vector2
from scenes.main import MainScene
from scenes.new_game_generating import SAVES_FOLDER, GameGenerationScene


class NewGameScene(BaseScene):
    """Сцена создания новой игры"""

    @classmethod
    def on_load(cls, game: Game):
        game_name = InputField(Vector2(100, 100), "new_game", FONT_30,
                               placeholder_text="New game name")
        chunk_size = InputField(Vector2(100, 150), "10", FONT_30,
                                placeholder_text="Chunk size")
        map_size = InputField(Vector2(100, 200), "10", FONT_30,
                              placeholder_text="Map size")

        def on_game_start():
            try:
                GameGenerationScene.CHUNK_SIZE = (
                    int(chunk_size.text), int(chunk_size.text))
                GameGenerationScene.MAP_SIZE = (
                    int(map_size.text), int(map_size.text))
                assert game_name.text != ''

                GameGenerationScene.SAVE_NAME = game_name.text
                game.set_scene(GameGenerationScene)
            except:
                Popup(Vector2.from_tuple(pygame.mouse.get_pos()),
                      "Something went wrong...", FONT_30)

        def start_game_from_file(file_name):
            try:
                MainScene.FILE_TO_LOAD = file_name
                game.set_scene(MainScene)
            except Exception as e:
                print(e)
                Popup(Vector2.from_tuple(pygame.mouse.get_pos()),
                      "Something went wrong... ", FONT_30)

        new_game = Button(Vector2(100, 250), "Start Game",
                          FONT_30, on_game_start)

        for i, item in enumerate(os.listdir(SAVES_FOLDER)):
            Button(Vector2(400, i * 50 + 100),
                   f"Load {item}", FONT_30, partial(start_game_from_file, f"{SAVES_FOLDER}/{item}"))

    @classmethod
    def on_end(cls, game: Game):
        pass
