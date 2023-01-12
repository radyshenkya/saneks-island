from random import randint
from typing import List
from entities.item import ItemEntity
from items import Item
from pygame_entities.entities.entity import Entity
from pygame_entities.utils.math import Vector2, clamp

from entities.map import Map


class LivingEntity(Entity):
    """
    Живая сущность. У нее есть здоровье (HP), которое можно изменять. Так же она может умереть, если HP будут равны 0.
    """

    def __init__(self, position: Vector2, max_hp: int, map: Map) -> None:
        super().__init__(position)
        self.map = map
        self.max_hp = max_hp
        self.hp = max_hp

    def add_hp(self, amount: int):
        """
        Добавляет `amount` к текущему здоровью.

        Если после добавления `amount` здоровье стало меньше или равно нулю, то вызывается метод `on_die()`
        """
        self.set_hp(self.hp + amount)

    def set_hp(self, amount: int):
        self.hp = amount

        if self.hp <= 0:
            self.on_die()

    def add_hp_strictly(self, amount: int):
        """
        То же самое, что и `add_hp()`, но HP ограничиваются параметром `max_hp`
        """
        self.add_hp(amount)
        self.hp = clamp(self.hp, 0, self.max_hp)

    def get_loot(self) -> List[Item]:
        """
        тут будет генерироваться и возвращаться список предметов, которые должны выпасть из этой сущности при смерти.
        """
        pass

    def on_die(self):
        """
        Эта функция вызывается при смерти сущности.
        По дефолту тут будут дропаться предметы из сущности, а сама сущность будет удаляться.
        Но пока что предметов нет, как и нормального функционала у этой функции :)
        """
        # спавним лутеций жестк
        for item in self.get_loot():
            ItemEntity(self.position + Vector2(randint(-128, 128),
                       randint(-128, 128)), item)
        self.destroy()
