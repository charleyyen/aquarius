import numpy as np
import random
import string

def create_random_number_array_withiout_same_neibour(
        low:int=1,
        high:int=1000000,
        size:int=10000000,
        dimension:int=0,
        float_:bool=False,
        ) -> dict:
    data = create_random_number_array(
        low=low,
        high=high,
        size=size,
        dimension=dimension,
        float_=float_
    )
    """
    e.g.
    Original: [-5, -3,  4,  4,  0,  1, 1, 3,  3, 1, -4, -5]
         New: [-5, -3, 4, 0, 1, 3, 1, -4, -5]
    """
    array_ = []
    array_.append(data['list_'][0])
    for i, e in enumerate(data['list_'][1:], start=1):
        if e == data['list_'][i-1]:
            continue
        array_.append(e)

    return array_


def create_random_number_array(
        low:int=1,
        high:int=1000000,
        size:int=10000000,
        dimension:int=0,
        float_:bool=False,
        ) -> dict:
    """
    Generate a NumPy array with random numbers.
    If float_ is True,  each element range is: low <= element's value <  high
    If float_ is False, each element range is: low <= element's value <= high
    """
    data = {}
    if float_:
        if dimension:
            array_ = np.random.uniform(low=low, high=high, size=(size, dimension))
        else:
            array_ = np.random.uniform(low=low, high=high, size=size)
    else:
        if dimension:
            array_ = np.random.randint(low=low, high=high+1, size=(size, dimension))
        else:
            array_ = np.random.randint(low=low, high=high+1, size=size)

    data['array_'] = array_
    data['list_'] = array_.tolist()
    data['set_'] = set(array_.flatten())
    data['sorted_'] = sorted(array_)
    data['sorted_unique'] = sorted(list(set(array_.flatten())))
    return data

def create_random_alphabet_string(
        letters_used:str=string.ascii_uppercase + string.ascii_lowercase,
        size:int=1000000
        ) -> dict:
    """
    Create a random string with a length == size. By default, this string contains
    all 52 letters (upper and lower cases).
    """
    data = {}
    random_string = ""
    i = 0
    while len(random_string) < size:
        random_string += letters_used[(random.randint(0, len(letters_used)-1))]

    data['string_'] = random_string
    data['sorted_'] = ''.join(sorted(random_string))
    data['sorted_lower_'] = ''.join(sorted(random_string.lower()))
    data['sorted_upper_'] = ''.join(sorted(random_string.upper()))
    data['unique'] = ''.join(list(set(random_string)))
    data['sorted_unique'] = ''.join(sorted(list(set(random_string))))
    data['sorted_unique_lower_'] = ''.join(sorted(list(set(random_string.lower()))))
    data['sorted_unique_upper_'] = ''.join(sorted(list(set(random_string.upper()))))
    return data

def display(data):
    for key, value in data.items():
        print(f'{key} -> {value}')

if __name__ == '__main__':
    #data = create_random_number_array(low=-5, high=5, size=10)
    #display(data)
    #data = create_random_alphabet_string(size=20)
    #display(data)
    #data = create_random_number_array_withiout_same_neibour(low=-5, high=5, size=10)
    data = create_random_number_array_withiout_same_neibour()
#    display(data)

"""
TODO List:
1) A float array:
REF: https://stackoverflow.com/questions/29060824/is-there-a-way-to-define-a-float-array-in-python
>>> np.tile(0, 10).dtype
dtype('int64')
>>> np.tile(0.0, 10).dtype
dtype('float64')
>>> np.zeros(10)
array([ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.])
>>> np.zeros(10).dtype
dtype('float64')
"""
