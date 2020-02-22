from controller import Controller
from paddle import Paddle
from ball import Ball

if __name__ == "__main__":
    paddleOne = Paddle()
    ball = Ball()
    controller = Controller()
    controller.add_objects_to_render(paddleOne, ball)
    controller.start_game()