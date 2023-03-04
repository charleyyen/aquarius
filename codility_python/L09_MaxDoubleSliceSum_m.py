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


def solution(array_):
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

if __name__ == '__main__':
    arr = [-3,-2,-6,-1,4,5,-1,2]
    #arr = [199,2,6,-1,4,5,1,99]
    arr = [3,-2,6,-1,-4,-1,5,-1,2]
#    arr = [3,2,6,-1,-4,-1,5,-1,2]
    arr = [3,2,6,-1,4,5,-1,2]
    print(arr)
    answer = solution(arr)
    print(f'answer: {answer}')
