"""
# TapeEquilibrium

Minimize the value |(A[0] + ... + A[P-1]) - (A[P] + ... + A[N-1])|.

A non-empty array A consisting of N integers is given.
Array A represents numbers on a tape.

Any integer P, such that 0 < P < N, splits this tape into two non-empty parts:
A[0], A[1], ..., A[P − 1] and A[P], A[P + 1], ..., A[N − 1].

The difference between the two parts is the value of:
|(A[0] + A[1] + ... + A[P − 1]) − (A[P] + A[P + 1] + ... + A[N − 1])|

In other words, it is the absolute difference between the sum of the first part
and the sum of the second part.

For example, consider array A such that:
  A[0] = 3
  A[1] = 1
  A[2] = 2
  A[3] = 4
  A[4] = 3

We can split this tape in four places:

        P = 1, difference = |3 − 10| = 7
        P = 2, difference = |4 − 9| = 5
        P = 3, difference = |6 − 7| = 1
        P = 4, difference = |10 − 3| = 7

Write a function:

    def solution(A)

that, given a non-empty array A of N integers, returns the minimal difference
that can be achieved.

For example, given:
  A[0] = 3
  A[1] = 1
  A[2] = 2
  A[3] = 4
  A[4] = 3

the function should return 1, as explained above.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [2..100,000];
        each element of array A is an integer within the range [−1,000..1,000].

Copyright 2009–2022 by Codility Limited. All Rights Reserved.
Unauthorized copying, publication or disclosure prohibited.
"""

def solution_01_53_100_0(A):
  # test score: 53%, Correctness: 100%, Performance: 0
  minimum = -1
  for P in range(1, len(A)):
    diff = abs(sum(A[:P])-sum(A[P:]))
    if minimum == -1:
      minimum = diff
    else:
      if minimum > diff:
        minimum = diff

  return minimum

def solution_02_76_57_100(A):
  # test score: 76%, Correctness: 57%, Performance: 100%
  minimum = -1
  left = A[0]
  right = sum(A[1:])

  for P in range(1, len(A)):
    left += A[P]
    right -= A[P]
    diff = abs(left - right)
    if minimum == -1:
      minimum = diff
    else:
      if minimum > diff:
        minimum = diff

  return minimum

def solution_03_100(A):
  # test score: 100%
  left = A[0]
  right = sum(A[1:])
  minimum = abs(left - right)
    
  for P in range(1, len(A)-1):
    left += A[P]
    right -= A[P]
    diff = abs(left - right)
    if minimum > diff:
      minimum = diff
    
  return minimum


if __name__ == '__main__':
    arr = list(range(-10, 10))
    arr = [3,1,2,4,3]
    arr = [1,2,1,1,1]
    arr = [1,1]
    arr = [-1000,1000]
    arr = [1]
    print(solution(arr))
