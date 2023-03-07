"""
A non-empty array A consisting of N integers is given.

A triplet (X, Y, Z), such that 0 ≤ X < Y < Z < N, is called a double slice.

The sum of double slice (X, Y, Z) is the total of
A[X + 1] + A[X + 2] + ... + A[Y − 1] + A[Y + 1] + A[Y + 2] + ... + A[Z − 1].

For example, array A such that:
    A[0] = 3
    A[1] = 2
    A[2] = 6
    A[3] = -1
    A[4] = 4
    A[5] = 5
    A[6] = -1
    A[7] = 2

contains the following example double slices:

        double slice (0, 3, 6), sum is 2 + 6 + 4 + 5 = 17,
        double slice (0, 3, 7), sum is 2 + 6 + 4 + 5 − 1 = 16,
        double slice (3, 4, 5), sum is 0.

The goal is to find the maximal sum of any double slice.

Write a function:

    def solution(A)

that, given a non-empty array A consisting of N integers, returns the
maximal sum of any double slice.

For example, given:
    A[0] = 3
    A[1] = 2
    A[2] = 6
    A[3] = -1
    A[4] = 4
    A[5] = 5
    A[6] = -1
    A[7] = 2

the function should return 17, because no double slice of array A has a sum of greater than 17.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [3..100,000];
        each element of array A is an integer within the range [−10,000..10,000].

Copyright 2009–2023 by Codility Limited. All Rights Reserved. Unauthorized
copying, publication or disclosure prohibited.
"""
import threading
from collections import defaultdict

def get_sum_other(array_):
    """ 
    REF: https://curt-park.github.io/2018-09-13/algorithm-max-slice-sum/
    """
    if len(array_) == 0:
        return 0

    max_sum = sub_sum = array_[0]
    for i in range(1, len(array_)):
        sub_sum = max(sub_sum + array_[i], array_[i])
        max_sum = max(max_sum, sub_sum)

    return max_sum

def solution_v1(array_):
    # Task Score 46% Correctness 100% Performance 0%
    max_ = 0
    for j, value in enumerate(array_[1:-1], start=1):
        #print(f'x=0, y=j: {j}, z: {len(array_)}, array_[{j}]: {array_[j]}')
        left = array_[1:j][::-1]
        #print(f'left: {left}, left length: {len(left)}')
        left_sum = get_sum_other(left)
        #print(f'left_sum: {left_sum}')
        right = array_[j+1:-1]
        #print(f'right: {right}, right length: {len(right)}')
        right_sum = get_sum_other(right)
        #print(f'right_sum: {right_sum}')
        max_ = max(max_, left_sum + right_sum)

    return max_

def get_sum_mine(array_):
    if len(array_) == 0:
        return 0

    if max(array_) < 0:
        # array_ll negative
        return 0
    if min(array_) > 0:
        # array_ll positive
        return sum(array_)
    if len(array_) == 1:
        # array_[0] is positive
        return array_[0]

    sum_ = 0
    max_ = 0
    for _ in array_:
        sum_ += _
        max_ = max(max_, sum_)

    return max_


def get_sum_thread_left(array_:list, result:dict, index:int, key:str):
    if index not in result.keys():
        result[index] = {}
    if len(array_) == 0:
        result[index][key] = 0
    else:
        result[index][key] = get_sum_mine(array_)


def get_sum_thread_right(array_:list, result:dict, index:int, key:str):
    if index not in result.keys():
        result[index] = {}
    if len(array_) == 0:
        result[index][key] = 0
    else:
        result[index][key] = get_sum_mine(array_)


def solution(array_):
    # Task Score 61% Correctness 100% Performance 28%
    #
    # medium_range -1000, ..., 1000
    #   TIMEOUT ERROR running time: 0.512 sec., time limit: 0.100 sec.
    # large_ones random numbers from -1 to 1, length = ~100,000
    #   TIMEOUT ERROR Killed. Hard limit reached: 6.000 sec.
    # large_random random, length = ~100,000
    #   TIMEOUT ERROR Killed. Hard limit reached: 6.000 sec.
    # extreme_maximal all maximal values, length = ~100,000
    #   TIMEOUT ERROR running time: 3.560 sec., time limit: 0.704 sec. // slightly better than no thread
    # large_sequence many the same small sequences, length = ~100,000
    #   TIMEOUT ERROR Killed. Hard limit reached: 6.000 sec.

    result = defaultdict(dict)
    max_ = 0
    for j in range(1, len(array_[1:])):
        left = array_[1:j][::-1]
        right = array_[j+1:-1]
        l_thread = threading.Thread(target=get_sum_thread_left, args=(left, result, j, 'left'))
        l_thread.start()
        l_thread.join()

        r_thread = threading.Thread(target=get_sum_thread_right, args=(right, result, j, 'right'))
        r_thread.start()
        r_thread.join()

        max_ = max(max_, result[j]['left'] + result[j]['right'])

    return max_


if __name__ == '__main__':
    arr = [-3,-2,-6,-1,4,5,-1,2]
    #arr = [199,2,6,-1,4,5,1,99]
    arr = [3,-2,6,-1,-4,-1,5,-1,2]
#    arr = [3,2,6,-1,-4,-1,5,-1,2]
    arr = [3,2,6,-1,4,5,-1,2]
    print(arr)
    answer = solution(arr)
    print(f'answer: {answer}')
