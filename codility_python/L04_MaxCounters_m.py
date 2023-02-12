"""
# MaxCounters

Calculate the values of counters after applying all alternating operations:
increase counter by 1; set value of all counters to current maximum.

You are given N counters, initially set to 0, and you have two possible
operations on them:

    * increase(X) - counter X is increased by 1,
    * max counter - all counters are set to the maximum value of any counter.

A non-empty array A of M integers is given.
This array represents consecutive operations:

    * if A[K] = X, such that 1 <= X <=  N, then operation K is increase(X),
    * if A[K] = N + 1 then operation K is max counter.

For example, given integer N = 5 and array A such that:
    A[0] = 3
    A[1] = 4
    A[2] = 4
    A[3] = 6
    A[4] = 1
    A[5] = 4
    A[6] = 4

the values of the counters after each consecutive operation will be:
    (0, 0, 1, 0, 0)
    (0, 0, 1, 1, 0)
    (0, 0, 1, 2, 0)
    (2, 2, 2, 2, 2)
    (3, 2, 2, 2, 2)
    (3, 2, 2, 3, 2)
    (3, 2, 2, 4, 2)

The goal is to calculate the value of every counter after all operations.

Write a function:

    def solution(N, A)

that, given an integer N and a non-empty array A consisting of M integers,
returns a sequence of integers representing the values of the counters.

Result array should be returned as an array of integers.

For example, given:
    A[0] = 3
    A[1] = 4
    A[2] = 4
    A[3] = 6
    A[4] = 1
    A[5] = 4
    A[6] = 4

the function should return [3, 2, 2, 4, 2], as explained above.

Write an efficient algorithm for the following assumptions:

        N and M are integers within the range [1..100,000];
        each element of array A is an integer within the range [1..N + 1].

Copyright 2009–2022 by Codility Limited. All Rights Reserved.
Unauthorized copying, publication or disclosure prohibited.

"""
import random
import time

def solution_1_77_100_60(N, A):
    # Task Score 77% Correctness 100% Performance 60%
    arr = [0]*(N+1)
    maximum = 0
    for e in A:
        if e > N:
            arr = [maximum]*(N+1) # time consuming
        else:
            arr[e] += 1
            if arr[e] > maximum:
                maximum = arr[e]

    return arr[1:]

def solution_2_66_100_40(N, A):
    """
    Detected time complexity: O(N*M)
    Task Score 66% Correctness 100% Performance 40%
    large_random1: large random test, 2120 max_counter operations
    TIMEOUT ERROR
    running time: 1.040 sec., time limit: 0.272 sec.
    large_random2: large random test, 10000 max_counter operations
    TIMEOUT ERROR
    running time: 4.724 sec., time limit: 0.528 sec.
    extreme_large: all max_counter operations
    TIMEOUT ERROR
    Killed. Hard limit reached: 6.000 sec.
    """
    arr = [0]*(N)
    maxium = 0
    for e in A:
        if e > N:
            maxium += sorted(arr)[-1] # Time consuming
            arr = [0]*(N) # Time consuming
        else:
            arr[e-1] += 1

    return [x + maxium for x in arr]
    #return list(map(lambda x : x + maxium, arr)) # same score

def solution_3_66_100_40(N, A):
    # Task Score 66% Correctness 100% Performance 40%
    arr = [0]*(N)
    maxium = 0
    for e in A:
        if e > N:
            maxium = sorted(arr)[-1] # Time consuming
            arr = [maxium]*(N) # Time consuming
        else:
            arr[e-1] += 1

    return arr

def solution_4_66_100_40(N, A):
    # Task Score 66% Correctness 100% Performance 40%
    arr = [0]*(N)
    for e in A:
        if e > N:
            arr = [max(arr)]*(N) # Time consuming
        else:
            arr[e-1] += 1

    return arr


# ---------------------------------------------------------------
# I new the implementation below would fail the performance test.
# But I did not expected it scored ZERO, because it failed the
# performance test on EVERY sigle case!!
# ---------------------------------------------------------------
from collections import Counter

def solution_5_0(N, A):
    # Only passed the sample data. Score: 0
    indices = [i for i, x in enumerate(A) if x == N+1]
    j = 0
    maximum = 0
    for i, e in enumerate(indices):
        if i > 0:
            j = indices[i-1] + 1
        block = A[j:e]
        data = Counter(block)
        maximum += block.count(max(block, key=data.get))
    
    arr = [maximum]*(N)
    for e in A[indices[-1]+1:]:
        arr[e-1] += 1

    return arr
# end of solution_5_0()

def solution(N, A):
    """
    This solution is very much like the first solution - solution_1_77_100_60(N, A).
    The only difference is that when i > N, we save the maximum instead of assigning
    it to arr (arr = [maximum]). By doing so, it passed the performance test.
    """
    arr = [0]*(N)
    minimum = maximum = 0
    for i in A:
        if i > N:
            minimum = maximum
        else:
            arr[i-1] = max(arr[i-1], minimum)
            arr[i-1] += 1
            if arr[i-1] > maximum:
                maximum = arr[i-1]

    for i in range(len(arr)):
        arr[i] = max(arr[i], minimum)

    return arr


#data = [1, 3, 6, 4, 1, 2]
#data = [3, 4, 4, 6, 1, 4, 4]
#data = [6,3,4,4,6,1,1,6,2,2,2,6,3,3,3,3,3,3,6,1,4,4,6]
#data = [3, 4, 4, 6, 1, 1, 2, 2, 2, 3, 6, 5, 3, 3, 3, 3, 3, 6, 1, 4, 4]
def test_performance(arr_length, integer_count, random_number):
    #N and M are integers within the range [1..100,000];
    #each element of array A is an integer within the range [1..N + 1].
    arr = [random.randint(1, integer_count-1) for _ in range(arr_length)]
    print(f'A. arr length: {len(arr)}, random_number: {random_number}')
    for i in range(random_number):
        arr.append(arr_length+1)
    print(f'B. arr length: {len(arr)}, random_number: {random_number}')
    random.shuffle(arr)
    #arr = arr[:arr_length]
    print(f'C. arr length: {len(arr)}, random_number: {random_number}')
    
    print(f'arr[:10]: {len(arr[:10])}, arr[:10]: {arr[:10]}')
    print(f'arr[-10:]: {len(arr[-10:])}, arr[-10:]: {arr[-10:]}')
    if arr_length+1 in arr:
        print(f'arr.count({arr_length+1}): {arr.count(arr_length+1)}')
    else:
        print(f'{arr_length} is not in arr whose length is {len(arr)}')

    return arr

if __name__ == '__main__':
    arr_length = integer_count = 100000
    random_number = random.randint(1, integer_count/10)
#    arr_length = integer_count = 20
#    random_number = random.randint(1, integer_count-1)
    data = test_performance(arr_length, integer_count, random_number)
    print()

    start = time.time()
    new_arr = solution_1_77_100_60(arr_length, data)
    print(f'A. Total run time: {round((time.time() - start), 3)}')
    print(f'A. length: {len(new_arr)}\n{new_arr[:10]}\n{new_arr[-10:]}\n')

    start = time.time()
    new_arr = solution(arr_length, data)
    print(f'B. Total run time: {round((time.time() - start), 3)}')
    print(f'B. length: {len(new_arr)}\n{new_arr[:10]}\n{new_arr[-10:]}\n')
