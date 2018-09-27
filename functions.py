# functions.py
# Description: functions.
# ---------------------------------------------------------------------------------------------------------------------

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
    Clamps a value between a min and a max.
    """
    return max(x_min, min(value, x_max))

if __name__ == '__main__':
    a = {'a': 1, 'b': 2, 'c': [1, 2]}
    print_dict(a)
    print(clamp(10, 0, 3))