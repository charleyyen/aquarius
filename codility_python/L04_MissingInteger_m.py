"""
# Missing Integer
Find the smallest positive integer that does not occur in a given sequence.

Write a function:

    def solution(A)

that, given an array A of N integers, returns the smallest positive integer
(greater than 0) that does not occur in A.

For example, given A = [1, 3, 6, 4, 1, 2], the function should return 5.

Given A = [1, 2, 3], the function should return 4.

Given A = [−1, −3], the function should return 1.

Write an efficient algorithm for the following assumptions:

    N is an integer within the range [1..100,000];
    each element of array A is an integer within the range [−1,000,000..1,000,000].

Copyright 2009–2022 by Codility Limited. All Rights Reserved.
Unauthorized copying, publication or disclosure prohibited.
"""
import random
from parameterized import parameterized

def solution_1_77_100_50(A):
    # Task Score 77% Correctness 100% Performance 50%
    # large_1: chaotic + sequence 1, 2, ..., 40000 (without minus)
    # TIMEOUT ERROR
    # Killed. Hard limit reached: 6.000 sec. 
    #
    # large_3: chaotic + many -1, 1, 2, 3 (with minus)
    # TIMEOUT ERROR
    # running time: 0.760 sec., time limit: 0.272 sec. 
    if 1 not in A:
        return 1

    A.append(0)
    A = sorted(list(set(A)))
    index = A.index(0)
    A = A[index+1:] # all positives
    if len(A) == 0:
        # Original A contains all negative elements
        return 1

    B = list(range(1, A[-1]+1))
    len_A = len(A)
    len_B = len(B)
    if len_A + 1 == len_B:
        return sum(B) - sum(A)
    if len_A == len_B:
        return A[-1]+1

    for i in B:
        if i not in A:
            return i
    return B[-1] + 1


def solution_2_88_100_75(A):
    # Task Score 88% Correctness 100% Performance 75%
    # medium chaotic sequences length=10005 (with minus)
    # TIMEOUT ERROR
    # running time: 0.180 sec., time limit: 0.100 sec. 
    if 1 not in A:
        return 1

    A = sorted(A)
    index = A.index(1)
    A = A[index:] # all positives
    set_a = set(A)
    set_a_len = len(set_a)
    if set_a_len == 1:
        # A has one element - 1 (one)
        return 2

    if set_a_len == A[-1]:
        return A[-1]+1

    set_b = set(list(range(1, A[-1]+1)))
    set_c = set_b.difference(set_a)
    if set_c:
        return sorted(list(set_c))[0]

    return A[-1]+1


def solution(A):
    # Scored 100%
    if 1 not in A:
        return 1

    A = sorted(list(set(A)))
    index = A.index(1)
    A = A[index:] # all positives and sorted array
    if len(A) == 1:
        # A has one element - 1 (one)
        return 2
    if len(A) == A[-1]:
        return A[-1]+1

    return more_search(A)

def more_search(A):
    half_position = len(A)//2
    left = A[:half_position]
    right = A[half_position:]
    if len(left) == left[-1] - left[0] + 1:
        if left[-1] + 1 < right[0]:
            return left[-1] + 1
        return more_search(right)
    return more_search(left)

###########################################
def generate_test_data():
    test_data = [
        ([1, 3, 6, 4, 1, 2], 5),
        ([1, 2, 3], 4),
        ([-1, -3], 1),
        ([-1,-3, 1, 3, 5, 4, 1, 2, 8], 6),
        ([-1,-3, 3, 5, 4, 2, 8], 1),
        ([1], 2),
        ([1,2,3,4,5,6,7,8,9], 10),
        ]

    #N is an integer within the range [1..100,000];
    #each element of array A is an integer within the range [−1,000,000..1,000,000].
    N = 100000
    x = random.randint(1, N)
    arr = list(range(-x, x))
    number_to_be_removed = random.randint(1, len(arr)//2)
    print(f'x: {x}, length: {len(arr)}, number_to_be_removed: {number_to_be_removed}')
    i = 0
    removed_items = []
    while i < number_to_be_removed:
        position = random.randint(2, len(arr)//2 - 1)
        del arr[position]
        removed_items.append(arr[position])
        i += 1

    random.shuffle(arr)
    removed_items.append(0)
    removed_items = sorted(removed_items)
    index = removed_items.index(0)
    a = sorted(list(set(removed_items[index:])))
    minimum = a[1]
    print(f'length: {len(arr)}, {arr[:10]}, {len(removed_items)}')
    print(f'index: {index}, {a[:10]}, minimum: {minimum}')
#    test_data.append((arr, minimum))


    for element in test_data:
        yield element[0], element[1]

@parameterized.expand(generate_test_data())
def test_solution(data, expected):
    """Test solution()"""
    assert solution(data) == expected
