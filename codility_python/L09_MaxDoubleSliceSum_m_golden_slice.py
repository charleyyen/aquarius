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
def get_sum(array_):
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
    for value in array_:
        sum_ += value
        max_ = max(max_, sum_)

    return max_


def solution_mine_01(array_):
    # Task Score 61% Correctness 100% Performance 28%
    # medium_range -1000, ..., 1000                                                                                                         
    # TIMEOUT ERROR running time: 0.624 sec., time limit: 0.100 sec.
    # large_ones random numbers from -1 to 1, length = ~100,000
    # TIMEOUT ERROR Killed. Hard limit reached: 6.000 sec.
    # large_random random, length = ~100,000
    # TIMEOUT ERROR Killed. Hard limit reached: 6.000 sec.
    # extreme_maximal all maximal values, length = ~100,000
    # TIMEOUT ERROR Killed. Hard limit reached: 6.000 sec.
    # large_sequence many the same small sequences, length = ~100,000
    # TIMEOUT ERROR Killed. Hard limit reached: 6.000 sec.
    
    max_ = 0
    for j in range(1, len(array_[1:])):
        left = array_[1:j][::-1]
        left_sum = get_sum(left)
        right = array_[j+1:-1]
        right_sum = get_sum(right)
        max_ = max(max_, left_sum + right_sum)

    return max_

def solution_mine_02(array_):
    # Score 100%

    #--------------------------------------------------
    # Declare the following two lists: left and right,
    # which are used to hold the max value. This method
    # is similar to L04_MaxCounters_m.py
    left, right = [0]*len(array_), [0]*len(array_)
    left_sum = 0
    for i, value in enumerate(array_[1:], start=1):
        left_sum = max(value, left_sum + value)
        left[i] = max(value, left_sum, 0)

    # Save this portion
    #n = len(array_)
    #for i in range(n - 2, 1, -1):
    #    right[i] = max(0, right[i + 1] + array_[i])
    #    print(f'A: i: {i}, right[{i}]: {right[i]}, array_[{i}]: {array_[i]}')
    # Save this portion

    right_sum_ = 0
    for i, value in enumerate(array_[2:-1][::-1], start=1):
        j = len(array_) - i - 1
        right_sum_ = max(value, right_sum_ + value)
        right[j] = max(value, right_sum_, 0)

    max_ = 0
    for i in range(1, len(array_[:-1])):
        max_ = max(max_, left[i-1] + right[i+1])
    return max_

def solution_other_03(A):
    L_slice, until_now, once_total = 0, 0, 0
    for Z in range(3, len(A)):
        L_slice = max(0, A[Z-2] + L_slice)
        until_now = max(L_slice, A[Z-1] + until_now)
        once_total = max(until_now, once_total)
    return once_total


import sys
def solution_other_04(A):
    n = len(A)
    left = [0] * n
    for i in range(1, n - 1):
        left[i] = max(0, left[i - 1] + A[i])

    right = [0] * n
    for i in range(n - 2, 1, -1):
        right[i] = max(0, right[i + 1] + A[i])

    max_sum = -sys.maxsize
    for i in range(1, n - 1):
        max_sum = max(max_sum, left[i - 1] + right[i + 1])
    return max_sum

if __name__ == '__main__':
    arr = [3,2,6,-1,4,5,-1,2]
    print(f'Sample array: {arr}')
    answer = solution_mine_02(arr)
    print(f'answer (sample array): {answer}\n')

    #N is an integer within the range [3..100,000];
    #each element of array A is an integer within the range [−10,000..10,000].
    size = 1000
    high = 1000
    low = (-1)*high
    solution_list = [
            solution_mine_01,
            solution_mine_02,
            solution_other_03,
            solution_other_04,
            ]

    import my_test # in house
    import time
    from aquarius.libs import data_generator

    data_hash = data_generator.create_random_number_array(low=low, high=high, size=size)
    arr = data_hash['list_']
    #arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f'Array length in test: {len(arr):,}')
    summary = []
    for j, solution in enumerate(solution_list, start=1):
        method = str(solution).split()[1]
        start = time.time()
        answer = solution(arr)
        elapsed = round(time.time() - start, 4)
        #print(f'{method}, {answer:,}, {elapsed}')
        summary.append((method, answer, elapsed))
    my_test.display_summary(summary)

"""
Sample array: [3, 2, 6, -1, 4, 5, -1, 2]
answer (sample array): 17

Array length in test: 10,000
1,  solution_mine_01 - 102,969: Time Consumed: 22.2194
2,  solution_mine_02 - 102,969: Time Consumed: 0.0141
3, solution_other_03 - 102,969: Time Consumed: 0.0065
4, solution_other_04 - 102,969: Time Consumed: 0.0091

Array length in test: 1,000
1,  solution_mine_01 - 38,126: Time Consumed: 0.2264
2,  solution_mine_02 - 38,126: Time Consumed: 0.0014
3, solution_other_03 - 38,126: Time Consumed: 0.0006
4, solution_other_04 - 38,126: Time Consumed: 0.0009
"""
