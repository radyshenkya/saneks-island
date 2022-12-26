from typing import List
from pygame_entities.entities.entity import Entity
from pygame_entities.utils.math import Vector2, clamp


class LivingEntity(Entity):
    """
    Живая сущность. У нее есть здоровье (HP), которое можно изменять. Так же она может умереть, если HP будут равны 0.
    """

    def __init__(self, position: Vector2, max_hp: int) -> None:
        super().__init__(position)

        self.max_hp = max_hp
        self.hp = max_hp

    def add_hp(self, amount: int):
        """
        Добавляет `amount` к текущему здоровью.

        Если после добавления `amount` здоровье стало меньше или равно нулю, то вызывается метод `on_die()`
        """
        self.hp = self.hp + amount

        if self.hp <= 0:
            self.on_die()

    def add_hp_strictly(self, amount: int):
        """
        То же самое, что и `add_hp()`, но HP ограничиваются параметром `max_hp`
        """
        self.add_hp(amount)
        self.hp = clamp(self.hp, 0, self.max_hp)

    def get_loot(self) -> List:
        """
        тут будет генерироваться и возвращаться список предметов, которые должны выпасть из этой сущности при смерти,
        но т.к. пока что айтемов нет, он бесполезен.
        """
        pass

    def on_die(self):
        """
        Эта функция вызывается при смерти сущности.
        По дефолту тут будут дропаться предметы из сущности, а сама сущность будет удаляться.
        Но пока что предметов нет, как и нормального функционала у этой функции :)
        """
        self.destroy()
