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

from aquarius.libs import split_array

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


def show_data_info(blocks, message, sorted_array=False):
    line = f"{'-'*10}"
    message = line + message + line
    print(message)
    if sorted_array:
        if len(blocks) < 20:
            print(blocks)
        else:
            print(f' Left 10: {blocks[:10]}')
            print(f'Right 10: {blocks[10:]}')
    else:
        #print(f'length: {len(blocks)}\nblocks[0] length: {len(blocks[0])}\nblocks[-1] length: {len(blocks[-1])}\n')
        if len(blocks[0]) > 10:
            print(f'blocks[0][:10]: {blocks[0][:10]}')
        else:
            if len(blocks[0]) == 0:
                if len(blocks[1]) > 10:
                    print(f'blocks[1][:10]: {blocks[1][:10]}')
                else:
                    print(f'blocks[1]: {blocks[1]}')
            else:
                print(f'blocks[0]: {blocks[0]}')

        if len(blocks[-1]) > 10:
            print(f'blocks[-1][:10]: {blocks[-1][:10]}')
        else:
            if len(blocks[-1]) == 0:
                if len(blocks[-2]) > 10:
                    print(f'blocks[-2][:10]: {blocks[-2][:10]}')
                else:
                    print(f'blocks[-2]: {blocks[-2]}')
            else:
                print(f'blocks[-1]: {blocks[-1]}')
    print(f"{'-'*len(message)}\n")


def main():
    #--------------------------------------
    # N and M are integers within the range [1..100,000];
    # each element of array A is an integer within the range [1..N + 1].
    N = M = 100000
    data = split_array.create_random_array(high=M, size=M)
    random_number_index = random.randint(1, len(data))
    random_number = int(data[random_number_index]//(N/1000))
    for i in range(random_number):
        data.append(N+1)
    random.shuffle(data)
    # print(f'random_number: {random_number}, N: {N}, data length: {len(data)}')

    print()

    start = time.time()
    new_arr = solution_1_77_100_60(N, data)
    print(f'A. Total run time (solution_1()): {round((time.time() - start), 3)}')
    #print(f'A. length: {len(new_arr)}\n{new_arr[:10]}\n{new_arr[-10:]}\n')
    new_arr_1 = sorted(list(set(new_arr)))
    message = f"{'-'*10} Unique Elements returned by solution_1() (Original Length: {len(new_arr)}) {'-'*10}"
    show_data_info(new_arr_1, message, sorted_array=True)

    start = time.time()
    new_arr = solution(N, data)
    print(f'B. Total run time (solution_2()): {round((time.time() - start), 3)}')
    #print(f'B. length: {len(new_arr)}\n{new_arr[:10]}\n{new_arr[-10:]}\n')
    new_arr_2 = sorted(list(set(new_arr)))
    message = f"{'-'*10} Unique Elements returned by solution_2() (Original Length: {len(new_arr)}) {'-'*10}"
    show_data_info(new_arr_1, message, sorted_array=True)


if __name__ == '__main__':
    data = [3, 4, 4, 6, 1, 1, 2, 2, 2, 3, 6, 5, 3, 3, 3, 3, 3, 6, 1, 4, 4]
    result = solution_1_77_100_60(6, data)
    print(f'Solution 1: {result}')
    result = solution(6, data)
    print(f'Solution 1: {result}')
    print()
    main()
