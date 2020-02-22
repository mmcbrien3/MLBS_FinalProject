import pygame as pg


class Controller(object):

    BACKGROUND_COLOR = (0, 0, 0)
    CAPTION = "PING"

    def __init__(self, dimensions=[1000, 600]):
        self.clock = pg.time.Clock()
        self.objects_to_render = []
        self.window = None
        self.dimensions = dimensions
        self.quit_game_flag = False

    def add_objects_to_render(self, *objects: pg.sprite.Sprite):
        self.objects_to_render.extend(objects)

    def _should_game_continue(self):
        return not self.quit_game_flag

    @staticmethod
    def _check_for_window_close(event):
        return event.type == pg.QUIT

    def _do_updates(self):
        [o.update() for o in self.objects_to_render]
        pg.display.update()

    def _create_window(self):
        self.window = pg.display.set_mode((self.dimensions[0], self.dimensions[1]))
        pg.display.set_caption(self.CAPTION)
        pg.display.update()

    def start_game(self):
        pg.init()

        self._create_window()

        while self._should_game_continue():

            for event in pg.event.get():
                if self._check_for_window_close(event):
                    self.quit_game_flag = True
                    break

            self.window.fill(self.BACKGROUND_COLOR)

            self._do_updates()

        pg.quit()

