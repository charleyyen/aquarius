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
#import unittest
import random

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

