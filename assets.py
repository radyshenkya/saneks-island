from pygame_entities.utils.spritesheets import SpriteSheet
from pygame.transform import scale
from pygame.image import load

import pygame

SPRITESHEET_PATH = "assets/sprites/spritesheet.png"

# Во сколько раз апскейлятся спрайты на спрайтшите
SPRITESHEET_UPSCALE = 5

# Оригинальный размер всего спрайтшита
SPRITESHEET_ORIGINAL_SIZE = (1024, 1024)
# Размеры апскейльнутого спрайтшита
SPRITESHEET_SIZE = (SPRITESHEET_ORIGINAL_SIZE[0] * SPRITESHEET_UPSCALE,
                    SPRITESHEET_ORIGINAL_SIZE[1] * SPRITESHEET_UPSCALE)

# Оригинальный размер спрайта
SPRITE_ORIGINAL_SIZE = (32, 32)
# Размеры одного спрайта в пикселях, учитывая апскейл.
SPRITE_SIZE = (SPRITE_ORIGINAL_SIZE[0] * SPRITESHEET_UPSCALE,
               SPRITE_ORIGINAL_SIZE[1] * SPRITESHEET_UPSCALE)

# Спрайтшит
SPRITESHEET = SpriteSheet(
    *SPRITE_SIZE, scale(load(SPRITESHEET_PATH), SPRITESHEET_SIZE))


