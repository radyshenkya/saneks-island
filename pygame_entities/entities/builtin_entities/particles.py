from random import randint
from typing import List, Tuple
from pygame import Surface
from ..entity import Entity
from ...utils.math import Vector2
from ...utils.drawable import SpriteWithCameraOffset


class ParticleSystem(Entity):
    """Система партиклов"""

    def __init__(
            self,
            position: Vector2,
            particle_image: Surface,
            max_lifetime: float = 5,
            min_spawn_offset: Vector2 = Vector2(),
            max_spawn_offset: Vector2 = Vector2(),
            min_particle_velocity: Vector2 = Vector2(),
            max_particle_velocity: Vector2 = Vector2(),
            particle_image_layer: int = 0
    ) -> None:
        super().__init__(position)

        self._particle_image = particle_image

        # Particle images like: (SPRITE, TIME_STARTED_LIVING, VELOCITY)
        self._particles: List[Tuple[SpriteWithCameraOffset,
                                    float, Vector2]] = []

        self.max_lifetime = max_lifetime
        self.min_spawn_offset = min_spawn_offset
        self.max_spawn_offset = max_spawn_offset
        self.min_particle_velocity = min_particle_velocity
        self.max_particle_velocity = max_particle_velocity
        self.particle_image_layer = particle_image_layer

        self.subscribe_on_update(self.update_particles)

    def update_particles(self, _: float):
        to_delete = []

        for i, particle in enumerate(self._particles):
            particle[0].center_position = (
                particle[0].center_position[0] + particle[2].get_tuple()[0],
                particle[0].center_position[1] + particle[2].get_tuple()[1]
            )

            if self.game.scene_passed_time - particle[1] > self.max_lifetime:
                particle[0].kill()
                to_delete.append(i)

        # какой ужас
        deleted_counter = 0

        for i in to_delete:
            del self._particles[i - deleted_counter]
            deleted_counter += 1

    def burst(self, particle_count: int):
        for _ in range(particle_count):
            self._particles.append(
                (
                    SpriteWithCameraOffset(
                        self._particle_image,
                        self.particle_image_layer,
                        (self.position + Vector2.from_tuple((randint(self.min_spawn_offset.x, self.max_spawn_offset.x), randint(
                            self.min_spawn_offset.y, self.max_spawn_offset.y)))).get_tuple()
                    ),
                    self.game.scene_passed_time,
                    Vector2.from_tuple((randint(self.min_particle_velocity.x, self.max_particle_velocity.x), randint(
                        self.min_particle_velocity.y, self.max_particle_velocity.y)))
                )
            )
