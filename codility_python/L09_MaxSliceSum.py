"""
A non-empty array A consisting of N integers is given. A pair of integers
(P, Q), such that 0 ≤ P ≤ Q < N, is called a slice of array A. The sum
of a slice (P, Q) is the total of A[P] + A[P+1] + ... + A[Q].

Write a function:

    def solution(A)

that, given an array A consisting of N integers, returns the maximum sum
of any slice of A.

For example, given array A such that:
A[0] = 3  A[1] = 2  A[2] = -6
A[3] = 4  A[4] = 0

the function should return 5 because:

        (3, 4) is a slice of A that has sum 4,
        (2, 2) is a slice of A that has sum −6,
        (0, 1) is a slice of A that has sum 5,
        no other slice of A has sum greater than (0, 1).

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [1..1,000,000];
        each element of array A is an integer within the range [−1,000,000..1,000,000];
        the result will be an integer within the range [−2,147,483,648..2,147,483,647].

Copyright 2009–2023 by Codility Limited. All Rights Reserved. Unauthorized
copying, publication or disclosure prohibited.
"""
def solution(array_):
    """Find a maximum sum of a compact subsequence of array elements. Score 100%"""
    if max(array_) < 0:
        # array_ll negative
        return sorted(array_)[-1]
    if min(array_) > 0:
        # array_ll positive
        return sum(array_)
    if len(array_) == 1:
        return array_[0]
    if len(array_) == 2:
        return max(array_)

    array_.append(-1)
    all_positive = 0
    max_positive = 0
    for _ in array_:
        if _ > -1:
            all_positive += _
        else:
            max_positive = max(max_positive, all_positive)
            all_positive += _
            if all_positive < 0:
                all_positive = 0
                continue

    return max_positive


if __name__ == '__main__':
    arr = [30,-1,2,-1,9,-6,4,0,-1]
    arr = [3,2,-6,4,0]
    arr = [-1,99,-98,94,5]
    print(solution(arr))
