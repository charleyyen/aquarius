def split_list_by_value_1(value, data_list):
    indices = [i for i, x in enumerate(data_list) if x == value]

    blocks = []
    i = 0
    for e in indices:
        blocks.append(data_list[i:e])
        i = e + 1

    blocks.append(data_list[i:])
    return blocks, indices


def split_list_by_value_2(value, data_list):
    chunk = []
    for val in data_list:
        if val == value:
            yield chunk
            chunk = []
        else:
            chunk.append(val)
    yield chunk

if __name__ == '__main__':
    data = [3,4,4,6,1,1,2,2,2,3,6,3,3,3,3,3,6,1,4,4]
    item = 6
    blocks1, indices = split_list_by_value_1(item, data)
    for block in blocks1:
        print(f'1. block: {block}')

    print()

    blocks2 = split_list_by_value_2(item, data)
    for block in blocks2:
        print(f'2. block: {block}')

    #assert blocks1 == blocks2
