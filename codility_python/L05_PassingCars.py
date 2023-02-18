"""
# Passing Cars

Count the number of passing cars on the road.

A non-empty array A consisting of N integers is given.
The consecutive elements of array A represent consecutive cars on a road.

Array A contains only 0s and/or 1s:

        0 represents a car traveling east,
        1 represents a car traveling west.

The goal is to count passing cars. We say that a pair of cars (P, Q),
where 0 ≤ P < Q < N, is passing when P is traveling to the east
and Q is traveling to the west.

For example, consider array A such that:
  A[0] = 0
  A[1] = 1
  A[2] = 0
  A[3] = 1
  A[4] = 1

We have five pairs of passing cars: (0, 1), (0, 3), (0, 4), (2, 3), (2, 4).

Write a function:

    def solution(A)

that, given a non-empty array A of N integers, returns the number of pairs of passing cars.

The function should return -1 if the number of pairs of passing cars exceeds 1,000,000,000.

For example, given:
  A[0] = 0
  A[1] = 1
  A[2] = 0
  A[3] = 1
  A[4] = 1

the function should return 5, as explained above.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [1..100,000];
        each element of array A is an integer that can have one of the following values: 0, 1.

Copyright 2009–2022 by Codility Limited. All Rights Reserved.
Unauthorized copying, publication or disclosure prohibited.
"""
import time
from aquarius.libs import data_generator

MAX_PAIRS = int(1e9)
def solution_1(A):
    # Task Score 50% Correctness 100% Performance 0%
    pairs = 0
    for i, e in enumerate(A):
        if e < 1:
            pairs += A[i:].count(1)
    return -1 if pairs > MAX_PAIRS else pairs

def solution_2(A):
    # Scored 100%
    pairs = 0
    zero_count = 0
    for e in A:
        if e < 1:
            zero_count += 1
        else:
            pairs += zero_count

    return -1 if pairs > MAX_PAIRS else pairs


def main():
    print()
    # N is an integer within the range [1..100,000];
    # each element of array A is an integer that can have one of the following values: 0, 1.
    N = 10000
    data_hash = data_generator.create_random_number_array(low=0,high=1, size=N)
    data = data_hash['array_'].tolist()
    #if len(data) < 21:
    #    print(f'{data}')
    #else:
    #    print(f'Length: {len(data)}')
    #    print(f'First 10: {data[:10]}')
    #    print(f' Last 10: {data[-10:]}')
    solution = solution_1
    start = time.time()
    result_1 = solution(data)
    print(f'Result solution_1(): {result_1}')
    print(f'solution_1() [Score:  50] time consumed: {round(time.time() - start, 3)}')

    solution = solution_2
    start = time.time()
    result_2 = solution(data)
    print(f'Result solution_2(): {result_2}')
    print(f'solution_2() [Score: 100] time consumed: {round(time.time() - start, 3)}')
    assert result_1 == result_2
    print()

    # When N = 100,000
    # solution_1() [Score:  50] time consumed: 41.146
    # solution_2() [Score: 100] time consumed:  0.007


if __name__ == "__main__":
    #arr = [0,1,0,1,1]
    #print(solution_1(arr))
    #print(solution_2(arr))

    main()
