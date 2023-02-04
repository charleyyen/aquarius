"""
# PermMissingElem
Find the missing element in a given permutation.

An array A consisting of N different integers is given.
The array contains integers in the range [1..(N + 1)],
 which means that exactly one element is missing.

Your goal is to find that missing element.

Write a function:

    def solution(A)

that, given an array A, returns the value of the missing element.

For example, given array A such that:
  A[0] = 2
  A[1] = 3
  A[2] = 1
  A[3] = 5

the function should return 4, as it is the missing element.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [0..100,000];
        the elements of A are all distinct;
        each element of array A is an integer within the range [1..(N + 1)].

Copyright 2009–2022 by Codility Limited. All Rights Reserved.
Unauthorized copying, publication or disclosure prohibited.
"""
import random
import time
from parameterized import parameterized

def solution_1(A):
    """
    To find the missing number from A
    A: An unsorted array contains consective integers with a range [1..(N + 1)]
       with one number missing
    Scored 100%
    """

    if len(A) == 0:
        return 1 # Empty array

    # Construct a new sorted array containing all elements in A plus the missing one
    new_arr = list(range(1, len(A) + 2))
    return sum(new_arr) - sum(A)

def solution_2(A):
    """
    To find the missing number from A using binary search
    Less efficient than solution_1(). But still scored 100%
    """
    if len(A) == 0:
        return 1 # Empty array

    A = sorted(A)
    if A[0] == 2:
        return 1 # first one missing
    if len(A) == A[-1]:
        return A[-1] + 1 # last one missing

    half = len(A)//2
    left = A[:half]
    right = A[half:]
    if left[-1] + 2 == right[0]:
        return right[0] - 1 # The middle one missing

    if len(left) == left[-1] - left[0]:
        return solution_2(left)

    return solution_2(right)

################################################################
N = 100000
class TestPermMissingElem:
    """To test both solution_1() & solution_2()"""
    @staticmethod
    def generate_test_data():
        """Construct a series of data for test"""
        test_data = [
                ([2,3,1,5], 4), # sample data
                ([2,4,1,5], 3), # missing the middle
                ([2,3,4,5], 1), # missing the first
                ([1,2,3,4], 5), # missing the last
                ]
        test_run = random.randint(3, 15)
        i = 0
        while i < test_run:
            uplimit = random.randrange(1, N+1)
            arr = list(range(1, uplimit))
            missing_number = arr[-1] + 1
            while missing_number not in arr:
                missing_number = random.randrange(1, N+1)

            arr.remove(missing_number)
            random.shuffle(arr)
            test_data.append((arr,missing_number))
            i += 1

        for element in test_data:
            yield element[0], element[1]

    @parameterized.expand(generate_test_data())
    def test_solution(self, arr, missing_number):
        """Test solution_1 & solution_2 to compare the performance"""
        print()
        i = 1
        for solution in (solution_1, solution_2):
            start = time.time()
            assert solution(arr) == missing_number
            print(f'{i}, Total run time: {round((time.time() - start), 3)}, Array Length: {len(arr)}')
            i += 1
