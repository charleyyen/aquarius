import random
import time
from array import *

def split_list_by_value_1(value, data_list, more_or_less=0):
    if more_or_less < 0:
        indices = [i for i, x in enumerate(data_list) if x <= value]
    elif more_or_less > 0:
        indices = [i for i, x in enumerate(data_list) if x >= value]
    else: # more_or_less == 0:
        indices = [i for i, x in enumerate(data_list) if x == value]

    blocks = []
    i = 0
    for e in indices:
        blocks.append(data_list[i:e])
        i = e + 1

    blocks.append(data_list[i:])
    return blocks, indices


def split_list_by_value_2(value, data_list, more_or_less=0):
    chunk = []
    for val in data_list:
        if more_or_less < 0:
            if val <= value:
                yield chunk
                chunk = []
            else:
                chunk.append(val)
        elif more_or_less > 0:
            if val >= value:
                yield chunk
                chunk = []
            else:
                chunk.append(val)
        else: # more_or_less == 0
            if val == value:
                yield chunk
                chunk = []
            else:
                chunk.append(val)
    yield chunk

def create_random_array(
        low:int=1,
        high:int=1000000,
        sort:bool=False,
        unique:bool=False,
        size:int=10000000) -> array:

    arr = array('i', [])
    while len(arr) < size:
        arr.append(random.randint(low, high))

    if unique:
        arr = set(arr)

    if sort:
        arr = sorted(list(arr))

    return arr


if __name__ == '__main__':
    #data = create_random_array(high=15, size=30)
    data = create_random_array()
    sorted_unique = sorted(list(set(data)))
    #print(f'data length: {len(data)}, sorted_unique length: {len(sorted_unique)}')

    separator_index = random.randint(0, len(data))
    #print(f'separator_index: {separator_index}')
    assert data[separator_index] in data

    separator = data[separator_index]
    separator_count = data.count(separator)
    #print(f'separator: {separator}, separator_count: {separator_count}')

    start = time.time()
    blocks1, indices = split_list_by_value_1(separator, data)
    print(f'   split_list_by_value_1(): Total run time: {round((time.time() - start), 3)}')
    #print(f'blocks1 type: {type(blocks1)}')
    #print(f'blocks1 length: {len(blocks1,)}, indices length: {len(indices)}, {indices}')
    assert separator_count == len(indices)

    start = time.time()
    results = split_list_by_value_2(separator, data) # Very efficient
    print(f'A. split_list_by_value_2(): Total run time: {round((time.time() - start), 3)}')
    blocks2 = []
    #for element in split_list_by_value_2(separator, data):
    for element in results:
        # Time consuming
        blocks2.append(element)
    print(f'B. split_list_by_value_2(): Total run time: {round((time.time() - start), 3)}')
    #print(f'blocks2 type: {type(blocks2)}')
    #print(f'blocks2 length: {len(blocks2)}')

    #print()
    #print(f'blocks1: {list(blocks1)}')
    #print(f'blocks2: {blocks2}')

    assert len(blocks2) == len(blocks1)
    #assert list(blocks1) == blocks2
