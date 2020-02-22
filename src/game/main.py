from controller import Controller
from paddle import Paddle

if __name__ == "__main__":
    paddleOne = Paddle()
    controller = Controller()
    controller.add_objects_to_render(paddleOne)
    controller.start_game()