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
        self.starting_position = (200, 200)
        self.rect.x = self.starting_position[0]
        self.rect.y = self.starting_position[1]
        self.speed = [0, 0]
        self.max_speed = 8
        self.acceleration = 0.3
        self.deceleration = 0.2
        self.velocity = (0, 0)
        self.key_to_move_map = {pg.K_w: self._move_up,
                                pg.K_a: self._move_left,
                                pg.K_s: self._move_down,
                                pg.K_d: self._move_right}

    def update(self):
        self.speed = [np.sign(sp) * np.max((0, np.abs(sp) - self.deceleration)) for sp in self.speed]
        self.velocity = [sp for sp in self.speed]
        self._move(self.velocity[0], self.velocity[1])

    def _check_on_boundary(self, x_pos, y_pos):
        boundary_check = super()._check_on_boundary(x_pos, y_pos)
        if boundary_check is self.BOUNCE_TOP or boundary_check is self.BOUNCE_BOTTOM:
            self.speed[1] = 0
        elif boundary_check is self.BOUNCE_RIGHT or boundary_check is self.BOUNCE_LEFT:
            self.speed[0] = 0
        return boundary_check

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

    def _move_up(self):
        self.speed = [self.speed[0], np.max((self.speed[1] - self.acceleration, -self.max_speed))]

    def _move_down(self):
        self.speed = [self.speed[0], np.min((self.speed[1] + self.acceleration, self.max_speed))]

    def _move_left(self):
        self.speed = [np.max((self.speed[0] - self.acceleration, -self.max_speed)), self.speed[1]]

    def _move_right(self):
        self.speed = [np.min((self.speed[0] + self.acceleration, self.max_speed)), self.speed[1]]

    def handle_keyboard_input(self, keys):
        for k in keys:
            if k in self.key_to_move_map:
                self.key_to_move_map[k]()
