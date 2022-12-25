from typing import List, Tuple
from random import choices, choice

from assets import Sprites, SPRITE_SIZE

from pygame_entities.game import Game
from pygame_entities.entities.mixins import CollisionMixin
from pygame_entities.entities.entity import Entity
from pygame_entities.utils.drawable import BaseSprite, SpriteWithCameraOffset
from pygame_entities.utils.math import Vector2

import pygame
from perlin_noise import PerlinNoise


MAP_LAYER = -1000


class Tile:
    """
    Базовый класс тайла
    """
    image: pygame.Surface = None

    @classmethod
    def get_image(cls) -> pygame.Surface:
        return cls.image


class RandomVariatedTiles(Tile):
    """
    Тайл с рандомными картинками
    """
    images: List[pygame.Surface] = list()
    weights: List[float] = None
    is_weighted = False

    @classmethod
    def get_image(cls) -> pygame.Surface:
        if cls.is_weighted:
            return choices(cls.images, cls.weights, k=1)[0]
        else:
            return choice(cls.images)


class SandTile(RandomVariatedTiles):
    """Тайл песочка"""
    images = [Sprites.SAND_1, Sprites.SAND_2, Sprites.SAND_4,
              Sprites.SAND_3]
    weights = [0.5, 0.5, 0.4, 0.01]
    is_weighted = True


class GrassTile(RandomVariatedTiles):
    """Тайл травы"""  # где то тут снуп дог задумался о своем стартапе в айти
    images = [Sprites.GRASS_1, Sprites.GRASS_2,
              Sprites.GRASS_3, Sprites.GRASS_4]
    weights = [0.5, 0.3, 0.3, 0.001]
    is_weighted = True


class WaterTile(Tile):
    """Тайл воды"""
    image = Sprites.WATER


class Chunk:
    """
    Чанк из тайлов. Используется сущностью Map
    """

    def __init__(self, size: Tuple[int, int], default_tile: Tile, position: Vector2, tile_size: Tuple[int, int]) -> None:
        self.tile_size = tile_size
        self.game = Game.get_instance()
        self.position = position
        self.height = size[1]
        self.width = size[0]
        self.tiles = [[default_tile for _ in range(
            size[0])] for _ in range(size[1])]
        self.sprites: List[BaseSprite] = list()
        self.is_hidden = False

    def hide(self):
        """
        Прячет все отображаемые тайлы чанка
        """
        if self.is_hidden:
            return

        for sprite in self.sprites:
            sprite.kill()

        self.sprites = list()

        self.is_hidden = True

    def render(self):
        """
        Рендерит все тайлы в чанке
        """

        if not self.is_hidden:
            return

        for row in range(self.height):
            for col in range(self.width):
                tile = self.tiles[row][col]

                tile_image = tile.get_image()
                x = self.position.x + self.tile_size[0] * col
                y = self.position.y + self.tile_size[1] * row

                self.sprites.append(SpriteWithCameraOffset(
                    tile_image, MAP_LAYER, (int(x), int(y))))

        self.is_hidden = False

    def reload(self):
        """
        Перезагружает чанк
        """
        if self.is_hidden:
            return

        self.hide()
        self.render()

    def set_tile(self, position: Tuple[int, int], tile):
        """
        Установить тайл в чанке. Координаты относительно чанка
        """
        self.tiles[position[1]][position[0]] = tile

    def get_tile(self, position: Tuple[int, int]) -> Tile:
        """
        Получить тайл в чанке. Координаты относительно чанка
        """
        return self.tiles[position[1]][position[0]]

    def get_center_position(self) -> Vector2:
        """
        Получить позицию центра чанка в мире 
        """
        return self.position + Vector2((self.width * self.tile_size[0]) / 2, (self.height * self.tile_size[1]) / 2)


class MapBorder(CollisionMixin):
    """
    Сущность границы тайловой карты aka невидимая стенка.
    """

    def __init__(self, position: Vector2, collider_size: Vector2) -> None:
        super().__init__(position)
        self.collision_init(collider_size)


