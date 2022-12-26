from pygame_entities.utils.math import Vector2
from pygame_entities.utils.drawable import BaseSprite, SpriteWithCameraOffset
from pygame_entities.game import Game
from pygame_entities.entities.mixins import SpriteMixin, BlockingCollisionMixin, VelocityMixin
import pygame
from inspect import getsourcefile
import os.path as path
import sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])

if True:
    from assets import Sprites, SPRITE_SIZE
    from entities.map import Map, SandTile, fill_map

RESOLUTION = (800, 640)
FRAMERATE = 60
VOID_COLOR = (50, 50, 50)  # Цвет фона


class TestPlayer(SpriteMixin, BlockingCollisionMixin, VelocityMixin):
    SPEED = 500

    def __init__(self, position: Vector2, sprite: BaseSprite) -> None:
        super().__init__(position)

        self.sprite_init(sprite)
        self.velocity_init(False, 0.1)
        self.collision_init(Vector2(*SPRITE_SIZE), False)
        self.subscribe_on_update(self.player_move)

    def player_move(self, delta_time: float):
        keys = pygame.key.get_pressed()

        direction = Vector2()

        if keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1

        self.velocity = direction.normalized() * TestPlayer.SPEED * delta_time


def on_quit_event(event: pygame.event.Event):
    """
    Нужна для выхода из игры по крестику окна.
    """
    Game.get_instance().running = False


def main() -> None:
    game = Game.get_instance(RESOLUTION, FRAMERATE, VOID_COLOR)
    game.subsribe_for_event(on_quit_event, pygame.QUIT)

    # Создаем карту размерами 100x100 тайлов, с чанками 10x10
    tile_map = Map(Vector2(), (10, 10), (10, 10), SandTile)

    # Генерируем карту
    fill_map(tile_map, 1)

    player = TestPlayer(Vector2(100, 100), SpriteWithCameraOffset(
        Sprites.PLAYER_FRONT_1, 0))

    game.camera_follow_entity(player)

    game.run()


if __name__ == "__main__":
    main()
