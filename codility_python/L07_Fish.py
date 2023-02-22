"""
Task description

You are given two non-empty arrays A and B consisting of N integers.
Arrays A and B represent N voracious fish in a river, ordered
downstream along the flow of the river.

The fish are numbered from 0 to N − 1. If P and Q are two fish and P < Q,
then fish P is initially upstream of fish Q. Initially, each fish has a unique position.

Fish number P is represented by A[P] and B[P]. Array A contains the sizes
of the fish. All its elements are unique. Array B contains the directions
of the fish. It contains only 0s and/or 1s, where:

        0 represents a fish flowing upstream,
        1 represents a fish flowing downstream.

If two fish move in opposite directions and there are no other (living)
fish between them, they will eventually meet each other. Then only one
fish can stay alive − the larger fish eats the smaller one. More precisely,
we say that two fish P and Q meet each other when P < Q, B[P] = 1 and
B[Q] = 0, and there are no living fish between them. After they meet:

        If A[P] > A[Q] then P eats Q, and P will still be flowing downstream,
        If A[Q] > A[P] then Q eats P, and Q will still be flowing upstream.

We assume that all the fish are flowing at the same speed. That is, fish moving
in the same direction never meet. The goal is to calculate the number of fish
that will stay alive.

For example, consider arrays A and B such that:
  A[0] = 4    B[0] = 0
  A[1] = 3    B[1] = 1
  A[2] = 2    B[2] = 0
  A[3] = 1    B[3] = 0
  A[4] = 5    B[4] = 0

Initially all the fish are alive and all except fish number 1 are moving upstream.
Fish number 1 meets fish number 2 and eats it, then it meets fish number 3 and
eats it too. Finally, it meets fish number 4 and is eaten by it. The remaining
two fish, number 0 and 4, never meet and therefore stay alive.

Write a function:

    def solution(A, B)

that, given two non-empty arrays A and B consisting of N integers, returns the
number of fish that will stay alive.

For example, given the arrays shown above, the function should return 2, as explained above.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [1..100,000];
        each element of array A is an integer within the range [0..1,000,000,000];
        each element of array B is an integer that can have one of the following values: 0, 1;
        the elements of A are all distinct.

Copyright 2009–2023 by Codility Limited. All Rights Reserved. Unauthorized copying,
publication or disclosure prohibited.
"""
from parameterized import parameterized

def solution(fish_size, direction):
    """handle_generic_cases"""
    d_live = []
    count = len(fish_size)

    for i, fish_i in enumerate(fish_size):
        if direction[i] > 0:
            d_live.append(fish_i)

        if direction[i] == 0:
            if len(d_live) > 0:
                for d_fish in d_live[::-1]:
                    count -= 1
                    if d_fish > fish_i:
                        break
                    d_live.pop()

    return count

class TestFish:
    """To test solution()"""
    @staticmethod
    def generate_test_data():
        """Construct a series of data for test"""
        test_data = [
            # All downstreams
            (([9,8,4,3,2,7,1,6,5], [1,1,1,1,1,1,1,1,1]), 9),
            # A_ll upstreams
            (([9,8,4,3,2,7,1,6,5], [0,0,0,0,0,0,0,0,0]), 9),
            # The only downstream is at the end
            (([9,8,4,3,2,7,1,6,5], [0,0,0,0,0,0,0,0,1]), 9),
            # The only upstream is at the beginning
            (([9,8,4,3,2,7,1,6,5], [0,1,1,1,1,1,1,1,1]), 9),
            # The only downstream is at the beginning and it's the largest
            (([9,8,4,3,2,7,4,6,1], [1,0,0,0,0,0,0,0,0]), 1),
            # The only upstream is at the end and it's the largest
            (([5,8,4,3,2,7,1,6,9], [1,1,1,1,1,1,1,1,0]), 1),
            # The only downstream is the smallest
            (([9,8,1,3,2,7,4,6,5], [0,0,1,0,0,0,0,0,0]), 8),
            # The only upstream is the smallest
            (([9,8,4,3,2,7,1,6,5], [1,1,1,1,1,1,0,1,1]), 8),
            # Some more generic data
            (([5,1,4,3,2,8,9,6,7], [0,1,0,0,0,0,1,1,1]), 8),
            (([5,9,4,3,2,8,1,6,7], [0,1,1,1,1,1,0,1,1]), 8),
            (([5,1,4,3,2,8,9,6,7], [0,1,0,1,0,0,1,0,1]), 5),
            # Sample data given by the assignment
            (([4,3,2,1,5], [0,1,0,0,0]), 2),
        ]

        for element in test_data:
            yield element[0], element[1]


    @parameterized.expand(generate_test_data())
    def test_solution(self, data, expected):
        """Test solution()"""
        assert solution(data[0], data[1]) == expected
