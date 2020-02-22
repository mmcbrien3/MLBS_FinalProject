import pygame as pg

class Paddle(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pg.Surface([10, 30])
        self.rect = self.image.get_rect()

    def update(self):
        pass