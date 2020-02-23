import pygame as pg
import asset_getter
from base_object import Base_Object
import numpy as np

class Paddle(Base_Object):

    IMAGE_NAME = "paddle.png"
    SIZE = (20, 120)

    def __init__(self):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(asset_getter.get_asset(self.IMAGE_NAME)), self.SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 200
        self.speed = (0, 0)
        self.max_speed = 4
        self.acceleration = 0.3
        self.deceleration = 0.15
        self.velocity = (0, 0)
        self.key_to_move_map = {pg.K_w: self._move_up,
                                pg.K_a: self._move_left,
                                pg.K_s: self._move_down,
                                pg.K_d: self._move_right}

    def update(self):
        self.velocity = (0, 0)
        self.speed = [np.max((0, sp - self.deceleration)) for sp in self.speed]

    def _check_valid_move(self, x_pos, y_pos):
        within_window = self._check_on_boundary(x_pos, y_pos)
        return within_window is None

    def _move(self, dx, dy):
        new_x = self.rect.x + dx
        new_y = self.rect.y + dy
        if self._check_valid_move(new_x, new_y):
            self.rect.x = new_x
            self.rect.y = new_y
            self.velocity = (dx, dy)
            self.speed = [np.min((sp + self.acceleration, self.max_speed)) for sp in self.speed]

    def _move_up(self):
        self._move(0, -self.speed[1])

    def _move_down(self):
        self._move(0, self.speed[1])

    def _move_left(self):
        self._move(-self.speed[0], 0)

    def _move_right(self):
        self._move(self.speed[0], 0)

    def handle_keyboard_input(self, keys):
        for k in keys:
            if k in self.key_to_move_map:
                self.key_to_move_map[k]()
