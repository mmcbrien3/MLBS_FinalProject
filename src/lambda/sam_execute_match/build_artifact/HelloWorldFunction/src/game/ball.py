import pygame as pg
import src.game.asset_getter as asset_getter
from src.game.base_object import BaseObject
import numpy as np

class Ball(BaseObject):

    IMAGE_NAME = "ball.png"
    SIZE = (30, 30)

    def __init__(self):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(asset_getter.get_asset(self.IMAGE_NAME)), self.SIZE)
        self.rect = self.image.get_rect()
        self.starting_position = (500 - self.SIZE[0] // 2, 300 - self.SIZE[1] // 2)
        self.rect.x = self.starting_position[0]
        self.rect.y = self.starting_position[1]
        self.deceleration = .01

        self.velocity = self._make_random_starting_velocity()

    def reset_to_starting_position(self):
        super().reset_to_starting_position()
        self.velocity = self._make_random_starting_velocity()

    def _make_random_starting_velocity(self):
        initial_velocity = np.random.randint(-8, 8)
        return [np.random.choice([-3, 3]), np.sign(initial_velocity + 0.1) * np.max((3, np.abs(initial_velocity)))]

    def bounce(self, collider_velocity, type, other_x, other_y, other_size):
        dx = 1.2 * collider_velocity[0]
        dy = 1.2 * collider_velocity[1]
        if type == self.BOUNCE_TOP:
            if other_x is not None:
                self.rect.y = other_y + other_size[1]
            dx += self.velocity[0]
            dy += -self.velocity[1]
        elif type == self.BOUNCE_BOTTOM:
            if other_x is not None:
                self.rect.y = other_y - self.SIZE[1]
            dx += self.velocity[0]
            dy += -self.velocity[1]
        elif type == self.BOUNCE_LEFT:
            if other_x is not None:
                self.rect.x = other_x + other_size[0]
            dx += -self.velocity[0]
            dy += self.velocity[1]
        elif type == self.BOUNCE_RIGHT:
            if other_x is not None:
                self.rect.x = other_x - self.SIZE[1]
            dx += -self.velocity[0]
            dy += self.velocity[1]

        self.velocity[0] = dx
        self.velocity[1] = dy

    def update(self):
        bounce_type = self._check_on_boundary(self.rect.x, self.rect.y)
        if bounce_type is not None:
            self.bounce((0, 0), bounce_type, None, None, None)
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        self.velocity = [np.sign(v) * np.max((0, np.abs(v) - self.deceleration)) for v in self.velocity]

    def check_for_bounces(self, objects):
        paddles_hit = []
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                self.bounce(obj.velocity,
                            self._calc_bounce_type(self.rect.x,
                                                   self.rect.y,
                                                   obj.rect.x,
                                                   obj.rect.y,
                                                   obj.SIZE),
                            obj.rect.x,
                            obj.rect.y,
                            obj.SIZE)
                paddles_hit.append(obj)
        return paddles_hit
