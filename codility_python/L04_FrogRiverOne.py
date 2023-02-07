"""
Frog River One

A small frog wants to get to the other side of a river. The frog is initially located on one bank of the river (position
 0) and wants to get to the opposite bank (position X+1). Leaves fall from a tree onto the surface of the river.

You are given an array A consisting of N integers representing the falling leaves. A[K] represents the position where
one leaf falls at time K, measured in seconds.

The goal is to find the earliest time when the frog can jump to the other side of the river. The frog can cross only
when leaves appear at every position across the river from 1 to X (that is, we want to find the earliest moment when
all the positions from 1 to X are covered by leaves). You may assume that the speed of the current in the river is
negligibly small, i.e. the leaves do not change their positions once they fall in the river.

For example, you are given integer X = 5 and array A such that:
  A[0] = 1
  A[1] = 3
  A[2] = 1
  A[3] = 4
  A[4] = 2
  A[5] = 3
  A[6] = 5
  A[7] = 4

In second 6, a leaf falls into position 5. This is the earliest time when leaves appear in every position across the
river.

Write a function:

    def solution(X, A)

that, given a non-empty array A consisting of N integers and integer X, returns the earliest time when the frog can jump
to the other side of the river.

If the frog is never able to jump to the other side of the river, the function should return −1.

For example, given X = 5 and array A such that:
  A[0] = 1
  A[1] = 3
  A[2] = 1
  A[3] = 4
  A[4] = 2
  A[5] = 3
  A[6] = 5
  A[7] = 4

the function should return 6, as explained above.

Write an efficient algorithm for the following assumptions:

        N and X are integers within the range [1..100,000];
        each element of array A is an integer within the range [1..X].

Copyright 2009–2022 by Codility Limited. All Rights Reserved. Unauthorized copying, publication or disclosure
prohibited.
"""
import random
from parameterized import parameterized

def solution(X,A):
    """
    Find the first appearance of the element e's index i
    so that set(A[:i+1]) == set(range(1, X+1))
        where 1 <= e <= X
        then
            return i
    e.g.
        A = [1,5,1,4,3,2,3,5]
        X = 5
    Answer:
        At index i = 5, A[5] = 2. So A[:6] = [1,5,1,4,3,2]
        set(range(1, X+1) = set(range(1, 6)) = {1,2,3,4,5}
        set(A[:6]) = {1,5,4,3,2} == {1,2,3,4,5}
        return 5
    """
    baseline_set = set(range(1, X+1))
    subset_ = set(A[:X])
    if baseline_set == subset_:
        return X - 1
    
    for j, x in enumerate(A[X:], start = len(A[:X])):
        subset_.add(x)
        if baseline_set == subset_:
            return j
  
    return -1

class TestFrogRiverOne:
    """To test solution()"""
    @staticmethod
    def generate_test_data():
        """Construct a series of data for test"""
        test_data = [
                # sample data
                # X = 5, A = [1, 3, 1, 4, 2, 3, 5, 4], the expected index: 6
                ((5, [1, 3, 1, 4, 2, 3, 5, 4]), 6),
                # Below are simple cases
                ((5, [1,5,1,4,3,2,3,5]), 5),
                ((3, [3, 3, 1, 1, 4]), -1),
                ((3, [3, 3, 3, 1, 1, 2]), 5),
                ((4, [3, 2, 1]), -1),
                # Below are extreme cases
                ((1, [1]), 0),
                ((0, [2]), -1),
                ((2, [2]), -1),
                ((2, [2, 1]), 1),
                ((2, [1, 2]), 1),
                ((2, [1, 1]), -1),
                ((2, [2, 2]), -1),
                ((3, [1, 2]), -1),
                ]

        x = 100000
        arr = list(range(1, x))
        random.shuffle(arr)
        arr.append(x)
        test_data.append(((x, arr), x-1))

        for element in test_data:
            yield element[0], element[1]


    @parameterized.expand(generate_test_data())
    def test_solution(self, data, expected):
        """Test solution()"""
        print(f'Data Type: {type(data)}, Data: #{data}#, expected: #{expected}#')
        assert solution(data[0], data[1]) == expected
