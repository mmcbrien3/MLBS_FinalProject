import pygame as pg
import numpy as np

class Base_Object(pg.sprite.Sprite):

    IMAGE_NAME = None
    SIZE = None
    BOUNCE_LEFT = "left"
    BOUNCE_RIGHT = "right"
    BOUNCE_TOP = "top"
    BOUNCE_BOTTOM = "bottom"

    def __init__(self):
        super().__init__()
        self.starting_position = None

    def reset_to_starting_position(self):
        self.rect.x = self.starting_position[0]
        self.rect.y = self.starting_position[1]
        self.velocity = [0, 0]

    def set_starting_position(self, start_pos):
        self.starting_position = start_pos
        self.reset_to_starting_position()

    def _check_on_boundary(self, x_pos, y_pos):
        if x_pos - 0 <= 0:
            self.rect.x = 1
            return self.BOUNCE_LEFT
        if x_pos + self.SIZE[0] >= 1000:
            self.rect.x = 1000 - self.SIZE[0] - 1
            return self.BOUNCE_RIGHT
        if y_pos - 0 <= 0:
            self.rect.y = 1
            return self.BOUNCE_TOP
        if y_pos + self.SIZE[1] >= 600:
            self.rect.y = 600 - self.SIZE[1] - 1
            return self.BOUNCE_BOTTOM
        return None

    def _calc_bounce_type(self, x_pos, y_pos, other_x_pos, other_y_pos, other_size):
        tolerance = 10
        bounces = [self.BOUNCE_LEFT, self.BOUNCE_RIGHT, self.BOUNCE_TOP, self.BOUNCE_BOTTOM]
        bounce_diffs = [x_pos - (other_x_pos + other_size[0]),
                        (x_pos + self.SIZE[0]) - other_x_pos,
                        y_pos - (other_y_pos + other_size[1]),
                        (y_pos + self.SIZE[1]) - other_y_pos]
        idx = np.argmin(np.abs(bounce_diffs))
        if bounce_diffs[idx] < tolerance:
            return bounces[idx]
        else:
            return None

    def handle_keyboard_input(self, keys):
        pass
