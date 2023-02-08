"""
# PermCheck
Check whether array A is a permutation.

A non-empty array A consisting of N integers is given.

A permutation is a sequence containing each element from 1 to N once, and only once.

For example, array A such that:
    A[0] = 4
    A[1] = 1
    A[2] = 3
    A[3] = 2

is a permutation, but array A such that:
    A[0] = 4
    A[1] = 1
    A[2] = 3

is not a permutation, because value 2 is missing.

The goal is to check whether array A is a permutation.

Write a function:

    def solution(A)

that, given an array A, returns 1 if array A is a permutation and 0 if it is not.

For example, given array A such that:
    A[0] = 4
    A[1] = 1
    A[2] = 3
    A[3] = 2

the function should return 1.

Given array A such that:
    A[0] = 4
    A[1] = 1
    A[2] = 3

the function should return 0.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [1..100,000];
        each element of array A is an integer within the range [1..1,000,000,000].

Copyright 2009–2022 by Codility Limited. All Rights Reserved.
Unauthorized copying, publication or disclosure prohibited.
"""
import pytest

def solution_1_75_83_66(A):
    # Task Score 75%, Correctness 83%, Performance 66%
    if 1 not in A:
        return 0

    arr = list(range(1, sorted(A)[-1]+1))
    if len(arr) != len(A):
        return 0

    return 1

def solution_2_83_83_83(A):
    # Task Score 83%, Correctness 83%, Performance 83%
    # antiSum1: total sum is correct, but it is not a permutation, N <= 10
    # WRONG ANSWER got 1 expected 0
    # antiSum2 total sum is correct, but it is not a permutation, N = ~100,000
    # WRONG ANSWER got 1 expected 0
    if 1 not in A:
        return 0
    arr = list(range(1, len(A)+1))
    print(f'arr: {arr}, A: {A}')
    if len(arr) != len(A) or sum(arr) != sum(A):
        return 0
    return 1

def solution_3_91_100_83(A):
    # Task Score 91% Correctness 100% Performance 83%
    # large_range sequence 1, 2, ..., N, N = ~100,000 - RUNTIME ERROR
    if 1 not in A:
        return 0

    arr = list(range(1, sorted(A)[-1]+1)) # It's time consuming by sorting a list
    if len(arr) != len(set(A)) or len(arr) != len(A) or sum(arr) != sum(A):
        return 0
    return 1

def solution(A):
    """Scored 100"""
    if 1 not in A or 0 in A or len(A) != len(set(A)):
        return 0

    arr = list(range(1, len(A)+1))
    # When A = [1,2,3,5], len(A) = 4. Then len(arr) = 4.
    # So we cannot simply do somthing like --
    # if len(arr) != len(A):
    #     return 0
    if sum(arr) != sum(A):
        return 0
    return 1

#=======================================
# test with parameterized pytest.fixture
#=======================================
test_data = [
    ([], 0),           # fail at if 1 not in A
    ([0,1,2], 0),      # fail at if 0 in A
    ([1,2,3,2], 0),    # fail at if len(A) != len(set(A))
    ([1,2,3,5], 0),    # fail at if sum(arr) != sum(A)
    ([1,2,3,4,5], 1),
    ]

@pytest.fixture(params=test_data)
def get_test_data(request):
    """ Fixture as a data store to share information between steps"""
    return request.param

def test_solution_using_fixture(get_test_data):
    assert solution(get_test_data[0]) == get_test_data[1]

