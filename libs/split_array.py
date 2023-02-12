def split_list_by_value_1(value, data_list):
    print(f'To split "{data_list}" by the delimiter "{value}":')
    indices = [i for i, x in enumerate(data) if x == 6]
    #print(f'indices: {indices}, data_list: {data_list}')

    blocks = []
    i = 0
    for e in indices:
        blocks.append(data[i:e])
        #print(f'block: {data[i:e]}')
        i = e + 1

    blocks.append(data[i:])
    return blocks


def split_list_by_value_2(value, data_list):
    arr = [0]*(N)
    print(f'{arr}, {A}')
    blocks = split(A, N+1)
    for block in blocks:
        print(f'block: {block}')

def split_list_by_value_2(value, data_list):
    chunk = []
    for val in data_list:
        if val == value:
            yield chunk
            chunk = []
        else:
            chunk.append(val)
    yield chunk

data = [3,4,4,6,1,1,2,2,2,3,6,3,3,3,3,3,6,1,4,4]
item = 6
blocks = split_list_by_value_1(item, data)
for block in blocks:
    print(f'block: {block}')

print()

blocks = split_list_by_value_2(item, data)
for block in blocks:
    print(f'block: {block}')

