"""
Тут хранится класс игрока, и все что с ним связано
"""
from functools import partial
from typing import List
from entities.item import ItemEntity
from entities.living_entities import LivingEntity
from entities.ui import UI_LAYER, Button, Image, UIElementsContainer, ActionsPanel
from entities.util_entities import OnMapSpriteMixin
from entities.map import Map
from assets import FONT_PATH, Sprites, SPRITE_SIZE, SPRITESHEET_UPSCALE
from items import Inventory, Item, UsableItem
from pygame_entities.entities.entity import Entity

from pygame_entities.utils.drawable import AnimatedSpriteWithCameraOffset
from pygame_entities.utils.math import Vector2
from pygame_entities.entities.mixins import BlockingCollisionMixin, VelocityMixin

import pygame


class Player(LivingEntity, OnMapSpriteMixin, BlockingCollisionMixin, VelocityMixin):
    FRONT_IDLE_ANIM = [Sprites.PLAYER_FRONT_1]
    FRONT_MOVE_ANIM = [Sprites.PLAYER_FRONT_1, Sprites.PLAYER_FRONT_2,
                       Sprites.PLAYER_FRONT_3, Sprites.PLAYER_FRONT_4]
    BACK_MOVE_ANIM = [Sprites.PLAYER_BACK_1, Sprites.PLAYER_BACK_2,
                      Sprites.PLAYER_BACK_3, Sprites.PLAYER_BACK_4]
    LEFT_MOVE_ANIM = [Sprites.PLAYER_LEFT_1, Sprites.PLAYER_LEFT_2,
                      Sprites.PLAYER_LEFT_3, Sprites.PLAYER_LEFT_4]
    RIGHT_MOVE_ANIM = [Sprites.PLAYER_RIGHT_1, Sprites.PLAYER_RIGHT_2,
                       Sprites.PLAYER_RIGHT_3, Sprites.PLAYER_RIGHT_4]

    COLLIDER_SIZE = Vector2(20, 20) * SPRITESHEET_UPSCALE

    # В тайл/сек.
    DEFAULT_SPEED = 3
    DEFAULT_HP = 10
    INVENTORY_SLOTS_COUNT = 10

    ITEMS_PICKUP_RADIUS = 128

    def __init__(self, position: Vector2, tile_map: Map) -> None:
        super().__init__(position, self.DEFAULT_HP, tile_map)
        self.set_speed(self.DEFAULT_SPEED)

        self.sprite_init(AnimatedSpriteWithCameraOffset(
            self.FRONT_IDLE_ANIM, 0.2), Vector2())

        self.last_animation = self.FRONT_IDLE_ANIM

        self.inventory: Inventory = Inventory(
            slots_count=self.INVENTORY_SLOTS_COUNT)

        self.selected_item_slot = 0

        self.collision_init(self.COLLIDER_SIZE)
        self.velocity_init(False, 0.1)

        self.inventory_panel = InventoryPanelUI(self)
        self.selected_slot_panel = SelectedSlotPanel(self)

        self.subscribe_on_update(self.move_player)
        self.subscribe_on_update(self.animate)
        self.subscribe_for_event(self.keys_handler, pygame.KEYDOWN)
        self.subscribe_for_event(
            self.mouse_buttons_handler, pygame.MOUSEBUTTONDOWN)
        self.subscribe_for_event(
            self.mouse_wheel_handler, pygame.MOUSEWHEEL)

        self.update_ui()

    def move_player(self, delta_time: float):
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

        self.velocity = direction.normalized() * self.speed * delta_time

    def keys_handler(self, event: pygame.event.Event):
        if event.key == pygame.K_f:
            self.pickup_nearest_items()

        elif event.key == pygame.K_i:
            self.toggle_inventory_panel()

        elif event.key == pygame.K_q:
            self.drop_item_from_inventory(self.selected_item_slot)

    def mouse_buttons_handler(self, event: pygame.event.Event):
        if event.button == 3:
            # ПКМ
            self.use_selected_item()

    def mouse_wheel_handler(self, event: pygame.event.Event):
        self.selected_item_slot -= event.y
        self.selected_item_slot %= self.inventory.slots

        self.update_ui()

    def toggle_inventory_panel(self):
        if self.inventory_panel.is_visible:
            self.inventory_panel.hide()
        else:
            self.inventory_panel.render()

    def pickup_nearest_items(self):
        for ent in self.game.enabled_entities:
            if not type(ent) == ItemEntity or (ent.position - self.position).magnitude() > self.ITEMS_PICKUP_RADIUS:
                continue

            ent: ItemEntity
            ent.item = self.inventory.add_item(ent.item)

        self.update_ui()

    def use_selected_item(self):
        selected_item = self.inventory.get_slot(self.selected_item_slot)

        if not isinstance(selected_item, UsableItem):
            return

        selected_item.use(initiator=self)

        if selected_item.amount <= 0:
            self.inventory.set_slot(None, self.selected_item_slot)

        self.update_ui()

    def update_ui(self):
        if self.inventory_panel.is_visible:
            self.inventory_panel.render()

        self.selected_slot_panel.render()

    def animate(self, delta_time: float):
        if self.velocity.x > 0:
            self.last_animation = self.LEFT_MOVE_ANIM
        elif self.velocity.x < 0:
            self.last_animation = self.RIGHT_MOVE_ANIM
        elif self.velocity.y > 0:
            self.last_animation = self.FRONT_MOVE_ANIM
        elif self.velocity.y < 0:
            self.last_animation = self.BACK_MOVE_ANIM
        else:
            self.last_animation = self.FRONT_IDLE_ANIM

        if self.sprite.frames != self.last_animation:
            self.sprite.frames = self.last_animation

    def drop_item_from_inventory(self, slot_index: int):
        if self.inventory.get_slot(slot_index) is None:
            return

        ItemEntity(self.position, self.inventory.swap_slot(slot_index, None))

        self.update_ui()

    def get_loot(self) -> List[Item]:
        return [item for item in self.inventory.grid if not item is None]

    def set_speed(self, tiles_in_second: float) -> None:
        self.speed = tiles_in_second * SPRITE_SIZE[0]
        print(self.speed)


