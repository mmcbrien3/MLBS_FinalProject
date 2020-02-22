import pygame as pg
import asset_getter

class Ball(pg.sprite.Sprite):

    SIZE = (30, 30)
    def __init__(self):
        super().__init__()
        self.image = pg.transform.scale(pg.image.load(asset_getter.get_asset("munns.png")), self.SIZE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

    def update(self):
        pass

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y