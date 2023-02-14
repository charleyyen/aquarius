"""
# CountDiv

Compute number of integers divisible by k in range [a..b].

Write a function:

    def solution(A, B, K)

that, given three integers A, B and K, returns the number of integers within the range [A..B] that are
divisible by K, i.e.:

    { i : A <= i <= B, i mod K = 0 }

For example, for A = 6, B = 11 and K = 2, your function should return 3, because there are three
numbers divisible by 2 within the range [6..11], namely 6, 8 and 10.

Write an efficient algorithm for the following assumptions:

    * A and B are integers within the range [0..2,000,000,000];
    * K is an integer within the range [1..2,000,000,000];
    * A ≤ B.

Copyright 2009–2022 by Codility Limited. All Rights Reserved.
Unauthorized copying, publication or disclosure prohibited.
"""
def solution_1(A: int, B: int, K: int) -> int:
    # Task Score 87% Correctness 75% Performance 100%
    # extreme_ifempty A = 10, B = 10, K in {5,7,20}
    # WRONG ANSWER got 1 expected 0
    if A == 0:
        return int(B/K) + 1

    if B < K:
        return 0

    i = A
    while i%K != 0:
        i += 1

    return int((B-i)/K) + 1 # Must use floor calculation

def solution_2(A: int, B: int, K: int) -> int:
    # Score 100%
    i = A
    while i%K != 0:
        i += 1

    return (B-i)//K + 1

def solution_3(A: int, B: int, K: int) -> int:
    # The following implementation (scored 100%) is from
    # https://github.com/johnmee/codility
    return B//K - (A-1)//K

    # ===================================================================
    # The following implementation scored 62%
    # Task Score 62% Correctness 50% Performance 75%
    # minimal A = B in {0,1}, K = 11
    # WRONG ANSWER got 0 expected 1 
    # extreme_endpoints verify handling of range endpoints, multiple runs
    # WRONG ANSWER got 7 expected 8
    # big_values3 A = 0, B = MAXINT, K in {1,MAXINT}
    # WRONG ANSWER got 1 expected 2
    # -----------------------------------------
    #return int(B/K) - int((A-1)/K) # Score 62%
    # -----------------------------------------

    # ===================================================================
    # Task Score 25% Correctness 0% Performance 50%
    # simple A = 11, B = 345, K = 17
    # WRONG ANSWER got 19 expected 20
    # minimal A = B in {0,1}, K = 11
    # WRONG ANSWER got 0 expected 1
    # extreme_ifempty A = 10, B = 10, K in {5,7,20}
    # WRONG ANSWER got 0 expected 1
    # extreme_endpoints verify handling of range endpoints, multiple runs
    # WRONG ANSWER got 2 expected 3
    # big_values3 A = 0, B = MAXINT, K in {1,MAXINT}
    # WRONG ANSWER got 1 expected 2
    # big_values4 A, B, K in {1,MAXINT}
    # WRONG ANSWER got 0 expected 1
    # -----------------------------------------
    #return (B - A + 1) // K        # Score 25%
    # -----------------------------------------

    # ===================================================================
    # Task Score 25% Correctness 0% Performance 50%
    # The details are the same as the above solution
    # -----------------------------------------
    #return int((B-A+1)/K)          # Score 25%
    # -----------------------------------------

if __name__ == '__main__':
    solution = solution_2
    print(solution(11, 345, 17))
    print(solution(0, 1, 11))
    print(solution(0, 0, 11))
    print(solution(10, 10, 5))
    print(solution(6, 11, 2))
    print(solution(11, 37, 17))
    print(solution(18, 37, 17))
    print(solution(11, 25, 5))
