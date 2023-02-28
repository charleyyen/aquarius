"""
You are going to build a stone wall. The wall should be straight and N
meters long, and its thickness should be constant; however, it should
have different heights in different places. The height of the wall is
specified by an array H of N positive integers. H[I] is the height of
the wall from I to I+1 meters to the right of its left end. In particular,
H[0] is the height of the wall's left end and H[N−1] is the height of
the wall's right end.

The wall should be built of cuboid stone blocks (that is, all sides of
such blocks are rectangular). Your task is to compute the minimum number
of blocks needed to build the wall.

Write a function:

    def solution(H)

that, given an array H of N positive integers specifying the height of
the wall, returns the minimum number of blocks needed to build it.

For example, given array H containing N = 9 integers:
  H[0] = 8    H[1] = 8    H[2] = 5
  H[3] = 7    H[4] = 9    H[5] = 8
  H[6] = 7    H[7] = 4    H[8] = 8

the function should return 7. The figure shows one possible arrangement
of seven blocks.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [1..100,000];
        each element of array H is an integer within the range [1..1,000,000,000].

Copyright 2009–2023 by Codility Limited. All Rights Reserved. Unauthorized
copying, publication or disclosure prohibited.
"""
from aquarius.libs import data_generator

def solution_1(H):
    # Task Score 85% Correctness 100% Performance 77%
    # large_piramid TIMEOUT ERROR
    # Killed. Hard limit reached: 6.000 sec.
    # large_increasing_decreasing
    # TIMEOUT ERROR Killed. Hard limit reached: 6.000 sec.
    brick_used = set()
    brick_used.add(min(H))
    brick_count = 1
    for i, brick in enumerate(H):
        if brick not in brick_used:
            brick_used.add(brick)
            brick_count += 1

        for x in brick_used.copy():
            if x > brick:
                # We use a set here so we can call discard() w/o worrying performance
                brick_used.discard(x)

    return brick_count


def solution_2(H):
    # Score 64
    brick_used = set()
    brick_used.add(min(H))
    brick_count = 1
    for i, brick in enumerate(H):
        if brick not in brick_used:
            brick_used.add(brick)
            brick_count += 1

        if i>0 and i+1 < len(H) and H[i] < H[i-1] and H[i] < H[i+1]:
            # With this if, correctness decreased remendously
            for x in brick_used.copy():
                if x > brick:
                    brick_used.discard(x)

    return brick_count


def solution_3(H):
    # Task Score 92% Correctness 100% Performance 88%
    # large_piramid TIMEOUT ERROR
    # running time: 5.492 sec., time limit: 0.352 sec.
    brick_used = [] # use a list instead of a set here
    brick_used.append(min(H))
    brick_count = 1
    for brick in H:
        if brick > brick_used[-1]:
            # To make sure brick_used is sorted
            brick_used.append(brick)
            brick_count += 1
        elif brick < brick_used[-1]:
            for x in brick_used[::-1]:
                if x > brick:
                    # use pop(), because brick_used is sorted
                    brick_used.pop()
                else:
                    break
            if brick > brick_used[-1]:
                # To make sure brick_used is sorted
                brick_used.append(brick)
                brick_count += 1

    return brick_count


def solution_4(H):
    # Score 100% 
    brick_used = []
    brick_used.append(min(H))
    brick_count = 1
    for brick in H:
        if brick > brick_used[-1]:
            brick_used.append(brick)
            brick_count += 1
        elif brick < brick_used[-1]:
            while brick < brick_used[-1]:
                # While loop is fast than for loop
                brick_used.pop()
            if brick > brick_used[-1]:
                brick_used.append(brick)
                brick_count += 1

    return brick_count

if __name__ == '__main__':
    import time
    size = 100
    high = 50
    data_hash = data_generator.create_random_number_array(size=size, high=high)
    print(f"data_hash['array_'] length: {len(data_hash['array_'])}, max: {max(data_hash['array_'])}")
    for solution in [solution_1, solution_3, solution_4]:
        start = time.time()
        answer = solution(data_hash['array_'])
        print(f'answer: {answer}, time: {round((time.time() - start), 3)}')

#    H = [1,2,3,7,9,8,3,2,9]
#    print(solution(H))
#    H = [1,2,3,4,5,1,2,3,4,5,1,2,3,4,5]
#    print(solution(H))
#    H = [1,2,3,4,5,4,3,2,1,2,3,4,5,4,3,2,1,2,3,4,5,4,3,2,1]
#    print(solution(H))

