import pygame as pg
import asset_getter
import random
from base_object import Base_Object


class Ball(Base_Object):

    IMAGE_NAME = "ball.png"
    SIZE = (30, 30)

    def __init__(self):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(asset_getter.get_asset(self.IMAGE_NAME)), self.SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

        self.velocity = [random.randint(-5, 5), random.randint(-5, 5)]

    def bounce(self, collider_velocity, type):
        dx = collider_velocity[0]
        dy = collider_velocity[1]
        if type == self.BOUNCE_TOP:
            dx += self.velocity[0]
            dy += -self.velocity[1]
        elif type == self.BOUNCE_BOTTOM:
            dx += self.velocity[0]
            dy += -self.velocity[1]
        elif type == self.BOUNCE_LEFT:
            dx += -self.velocity[0]
            dy += self.velocity[1]
        elif type == self.BOUNCE_RIGHT:
            dx += -self.velocity[0]
            dy += self.velocity[1]

        self.velocity[0] = dx
        self.velocity[1] = dy

    def update(self):
        bounce_type = self._check_on_boundary(self.rect.x, self.rect.y)
        if bounce_type is not None:
            self.bounce((0, 0), bounce_type)
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
