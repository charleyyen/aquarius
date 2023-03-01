"""
A non-empty array A consisting of N integers is given.

The leader of this array is the value that occurs in more than half of the elements of A.

An equi leader is an index S such that 0 ≤ S < N − 1 and two sequences
A[0], A[1], ..., A[S] and A[S + 1], A[S + 2], ..., A[N − 1] have
leaders of the same value.

For example, given array A such that:
    A[0] = 4
    A[1] = 3
    A[2] = 4
    A[3] = 4
    A[4] = 4
    A[5] = 2

we can find two equi leaders:

        0, because sequences: (4) and (3, 4, 4, 4, 2) have the same leader, whose value is 4.
        2, because sequences: (4, 3, 4) and (4, 4, 2) have the same leader, whose value is 4.

The goal is to count the number of equi leaders.

Write a function:

    def solution(A)

that, given a non-empty array A consisting of N integers, returns the number of equi leaders.

For example, given:
    A[0] = 4
    A[1] = 3
    A[2] = 4
    A[3] = 4
    A[4] = 4
    A[5] = 2

the function should return 2, as explained above.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [1..100,000];
        each element of array A is an integer within the range [−1,000,000,000..1,000,000,000].

Copyright 2009–2023 by Codility Limited. All Rights Reserved. Unauthorized
copying, publication or disclosure prohibited.
"""
wrong_answer = 1_000_000_001
def find_leader_v1(arr):
    # This method is used by solution_v1()
    if len(arr) == 0 or len(set(arr)) == 0:
        return wrong_answer
    if len(arr) == 1 or len(set(arr)) == 1:
        return arr[0] 

    leader = sorted(arr)[len(arr)//2]
    if arr.count(leader)/len(arr) > 0.5:
        return leader

    return wrong_answer

def find_equi_leader_v1(leader, left, right):
    # This method is used by solution_v1()
    # Not efficient at all.
    # We know who is the leader, so we don't have to call find_leader_v1()
    # This is the reason why it's scored 55% only
    leader_in_left = find_leader_v1(left)
    leader_in_right = find_leader_v1(right)
    if leader_in_left == wrong_answer or leader_in_right == wrong_answer:
        return False

    if leader_in_right == leader and leader_in_right == leader_in_left:
        return True
    return False

def solution_v1(A):
    # Task Score 55% Correctness 100% Performance 0%
    leader = find_leader_v1(A)
    equi_leader_count = 0
    for i in range(len(A)):
        if find_equi_leader_v1(leader, A[:i+1], A[i+1:]):
            equi_leader_count += 1

    return equi_leader_count

def find_leader_v2(arr):
    # This method is used by solution_v2()
    if len(arr) == 1:
        return arr[0] 

    leader = sorted(arr)[len(arr)//2]
    if arr.count(leader)/len(arr) > 0.5:
        return leader

    return wrong_answer

def find_equi_leader_v2(leader, left, right):
    # This method is used by solution_v2()
    if len(left) == 0 or len(right) == 0:
        return False

    if left.count(leader)/len(left) > 0.5 and right.count(leader)/len(right) > 0.5:
        # This line increased the score from 55% to 77%
        return True
    return False

def solution_v2(A):
    # Task Score 77% Correctness 100% Performance 50%
    if len(set(A)) == 1:
        return len(A) - 1

    leader = find_leader_v2(A)
    if leader == wrong_answer:
        return 0

    equi_leader_count = 0
    for i in range(len(A)):
        if find_equi_leader_v2(leader, A[:i+1], A[i+1:]):
            equi_leader_count += 1

    return equi_leader_count

def solution_v3(A):
    # Task Score 77% Correctness 100% Performance 50%
    # large random test with two values, length = ~50,000
    # TIMEOUT ERROR. Killed. Hard limit reached: 6.000 sec.
    # large random(0,1) + 50000 * [0] + random(0, 1), length = ~100,000
    # TIMEOUT ERROR Killed. Hard limit reached: 6.000 sec.
    if len(set(A)) == 1:
        return len(A) - 1

    len_a = len(A) # This line does not increase performance much
    leader = sorted(A)[len_a//2]
    leader_count = A.count(leader)
    if leader_count <= len_a>>1:
        # W/O this check, the score is decreased to 66%
        return 0

    equi_leader_count = 0
    for i in range(len_a-1):
        left = A[:i+1]
        left_leader_count = left.count(leader) # This line slows down the performance
        right_leader_count = leader_count - left_leader_count
        if left_leader_count>i+1>>1 and right_leader_count>len_a-i-1>>1:
            equi_leader_count += 1

    return equi_leader_count

def solution_v4(A):
    # Task Score 77% Correctness 100% Performance 50%
    len_a_set = len(set(A))
    len_a = len(A)
    if len_a_set == 1:
        return len_a - 1

    leader = sorted(A)[len_a//2]
    leader_count = A.count(leader)
    if leader_count/len_a < 0.5:
        return 0

    left_leader = 0
    right_leader = leader_count
    equi_leader_count = 0
    for i in range(len_a-1):
        if A[i] == leader:
            left_leader += 1
            right_leader -= 1
        # Note: The block below can only score 77%
        left = A[:i+1]
        right = A[i+1:]
        if left_leader > len(left)>>1 and right_leader > len(right)>>1:
            equi_leader_count += 1
        # End of Note: The block below can only score 77%

        #if left_leader/(i+1) > 0.5 and right_leader/(len_a - i - 1) > 0.5:
            # This 'if' block scores 100%
            #equi_leader_count += 1
        if left_leader == leader_count:
            break

    return equi_leader_count

def solution_v5_best(A):
    # Task Score 100%
    if len(set(A)) == 1:
        return len(A) - 1

    len_a = len(A)
    leader = sorted(A)[len_a//2]
    """
    #------ Note: Another way to find the leader ------
    # This block does not affect performance!!
    hash_ = {}
    #for x in A:
    # Does not affect performance
    #    hash_[x] = 0
    #for x in A:
    #    hash_[x] += 1

    for x in A:
        if x not in hash_.keys():
        # Does not affect performance
            hash_[x] = 1
        else:
            hash_[x] += 1

    leader = wrong_answer
    for k,v in hash_.items():
        if v > len(A)>>1:
            leader = k
            break

    if leader == wrong_answer:
        return 0
    #------ End of Note: Another way to find the leader ------
    """
    leader_count = A.count(leader)
    if leader_count <= len_a>>1:
        return 0

    left_leader_count = 0
    right_leader_count = leader_count
    equi_leader_count = 0
    for i in range(len_a-1):
        if A[i] == leader: # this 'if' block is the KEY
            left_leader_count += 1
            right_leader_count -= 1

        if left_leader_count > i+1>>1 and right_leader_count > len_a-i-1>>1:
            equi_leader_count += 1

    return equi_leader_count

def solution_v5_modified(A):
    # Task Score 100%
    if len(set(A)) == 1:
        return len(A) - 1

    leader = sorted(A)[len(A)//2] # keep calling 'len(A)' would not slow down the performance
    leader_count = A.count(leader)
    if leader_count <= len(A) >>1:
        return 0

    left_leader_count = 0
    right_leader_count = leader_count
    equi_leader_count = 0
    for i in range(len(A)-1):
        if A[i] == leader:
            # This 'if' block is the KEY
            left_leader_count += 1
            right_leader_count -= 1

        #if left_leader/(i+1) > 0.5 and right_leader/(len_a - i - 1) > 0.5:
        # The line above is just as good as the line below
        if left_leader_count > i+1>>1 and right_leader_count > len(A)-i-1>>1:
            equi_leader_count += 1

    return equi_leader_count

def solution_v6(A):
    # Task Score 100%
    if len(set(A)) == 1:
        return len(A) - 1

    len_a = len(A)
    leader = sorted(A)[len_a//2]

    leader_count_list = []
    leader_count = 0
    for x in A:
        # this for loop would not slow down the performance
        if x == leader:
            leader_count += 1
        leader_count_list.append(leader_count)

    if leader_count <= len_a>>1:
        return 0

    equi_leader_count = 0
    for i in range(len_a-1):
        if leader_count_list[i]>i+1>>1 and leader_count-leader_count_list[i]>len_a-i-1>>1:
            equi_leader_count += 1

    return equi_leader_count

if __name__ == '__main__':
    import my_test # in house
    import time
    from aquarius.libs import data_generator
    arr = [4,3,4,4,4,2,2,4]
    solution = solution_v5_modified
    equi_leader_count = solution(arr)
    print(f'equi_leader_count: {equi_leader_count}')

    #N is an integer within the range [1..100,000];
    #each element of array A is an integer within the range [−1,000,000,000..1,000,000,000].
    low = -500_000_000
    high = +500_000_000
    maxium_size = 1000
    size = 350
    leader_size = maxium_size - size
    data_hash = data_generator.create_random_number_array(low=low, high=high, size=size)
    arr = data_hash['array_'].tolist()
    for i in range(leader_size):
        arr.append(high+1)

    solution_list = [
            solution_v1,
            solution_v2,
            solution_v3,
            solution_v4,
            solution_v5_best,
            solution_v5_modified,
            solution_v6
            ]
    summary = []
    for j, solution in enumerate(solution_list, start=1):
        method = str(solution).split()[1]
        start = time.time()
        answer = solution(arr)
        elapsed = round(time.time() - start, 4)
        #print(method, answer, elapsed)
        summary.append((method, answer, elapsed))

    my_test.display_summary(summary)

    """
    maxium_size = 100_000
    size = 35000
    1,          solution_v1 - 29999: Time Consumed: 1471.1237
    2,          solution_v2 - 29999: Time Consumed: 125.3926
    3,          solution_v3 - 29999: Time Consumed: 96.6138
    4,          solution_v4 - 29999: Time Consumed: 47.2818
    5,     solution_v5_best - 29999: Time Consumed: 0.036
    6, solution_v5_modified - 29999: Time Consumed: 0.0388
    7,          solution_v6 - 29999: Time Consumed: 0.0397

    maxium_size = 10_000
    size = 3500
    1,          solution_v1 - 2999: Time Consumed: 11.807
    2,          solution_v2 - 2999: Time Consumed: 1.1709
    3,          solution_v3 - 2999: Time Consumed: 0.9138
    4,          solution_v4 - 2999: Time Consumed: 0.3988
    5,     solution_v5_best - 2999: Time Consumed: 0.0036
    6, solution_v5_modified - 2999: Time Consumed: 0.0039
    7,          solution_v6 - 2999: Time Consumed: 0.0038

    maxium_size = 1000
    size = 350
    1,          solution_v1 - 299: Time Consumed: 0.1023
    2,          solution_v2 - 299: Time Consumed: 0.0108
    3,          solution_v3 - 299: Time Consumed: 0.0084
    4,          solution_v4 - 299: Time Consumed: 0.0037
    5,     solution_v5_best - 299: Time Consumed: 0.0003
    6, solution_v5_modified - 299: Time Consumed: 0.0003
    7,          solution_v6 - 299: Time Consumed: 0.0003
    """