class Sprites:
    """
    Хранит в себе все спрайты из игры объектами pygame.Surface
    """
    SAND_1 = SPRITESHEET.image_at((0, 0))
    SAND_2 = SPRITESHEET.image_at((0, 1))
    SAND_3 = SPRITESHEET.image_at((0, 2))
    SAND_4 = SPRITESHEET.image_at((0, 3))

    GRASS_1 = SPRITESHEET.image_at((1, 0))
    GRASS_2 = SPRITESHEET.image_at((1, 1))
    GRASS_3 = SPRITESHEET.image_at((1, 2))
    GRASS_4 = SPRITESHEET.image_at((1, 3))

    WATER = SPRITESHEET.image_at((0, 4))

    FIRE_1 = SPRITESHEET.image_at((2, 0))
    FIRE_2 = SPRITESHEET.image_at((3, 0))
    FIRE_3 = SPRITESHEET.image_at((4, 0))
    FIRE_4 = SPRITESHEET.image_at((5, 0))

    SPLASH_1 = SPRITESHEET.image_at((6, 0))
    SPLASH_2 = SPRITESHEET.image_at((7, 0))
    SPLASH_3 = SPRITESHEET.image_at((8, 0))
    SPLASH_4 = SPRITESHEET.image_at((9, 0))
    SPLASH_5 = SPRITESHEET.image_at((10, 0))

    STONE = SPRITESHEET.image_at((2, 1))
    STONE_WITH_AMETHYST = SPRITESHEET.image_at((3, 1))
    STONE_WITH_GOLD = SPRITESHEET.image_at((4, 1))
    STONE_WITH_COAL = SPRITESHEET.image_at((5, 1))
    STONE_WITH_IRON = SPRITESHEET.image_at((3, 2))
    STONE_WITH_IRON_2 = SPRITESHEET.image_at((4, 2))

    ROCK = SPRITESHEET.image_at((5, 2))
    GOLD_INGOT = SPRITESHEET.image_at((6, 2))
    IRON_INGOT = SPRITESHEET.image_at((7, 2))
    COAL = SPRITESHEET.image_at((2, 3))
    AMETHYST = SPRITESHEET.image_at((3, 3))
    GOLD = SPRITESHEET.image_at((4, 3))
    IRON = SPRITESHEET.image_at((5, 3))

    GRAVE = SPRITESHEET.image_at((2, 4))
    GRAVE_WITH_FLOWERS = SPRITESHEET.image_at((3, 4))

    BAG = SPRITESHEET.image_at((4, 4))

    ITEM_SLOT = SPRITESHEET.image_at((5, 4))

    MARK_SIGN = SPRITESHEET.image_at((6, 3))
    CROSS_SIGH = SPRITESHEET.image_at((7, 3))

    WOOD = SPRITESHEET.image_at((6, 4))
    LEAVES = SPRITESHEET.image_at((7, 4))
    STRING = SPRITESHEET.image_at((8, 4))

    PICKAXE_GOLD = SPRITESHEET.image_at((0, 5))
    PICKAXE_IRON = SPRITESHEET.image_at((1, 5))
    PICKAXE_STONE = SPRITESHEET.image_at((2, 5))
    PICKAXE_WOOD = SPRITESHEET.image_at((3, 5))

    SWORD_GOLD = SPRITESHEET.image_at((4, 5))
    SWORD_IRON = SPRITESHEET.image_at((5, 5))
    SWORD_STONE = SPRITESHEET.image_at((6, 5))
    SWORD_WOOD = SPRITESHEET.image_at((7, 5))

    CRATE = SPRITESHEET.image_at((7, 6))

    COOKED_MEAT = SPRITESHEET.image_at((8, 6))
    RAW_MEAT = SPRITESHEET.image_at((9, 6))

    SKULL = SPRITESHEET.image_at((8, 2))

    FURNACE = SPRITESHEET.image_at((6, 1))
    CHEST = SPRITESHEET.image_at((7, 1))
    WORKBENCH = SPRITESHEET.image_at((8, 1))
    CAMPFIRE = SPRITESHEET.image_at((9, 1))

    PIE = SPRITESHEET.image_at((11, 0))

    BLOODPARTICLE = SPRITESHEET.image_at((8, 3))

    PLAYER_FRONT_1 = SPRITESHEET.image_at((10, 1))
    PLAYER_FRONT_2 = SPRITESHEET.image_at((10, 2))
    PLAYER_FRONT_3 = SPRITESHEET.image_at((10, 3))
    PLAYER_FRONT_4 = SPRITESHEET.image_at((10, 4))

    PLAYER_BACK_1 = SPRITESHEET.image_at((11, 1))
    PLAYER_BACK_2 = SPRITESHEET.image_at((11, 2))
    PLAYER_BACK_3 = SPRITESHEET.image_at((11, 3))
    PLAYER_BACK_4 = SPRITESHEET.image_at((11, 4))

    PLAYER_LEFT_1 = SPRITESHEET.image_at((9, 2))
    PLAYER_LEFT_2 = SPRITESHEET.image_at((9, 3))
    PLAYER_LEFT_3 = SPRITESHEET.image_at((9, 4))
    PLAYER_LEFT_4 = SPRITESHEET.image_at((9, 5))

    PLAYER_RIGHT_1 = SPRITESHEET.image_at((12, 3))
    PLAYER_RIGHT_2 = SPRITESHEET.image_at((12, 4))
    PLAYER_RIGHT_3 = SPRITESHEET.image_at((12, 5))
    PLAYER_RIGHT_4 = SPRITESHEET.image_at((12, 6))

    SPIDER_1 = SPRITESHEET.image_at((11, 5))
    SPIDER_2 = SPRITESHEET.image_at((11, 6))
    SPIDER_3 = SPRITESHEET.image_at((11, 5))
    SPIDER_4 = SPRITESHEET.image_at((10, 6))

    COBWEB = SPRITESHEET.image_at((10, 5))

    SNAKE_LEFT = SPRITESHEET.image_at((12, 1))
    SNAKE_UP = SPRITESHEET.image_at((13, 1))
    SNAKE_RIGHT = SPRITESHEET.image_at((13, 2))
    SNAKE_DOWN = SPRITESHEET.image_at((12, 2))

    BUSH = SPRITESHEET.image_at((13, 0))
    BUSH_WITH_BERRIES = SPRITESHEET.image_at((14, 0))

    PALMTREE_1 = SPRITESHEET.image_at((12, 0))
    PALMTREE_2 = SPRITESHEET.image_at((15, 0), (1, 2))
    PALMTREE_3 = SPRITESHEET.image_at((16, 0), (1, 2))


FONT_PATH = "assets/fonts/font.ttf"

# а так низя) ибо надо сначала пигейм инициализировать, да и так-то у нас много размеров шрифтов будет, поэтому не надо это тут
# FONT_16 = pygame.font.Font(FONT_PATH, 16)  # Дефолтный шрифт в проекте
