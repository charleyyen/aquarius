"""
An integer N is given, representing the area of some rectangle.

The area of a rectangle whose sides are of length A and B is A * B,
and the perimeter is 2 * (A + B).

The goal is to find the minimal perimeter of any rectangle whose area
equals N. The sides of this rectangle should be only integers.

For example, given integer N = 30, rectangles of area 30 are:

        (1, 30), with a perimeter of 62,
        (2, 15), with a perimeter of 34,
        (3, 10), with a perimeter of 26,
        (5, 6), with a perimeter of 22.

Write a function:

    def solution(N)

that, given an integer N, returns the minimal perimeter of any rectangle
whose area is exactly equal to N.

For example, given an integer N = 30, the function should return 22, as explained above.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [1..1,000,000,000].

Copyright 2009–2023 by Codility Limited. All Rights Reserved. Unauthorized
copying, publication or disclosure prohibited. 
"""

import math

def solution_1(area):
    width = int(math.sqrt(area))
    i, j = width, width
    while area%i != 0 and area%j != 0:
        i += 1
        j -= 1

    width = i if area%i == 0 else j
    return 2*(width + int(area/width))


def solution_2(N):
    # https://codesays.com/2014/solution-to-min-perimeter-rectangle-by-codility/.
    for i in range(int(math.sqrt(N)), 0, -1):
        if N % i == 0:
            return (int(N / i) + i) * 2

if __name__ == '__main__':
    # N is an integer within the range [1..1,000,000,000].
    solution_list = [
            solution_1,
            solution_2,
            ]
    import my_test # in house
    import random
    import time

    low = 100_000_000
    high = low * 10
    random_number = random.randint(low, high)
    print(f'random_number: {random_number:,}')
    summary = []
    for j, solution in enumerate(solution_list, start=1):
        method = str(solution).split()[1]
        start = time.time()
        answer = solution(random_number)
        elapsed = round(time.time() - start, 4)
        #print(method, answer, elapsed)
        summary.append((method, answer, elapsed))
    my_test.display_summary(summary)

