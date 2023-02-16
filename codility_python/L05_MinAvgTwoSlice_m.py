"""
MinAvgTwoSlice

Find the minimal average of any slice containing at least two elements.

https://codility.com/programmers/task/min_avg_two_slice/

A non-empty array A consisting of N integers is given.
A pair of integers (P, Q), such that 0 ≤ P < Q < N, is called a slice of array A
(notice that the slice contains at least two elements).
The average of a slice (P, Q) is the sum of A[P] + A[P + 1] + ... + A[Q] divided
by the length of the slice.
To be precise, the average equals (A[P] + A[P + 1] + ... + A[Q]) / (Q − P + 1).

For example, array A such that:
    A[0] = 4
    A[1] = 2
    A[2] = 2
    A[3] = 5
    A[4] = 1
    A[5] = 5
    A[6] = 8

contains the following example slices:

        slice (1, 2), whose average is (2 + 2) / 2 = 2;
        slice (3, 4), whose average is (5 + 1) / 2 = 3;
        slice (1, 4), whose average is (2 + 2 + 5 + 1) / 4 = 2.5.

The goal is to find the starting position of a slice whose average is minimal.

Write a function:

    def solution(A)

that, given a non-empty array A consisting of N integers, returns the starting
position of the slice with the minimal average. If there is more than one slice
with a minimal average, you should return the smallest starting position of such
a slice.

For example, given array A such that:
    A[0] = 4
    A[1] = 2
    A[2] = 2
    A[3] = 5
    A[4] = 1
    A[5] = 5
    A[6] = 8

the function should return 1, as explained above.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [2..100,000];
        each element of array A is an integer within the range [−10,000..10,000].

Copyright 2009–2022 by Codility Limited. All Rights Reserved.
Unauthorized copying, publication or disclosure prohibited.
----------------

# Discussion -- From https://github.com/johnmee/codility

The brute force solution is to determine the average of every slice of the
sequence. That's a lot of sequences! Is there a better way?

The solution doesn't even need prefix-sums.  The 'trick' is not in the coding at
all, but in an appreciation in the nature of the problem.

For this problem, the lowest average of two, or three, points can not be bested by
a longer sequence of points.  We do not need to consider any longer sequences.

To illustrate, consider [1, -1, 1, -1].
The two-point averages all come to 0.
The four-point average also comes to 0; it cannot best the two-point averages.
The three-point averages are 0.33 and -0.33.
So the correct answer is index point 1.

If you extend that sequence with, say, 100, it changes nothing.
If you extend that sequence with -100, then the answer becomes [-1, -100] (-50.5)
which is the best pair.

So we need to pass over the sequence once, calculating the two, and three, point
averages and returning the best of those.  O(N)

https://app.codility.com/demo/results/training6P83U6-V79/
"""
def solution(A):
    # Score 100%
    double_pos = triple_pos = 0
    double_min = triple_min = 10000
    for i in range(len(A) - 1):
        if double_min > (A[i] + A[i+1])/2:
            double_min = (A[i] + A[i+1])/2
            double_pos = i

    for i in range(len(A) - 2):
        if triple_min > (A[i] + A[i+1] + A[i+2])/3:
            triple_min = (A[i] + A[i+1] + A[i+2])/3
            triple_pos = i

    print(f'double_min: {double_min}, triple_min: {triple_min}')
    print(f'double_pos: {double_pos}, triple_pos: {triple_pos}')

    if double_min < triple_min:
        return double_pos 
    elif double_min > triple_min:
        return triple_pos
    else:
        return double_pos if double_pos <= triple_pos else triple_pos


if __name__ == '__main__':
    arr = [4,1,8000,1000,1,4,1,8]
    index = int(solution(arr))
    print(f'{arr}. index: {index}')
