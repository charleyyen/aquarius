"""
# OddOccurrencesInArray

A non-empty array A consisting of N integers is given.
The array contains an odd number of elements, and
each element of the array can be paired with another element that has the same value,
except for one element that is left unpaired.

For example, in array A such that:
  A[0] = 9  A[1] = 3  A[2] = 9
  A[3] = 3  A[4] = 9  A[5] = 7
  A[6] = 9

        the elements at indexes 0 and 2 have value 9,
        the elements at indexes 1 and 3 have value 3,
        the elements at indexes 4 and 6 have value 9,
        the element at index 5 has value 7 and is unpaired.

Write a function:

    def solution(A)

that, given an array A consisting of N integers fulfilling the above conditions,
returns the value of the unpaired element.

For example, given array A such that:
  A[0] = 9  A[1] = 3  A[2] = 9
  A[3] = 3  A[4] = 9  A[5] = 7
  A[6] = 9

the function should return 7, as explained in the example above.

Write an efficient algorithm for the following assumptions:

        N is an odd integer within the range [1..1,000,000];
        each element of array A is an integer within the range [1..1,000,000,000];
        all but one of the values in A occur an even number of times.

Copyright 2009–2022 by Codility Limited. All Rights Reserved.
Unauthorized copying, publication or disclosure prohibited.
"""
def solution(A):
    """
    Consider 3 scenarios:
    1) A has one element only
    2) The single appearance is the last element in array A
    3) The single appearance is in the middle
    """
    if len(A) == 1:
        return A[0] # A has one element only

    new_array = []
    for i, element in enumerate(sorted(A), start=1):
        if element not in new_array:
            new_array.append(element)
        else:
            new_array.pop(0)

        if i%2 == 0 and len(new_array) == 2:
            return new_array[0] # The single appearance is in the middle

    return new_array[0] # The single appearance is the last element in array A

if __name__ == "__main__":
    arr = [4,3,4,3,5,7,5]
    assert solution(arr) == 7
