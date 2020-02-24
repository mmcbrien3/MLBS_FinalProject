import pygame as pg
import numpy as np
class ScoreKeeper(object):

    GOAL_COLOR = (100, 100, 100)
    GOAL_DRAW_WIDTH = 15
    LEFT_WINNER_DECLARATION = "LEFT"
    RIGHT_WINNER_DECLARATION = "RIGHT"

    def __init__(self):
        pg.font.init()
        self.score_font = pg.font.Font(pg.font.get_default_font(), 18)
        self.goal_locations = []
        self.ball = None
        self.scores = [0, 0]
        self.max_score = 2
        self.goal_center = 300
        self.goal_size = 300

    def get_winner(self):
        if self.scores[0] > self.scores[1]:
            return self.LEFT_WINNER_DECLARATION
        elif self.scores[0] < self.scores[1]:
            return self.RIGHT_WINNER_DECLARATION
        else:
            return None

    def is_max_score_reached(self):
        return np.max(self.scores) >= self.max_score

    def check_for_goal(self):
        ball_within_y_bounds = (self.goal_center - self.goal_size // 2 <=
                               self.ball.rect.y <=
                               self.goal_center + self.goal_size // 2 - self.ball.SIZE[1])

        ball_scores_on_left = self.ball.rect.x <= 0 and ball_within_y_bounds
        ball_scores_on_right = self.ball.rect.x + self.ball.SIZE[0] >= 1000 and ball_within_y_bounds
        scored = False

        if ball_scores_on_left:
            self.scores[1] += 1
            scored = True
            print(self.scores)
        elif ball_scores_on_right:
            self.scores[0] += 1
            scored = True
            print(self.scores)

        return scored

    def draw(self, window):
        top_left = (0, self.goal_center - self.goal_size // 2)
        window.fill(self.GOAL_COLOR, pg.Rect(top_left, (self.GOAL_DRAW_WIDTH, self.goal_size)))
        top_left = (1000 - self.GOAL_DRAW_WIDTH, self.goal_center - self.goal_size // 2)
        window.fill(self.GOAL_COLOR, pg.Rect(top_left, (self.GOAL_DRAW_WIDTH, self.goal_size)))

        text_surface = self.score_font.render(str(self.scores[0]), True, (255, 255, 255))
        window.blit(text_surface, dest=(5, 5))

        text_surface = self.score_font.render(str(self.scores[1]), True, (255, 255, 255))
        window.blit(text_surface, dest=(1000 - 15, 5))