

class Score_Keeper(object):

    def __init__(self):
        self.goal_locations = []
        self.ball = None
        self.scores = [0, 0]
        self.max_score = 5

    def check_for_goal(self):
        ball_scores_on_left = self.ball.rect.x <= 0
        ball_scores_on_right = self.ball.rect.x + self.ball.SIZE[0] >= 1000
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