"""
An array A consisting of N integers is given. It contains daily prices
of a stock share for a period of N consecutive days. If a single share
was bought on day P and sold on day Q, where 0 ≤ P ≤ Q < N, then the
profit of such transaction is equal to A[Q] − A[P], provided that
A[Q] ≥ A[P]. Otherwise, the transaction brings loss of A[P] − A[Q].

For example, consider the following array A consisting of six elements such that:
  A[0] = 23171
  A[1] = 21011
  A[2] = 21123
  A[3] = 21366
  A[4] = 21013
  A[5] = 21367

If a share was bought on day 0 and sold on day 2, a loss of 2048 would
occur because A[2] − A[0] = 21123 − 23171 = −2048. If a share was bought
on day 4 and sold on day 5, a profit of 354 would occur because
A[5] − A[4] = 21367 − 21013 = 354. Maximum possible profit was 356. It
would occur if a share was bought on day 1 and sold on day 5.

Write a function,

    def solution(A)

that, given an array A consisting of N integers containing daily prices
of a stock share for a period of N consecutive days, returns the maximum
possible profit from one transaction during this period. The function
should return 0 if it was impossible to gain any profit.

For example, given array A consisting of six elements such that:
  A[0] = 23171
  A[1] = 21011
  A[2] = 21123
  A[3] = 21366
  A[4] = 21013
  A[5] = 21367

the function should return 356, as explained above.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [0..400,000];
        each element of array A is an integer within the range [0..200,000].

Copyright 2009–2023 by Codility Limited. All Rights Reserved. Unauthorized
copying, publication or disclosure prohibited.
"""
import sys # solution_1

def solution_mine(A, possible_max=None):
    # Task Score 100%
    # Way more efficient than solution_1()
    if len(set(A)) <= 1:
        return possible_max if possible_max else 0

    max_0 = max(A)
    min_0 = min(A)
    max_0_index = A.index(max_0)
    min_0_index = A.index(min_0)
    if min_0_index <= max_0_index:
        # Simple Case: The minimum value is on the left of the maxium value.
        profit_0 = max_0 - min_0
        if possible_max:
            return profit_0 if profit_0 > possible_max else possible_max
        return profit_0

    # Complicated Case: The minimum value is on the right of the maxium value.
    #
    # Find the new maximum on the right of minimum
    max_1 = max(A[min_0_index:])
    # Find the new minimum on the left of maximum
    min_1 = min(A[:max_0_index+1])

    profit_0_1 = max_0 - min_1
    profit_1_0 = max_1 - min_0
    profit_1 = profit_0_1 if profit_0_1 > profit_1_0 else profit_1_0
    if possible_max:
        profit_1 = possible_max if possible_max > profit_1 else profit_1

    if len(A[max_0_index+1:min_0_index]) > 0:
        # Key: Recursive call
        return solution(A[max_0_index+1:min_0_index], possible_max=profit_1)
    return profit_1


def solution_1(A):
    # https://martinkysel.com/codility-maxprofit-solution/
    # Score 100% but it's almost 3 times slower
    # sys.maxsize == 9223372036854775807
    min_price = sys.maxsize
    max_profit = 0
    for a in A:
        min_price = min([min_price, a])
        max_profit = max([max_profit, a - min_price])

    return max_profit

if __name__ == '__main__':
    import my_test # in house

    import time
    from aquarius.libs import data_generator

    arr = [23171, 21011, 21123, 21366, 21013, 21367]
    arr = [6, 1, 3, 4, 2, 5]
    arr = [6, 6, 5, 4, 3, 4, 1]
    arr = [99, 6, 5, 14, 3, 4, 1]
    # N is an integer within the range [0..400,000];
    # each element of array A is an integer within the range [0..200,000].
    low = 0
    high = 200_000
    size = 4_000_000
    data_hash = data_generator.create_random_number_array(low=low, high=high, size=size)
    arr = data_hash['list_']
    print(f'Array length in test: {len(arr)}')

    summary = []
    solution_list = [solution_1, solution_mine]
    for j, solution in enumerate(solution_list, start=1):
        method = str(solution).split()[1]
        start = time.time()
        answer = solution(arr)
        elapsed = round(time.time() - start, 4)
        #print(method, answer, elapsed)
        summary.append((method, answer, elapsed))

    my_test.display_summary(summary)
