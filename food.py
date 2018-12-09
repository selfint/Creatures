# food.py
# Description: food object for simulation.
# ---------------------------------------------------------------------------------------

# Imports
from Constants.constants import FOOD_BODY


# Constants


class Food:

    def __init__(self, x, y, amount):
        self.x = x
        self.y = y
        self.amount = amount

        # Graphics.
        self.body = FOOD_BODY


if __name__ == '__main__':
    f = Food(100, 100, 1)