class Map(Entity):
    """
    Сущность тайловой карты.
    """
    RENDER_RADIUS = 5000

    def __init__(self, position: Vector2, chunk_size: Tuple[int, int], map_size: Tuple[int, int], default_tile: Tile) -> None:
        super().__init__(position)

        self.map_size = map_size
        self.tile_size = SPRITE_SIZE
        self.chunk_size = chunk_size
        self.chunks = [[Chunk(chunk_size, default_tile, Vector2(
            col * chunk_size[0] * self.tile_size[0], row * chunk_size[1] * self.tile_size[1]), self.tile_size) for col in range(map_size[0])] for row in range(map_size[1])]

        for row in self.chunks:
            for chunk in row:
                chunk.reload()

        # Создание границ мира
        map_size: Vector2 = self.get_map_size()
        self.left_border = MapBorder(
            Vector2(-map_size.x / 2, map_size.y / 2), map_size)
        self.right_border = MapBorder(
            Vector2(map_size.x + map_size.x / 2 - SPRITE_SIZE[0], map_size.y / 2), map_size)
        self.top_border = MapBorder(
            Vector2(map_size.x / 2, -map_size.y / 2), map_size)
        self.bottom_border = MapBorder(
            Vector2(map_size.x / 2, map_size.y + map_size.y / 2 - SPRITE_SIZE[1]), map_size)

        self.subscribe_on_update(self.render_chunks)
        self.subscribe_on_destroy(self.destroy_borders)

    def render_chunks(self, delta_time: float):
        """
        Рендерит чанки в мире. Вызывается каждый кадр
        """
        for row in self.chunks:
            for chunk in row:
                if (self.game.camera_center_position - chunk.get_center_position()).magnitude() > Map.RENDER_RADIUS:
                    chunk.hide()
                else:
                    chunk.render()

    def get_map_size_in_tiles(self) -> Tuple[int, int]:
        """
        Размер карты в тайлах
        """
        return (self.map_size[0] * self.chunk_size[0], self.map_size[1] * self.chunk_size[1])

    def get_tile(self, tile_position: Tuple[int, int]) -> Tile:
        """
        Получить значение тайла. Принимаются абсолютные координаты
        """
        chunk_x = tile_position[0] // self.chunk_size[0]
        chunk_y = tile_position[1] // self.chunk_size[1]

        tile_x = tile_position[0] - chunk_x * self.chunk_size[0]
        tile_y = tile_position[1] - chunk_y * self.chunk_size[1]

        return self.chunks[chunk_y][chunk_x].get_tile((tile_x, tile_y))

    def set_tile(self, tile_position: Tuple[int, int], new_tile, reload=True):
        """
        Установить значение для тайла. Принимаются абсолютные координаты
        """
        chunk_x = tile_position[0] // self.chunk_size[0]
        chunk_y = tile_position[1] // self.chunk_size[1]

        tile_x = tile_position[0] - chunk_x * self.chunk_size[0]
        tile_y = tile_position[1] - chunk_y * self.chunk_size[1]

        self.chunks[chunk_y][chunk_x].set_tile((tile_x, tile_y), new_tile)
        if reload:
            self.chunks[chunk_y][chunk_x].reload()

    def get_map_size(self) -> Vector2:
        """
        Размер карты в мире
        """
        return Vector2(self.get_map_size_in_tiles()[0] * self.tile_size[0], self.get_map_size_in_tiles()[1] * self.tile_size[1])

    def get_tile_position(self, tile_position: Tuple[int, int]) -> Vector2:
        """
        Позиция тайла в мире
        """
        return Vector2(self.tile_size[0] * tile_position[0], self.tile_size[1] * tile_position[1])

    def destroy_borders(self):
        """
        Убирает границы карты.
        Вызывается при удалении сущности карты
        """
        self.right_border.destroy()
        self.left_border.destroy()
        self.top_border.destroy()
        self.bottom_border.destroy()


def fill_map(map: Map, seed: int, noise_multiplier=0.1):
    """
    Заполняет всю карту рандомно по каким-то условиям.
    """

    # Тут мы указываем тайлы, используемые в генерации.
    # Тайлы идут от самого низкого, до самого высокого
    # Можно вставлять тайлы когда захочется, в алгоритме нет привязки именно к 3 тайлам.
    floor_tiles = [WaterTile, SandTile, GrassTile]

    map_center = Vector2(map.get_map_size_in_tiles()[
        0], map.get_map_size_in_tiles()[1]) / 2

    # Тут инициализируется объект для работы с шумом перлина с заданным сидом и 2 октавами
    perlin = PerlinNoise(2, seed)

    # Это нужно для закругления суши на карте, что бы по краям была вода, а в центре было сухенько
    max_magnitude = map_center.magnitude()

    for x in range(map.get_map_size_in_tiles()[0]):
        for y in range(map.get_map_size_in_tiles()[1]):

            # Вычисляем легендарный шум перлина для текущего тайла
            # +0.1 используется всегда, ибо если у нас будет ровное число (без чисел после запятой)
            # то шум перлина будет выдавать константное значение
            noise = perlin((noise_multiplier * x + 0.1,
                           noise_multiplier * y + 0.1)) + 1  # + 0.6

            # Эффект скругления суши. Чем ближе к центру карты - тем больше шанс того, что там будет не вода
            # Помоему эта формула имеет что-то общее с градиентом гаусса, но на самом деле я ее выдумал
            noise *= (max_magnitude - (map_center - Vector2(x, y)
                                       ).magnitude()) / max_magnitude

            # Тут идет вычисление индекса на основе результатов нашего шума
            tile_index = max(
                min(int(noise * len(floor_tiles)), len(floor_tiles) - 1), 0
            )
            map.set_tile((x, y), floor_tiles[tile_index], False)

    # Перезагрузка всех чанков
    for row in map.chunks:
        for chunk in row:
            chunk.reload()
