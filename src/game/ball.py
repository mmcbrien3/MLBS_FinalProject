import pygame as pg
import asset_getter
import random

class Ball(pg.sprite.Sprite):

    SIZE = (30, 30)
    BOUNCE_LEFT = "left"
    BOUNCE_RIGHT = "right"
    BOUNCE_TOP = "top"
    BOUNCE_BOTTOM = "bottom"

    def __init__(self):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(asset_getter.get_asset("munns.png")), self.SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

        self.velocity = [random.randint(-5, 5), random.randint(-5, 5)]

    def _check_on_boundary(self):
        if self.rect.x - 0 <= 0:
            return self.BOUNCE_LEFT
        if self.rect.x + self.SIZE[0] >= 1000:
            return self.BOUNCE_RIGHT
        if self.rect.y - 0 <= 0:
            return self.BOUNCE_TOP
        if self.rect.y + self.SIZE[1] >= 600:
            return self.BOUNCE_BOTTOM

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
        bounce_type = self._check_on_boundary()
        if bounce_type is not None:
            self.bounce((0, 0), bounce_type)
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y