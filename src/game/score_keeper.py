import pygame as pg

class Score_Keeper(object):

    GOAL_COLOR = (100, 100, 100)
    GOAL_DRAW_WIDTH = 15

    def __init__(self):
        self.goal_locations = []
        self.ball = None
        self.scores = [0, 0]
        self.max_score = 5
        self.goal_center = 300
        self.goal_size = 300

    def check_for_goal(self):
        ball_scores_on_left = self.ball.rect.x <= 0 and \
                              (self.goal_center - self.goal_size // 2 <=
                               self.ball.rect.y <=
                               self.goal_center + self.goal_size // 2)
        ball_scores_on_right = self.ball.rect.x + self.ball.SIZE[0] >= 1000 and \
                               (self.goal_center - self.goal_size // 2 <=
                                self.ball.rect.y <=
                                self.goal_center + self.goal_size // 2)
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