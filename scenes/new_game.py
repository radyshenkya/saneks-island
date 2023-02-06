from functools import partial
import os
import pygame
from assets import FONT_30, FONT_50
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
        MainScene.QUIT_TO_SCENE = cls

        Button(Vector2(100, 100), "Create New Game",
               FONT_50, color=(255, 200, 200))

        game_name = InputField(Vector2(100, 200), "new_game", FONT_30,
                               placeholder_text="New game name")
        chunk_size = InputField(Vector2(100, 250), "10", FONT_30,
                                placeholder_text="Chunk size")
        map_size = InputField(Vector2(100, 300), "10", FONT_30,
                              placeholder_text="Map size")

        def quit_game():
            game.running = False

        def on_game_start():
            try:
                GameGenerationScene.CHUNK_SIZE = (
                    int(chunk_size.text), int(chunk_size.text))
                GameGenerationScene.MAP_SIZE = (
                    int(map_size.text), int(map_size.text))
                assert game_name.text != ''

                MainScene.FILE_TO_LOAD = f"{SAVES_FOLDER}/{game_name.text}"
                MainScene.NEEDS_TO_BE_GENERATED = True
                MainScene.NEEDS_TO_BE_LOADED = False
                game.set_scene(MainScene)
            except:
                Popup(Vector2.from_tuple(pygame.mouse.get_pos()),
                      "Something went wrong...", FONT_30)

        def start_game_from_file(file_name):
            try:
                MainScene.FILE_TO_LOAD = file_name
                MainScene.NEEDS_TO_BE_GENERATED = False
                MainScene.NEEDS_TO_BE_LOADED = True
                game.set_scene(MainScene)
            except Exception as e:
                print(e)
                Popup(Vector2.from_tuple(pygame.mouse.get_pos()),
                      "Something went wrong... ", FONT_30)

        Button(Vector2(100, 350), "Start Game",
               FONT_30, on_game_start)

        Button(Vector2(100, 400), "Exit", FONT_30,
               quit_game, color=(100, 100, 100))

        Button(Vector2(500, 100), "Load Game", FONT_50, color=(200, 255, 200))
        for i, item in enumerate(os.listdir(SAVES_FOLDER)):
            Button(Vector2(500, i * 50 + 200),
                   f"Load {item}", FONT_30, partial(start_game_from_file, f"{SAVES_FOLDER}/{item}"))

    @classmethod
    def on_end(cls, game: Game):
        pass