# за такую реализацию убить мало, но как бы другие фичи проекта до 19 сами себя не сделают, поэтому как то так
class InventoryPanelUI(UIElementsContainer):
    """
    UI панелька инвентаря
    """
    SCREEN_PANEL_OFFSET = Vector2(0, 0)
    FONT_SIZE = 40
    ITEM_ACTIONS_LIST_OFFSET = Vector2(400, 0)

    def __init__(self, player: Player) -> None:
        super().__init__(self.SCREEN_PANEL_OFFSET)

        self.player = player
        self.font = pygame.font.Font(FONT_PATH, self.FONT_SIZE)
        self.current_selected_item_index = 0

    def render(self):
        super().render()

        self.add_element(
            Button(Vector2(), "Inventory", self.font))

        def on_slot_click(i):
            index = i
            self.current_selected_item_index = index
            self.item_actions_context_menu()

        for i in range(self.player.inventory.slots):
            item = self.player.inventory.get_slot(i)

            if item is None:
                continue

            self.add_element(Button(Vector2(
                0, (i + 1) * self.FONT_SIZE), f"{item.NAME} x{item.amount}", self.font,
                partial(on_slot_click, i), color=(150, 255, 200) if i == self.player.selected_item_slot else (255, 255, 255)
            ))

    def item_actions_context_menu(self):
        mouse_pos = pygame.mouse.get_pos()
        item = self.player.inventory.get_slot(self.current_selected_item_index)

        if item is None:
            return

        def drop(index):
            self.player.drop_item_from_inventory(index)
            self.render()

        action_list = ActionsPanel(Vector2.from_tuple(
            mouse_pos), f"{self.current_selected_item_index + 1}. {item.NAME} x{item.amount}", {"drop": partial(drop, self.current_selected_item_index)}, self.font)
        action_list.render()
        self.add_element(action_list, False)


class SelectedSlotPanel(UIElementsContainer):
    FONT_SIZE = 30

    def __init__(self, player: Player):
        super().__init__(Vector2())

        self.font = pygame.font.Font(FONT_PATH, self.FONT_SIZE)

        # Вычисляем позицию этой штуки
        pos = Vector2(Sprites.ITEM_SLOT.get_width() / 2,
                      self.game.screen_resolution[1] - Sprites.ITEM_SLOT.get_height() / 2)

        self.position = pos

        self.player = player

    def render(self):
        super().render()

        self.add_element(Image(Vector2(), Sprites.ITEM_SLOT, UI_LAYER - 1))

        displaying_item = self.player.inventory.get_slot(
            self.player.selected_item_slot)

        if displaying_item is None:
            return

        # Надпись предмета
        self.add_element(
            Button(Vector2(-Sprites.ITEM_SLOT.get_width() / 2, -Sprites.ITEM_SLOT.get_height() / 2 - self.FONT_SIZE), f"{displaying_item.NAME} x{displaying_item.amount}", self.font))

        # Картинка предмета
        self.add_element(Image(Vector2(), displaying_item.IMAGE))
