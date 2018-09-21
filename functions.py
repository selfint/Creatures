# functions.py
# Description: functions.
# ---------------------------------------------------------------------------------------

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
            temp = iter(value)
            for x in value.items():
                string += '\n\t' + str(x)
        except TypeError:
            string += str(value)
        string += '\n'

    return string


if __name__ == '__main__':
    a = {'a': 1, 'b': 2, 'c': [1, 2]}
    print_dict(a)
    print(dict_string(a))