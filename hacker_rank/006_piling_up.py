"""
https://www.hackerrank.com/challenges/piling-up/problem?isFullScreen=true
"""

def verify_inputs(size, blocks_as_string):
    temp = blocks_as_string.strip().split(' ')
    if len(temp) != size:
        return None

    blocks = []
    for x in temp:
        if not x.isdigit():
            return None
        blocks.append(int(x))

    return blocks

def get_input():
    t = int(input())
    #print(f't: {t}')
    for i in range(t):
        size = int(input())
        blocks_as_string = input()
        blocks_as_list = verify_inputs(size, blocks_as_string)
        if blocks_as_list:
            #print(f'size: {size}\n{blocks_as_list}')
            can_pile_up(blocks_as_list)

def can_pile_up(blocks):
    #print(f'blocks: {blocks}')
    min_ = min(blocks)
    i = blocks.index(min_)
    if i == 0:
        #print(f'sorted: {sorted(blocks)}')
        if blocks == sorted(blocks):
            print('Yes')
        else:
            print('No')
    elif i == len(blocks) - 1:
        #print(f'i: {i}, min_: {min_}')
        #print(f'reverse sorted: {sorted(blocks, reverse=True)}')
        if blocks == sorted(blocks, reverse=True):
            print('Yes')
        else:
            print('No')
    else:
        left = blocks[:i]
        right = blocks[i:]
        #print(f'left: {left}, right: {right}')
        if left == sorted(left, reverse=True) and right == sorted(right):
            print('Yes')
        else:
            print('No')


def main():
    get_input() # When test local, comment out this line

    b1 = [4, 3, 2, 1, 3, 4]
    b2 = [1, 3, 2]
    b3 = [1, 2, 3, 1, 2, 3]
    b4 = [2, 3, 4, 2, 3, 1]
    for b in (
            b1,
            b2,
            #b3,
            #b4
        ):
        can_pile_up(b)


if __name__ == '__main__':
    """
    https://www.hackerrank.com/challenges/piling-up/problem?isFullScreen=true
    Sample Input
    STDIN        Function
    -----        --------
    2            T = 2
    6            blocks[] size n = 6
    4 3 2 1 3 4  blocks = [4, 3, 2, 1, 3, 4]
    3            blocks[] size n = 3
    1 3 2        blocks = [1, 3, 2]

    Sample Output
    Yes
    No
    """
    main()
