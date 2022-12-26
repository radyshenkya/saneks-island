from pygame_entities.utils.math import Vector2
from pygame_entities.entities.mixins import SpriteMixin
from pygame_entities.utils.drawable import BaseSprite


class OnMapSpriteMixin(SpriteMixin):
    """
    Миксин, основанный на SpriteMixin, который устанавливает слой спрайта по его Y координате в пространстве.
    Нужен, что бы сущности на карте которые находятся выше рисовались как бы за теми сущностями, которые находятся ниже.
    """

    def sprite_init(self, sprite: BaseSprite, sprite_position_offset: Vector2) -> None:
        super().sprite_init(sprite, sprite_position_offset)
        self.subscribe_on_update(self.set_level_by_y_pos)

    def set_level_by_y_pos(self, _):
        self.sprite.layer = self.position
