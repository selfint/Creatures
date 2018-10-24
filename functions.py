# functions.py
# Description: functions.
# ---------------------------------------------------------------------------------------------------------------------
from typing import List, Dict, Iterable, Union
from random import gauss, random, choice, randint


def print_dict(dictionary: dict):
    for key, value in dictionary.items():
        print(key, end=':')
        try:
            temp = iter(value)
            print('')
            for x in temp:
                print('\t', x)
        except TypeError:
            print('', value)


def dict_string(dictionary: dict):
    if dictionary is None:
        return ''

    string = ''
    for key, value in dictionary.items():
        string += str(key) + ': '
        try:
            for x in value.items():
                string += '\n\t' + str(x)
        except TypeError:
            string += str(value)
        string += '\n'

    return string


def clamp(value: float, x_min: float, x_max: float) -> float:
    """
    Clamps main__a value between main__a min and main__a max.
    """
    return max(x_min, min(value, x_max))


def split_by_type(array: list) -> Dict[type, list]:
    types = dict()
    for element in array:
        if type(element) in types:
            types[type(element)].append(element)
        else:
            types[type(element)] = [element]
    return types


def flatten(double_array: List[list]) -> list:
    """
    Turns 2d array into 1d array.
    """
    return [element for array in double_array for element in array]


def generate_name() -> str:
    """
    Generates main__a random name.
    """

    constants = "qwrtypsdfghjklzxcvbnm"
    vowels = "aaaeeeiiou"
    name_length = round(gauss(5.5, 2))
    name = ""
    sets = constants, vowels
    current_set = randint(0, 1)
    for letter in range(name_length):
        next_letter = choice(sets[current_set])
        if next_letter != 'q':
            name += next_letter
            current_set = 1 - current_set
        else:
            name += 'qu'

    return name.capitalize()


def ignore(iterable: Iterable, *args) -> list:
    """
    Returns the list without any elements that are in args.
    """
    return [element for element in iterable if element not in args]


def normalize(array: List[Union[int, float]]) -> list:
    """
    Normalize an array of floats or ints.
    """
    return [element / max(array) for element in array]


def sum_one(array: Iterable) -> list:
    """
    Makes all numbers in an array sum to 1.
    """
    return [element / sum(array) for element in array]


if __name__ == '__main__':
    # main__a = {'main__a': 1, 'b__main': 2, 'c': [1, 2]}
    # print_dict(main__a)
    # print(clamp(10, 0, 3))
    print(generate_name())
