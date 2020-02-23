import pygame as pg

class Base_Object(pg.sprite.Sprite):

    IMAGE_NAME = None
    SIZE = None
    BOUNCE_LEFT = "left"
    BOUNCE_RIGHT = "right"
    BOUNCE_TOP = "top"
    BOUNCE_BOTTOM = "bottom"

    def __init__(self):
        super().__init__()

    def _check_on_boundary(self, x_pos, y_pos):
        if x_pos - 0 <= 0:
            return self.BOUNCE_LEFT
        if x_pos + self.SIZE[0] >= 1000:
            return self.BOUNCE_RIGHT
        if y_pos - 0 <= 0:
            return self.BOUNCE_TOP
        if y_pos + self.SIZE[1] >= 600:
            return self.BOUNCE_BOTTOM
        return None

    def handle_keyboard_input(self, keys):
        pass
