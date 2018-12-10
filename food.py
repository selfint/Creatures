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

    def __str__(self):
        return "{}(x={}, y={}, amount={})".format(self.__class__.__name__, self.x, self.y, self.amount)

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    f = Food(100, 100, 1)
