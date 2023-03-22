"""
# A candidate for the new tool - lineBreaker.py

A non-empty array A consisting of N integers is given.

A peak is an array element which is larger than its neighbors. More
precisely, it is an index P such that 0 < P < N − 1,  A[P − 1] < A[P]
and A[P] > A[P + 1].

For example, the following array A:
    A[0] = 1
    A[1] = 2
    A[2] = 3
    A[3] = 4
    A[4] = 3
    A[5] = 4
    A[6] = 1
    A[7] = 2
    A[8] = 3
    A[9] = 4
    A[10] = 6
    A[11] = 2

has exactly three peaks: 3, 5, 10.

We want to divide this array into blocks containing the same number of
elements. More precisely, we want to choose a number K that will yield
the following blocks:

        A[0], A[1], ..., A[K − 1],
        A[K], A[K + 1], ..., A[2K − 1],
        ...
        A[N − K], A[N − K + 1], ..., A[N − 1].

What's more, every block should contain at least one peak. Notice that
extreme elements of the blocks (for example A[K − 1] or A[K]) can also
be peaks, but only if they have both neighbors (including one in an
adjacent blocks).

The goal is to find the maximum number of blocks into which the array
A can be divided.

Array A can be divided into blocks as follows:

    one block (1, 2, 3, 4, 3, 4, 1, 2, 3, 4, 6, 2). This block contains three peaks.
    two blocks (1, 2, 3, 4, 3, 4) and (1, 2, 3, 4, 6, 2). Every block has a peak.
    three blocks (1, 2, 3, 4), (3, 4, 1, 2), (3, 4, 6, 2). Every block has a peak.
    Notice in particular that the first block (1, 2, 3, 4) has a peak at A[3], because
    A[2] < A[3] > A[4], even though A[4] is in the adjacent block.

However, array A cannot be divided into four blocks, (1, 2, 3), (4, 3, 4), (1, 2, 3)
and (4, 6, 2), because the (1, 2, 3) blocks do not contain a peak. Notice in
particular that the (4, 3, 4) block contains two peaks: A[3] and A[5].

The maximum number of blocks that array A can be divided into is three.

Write a function:

    def solution(A)

that, given a non-empty array A consisting of N integers, returns the
maximum number of blocks into which A can be divided.

If A cannot be divided into some number of blocks, the function should return 0.

For example, given:
    A[0] = 1
    A[1] = 2
    A[2] = 3
    A[3] = 4
    A[4] = 3
    A[5] = 4
    A[6] = 1
    A[7] = 2
    A[8] = 3
    A[9] = 4
    A[10] = 6
    A[11] = 2

the function should return 3, as explained above.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [1..100,000];
        each element of array A is an integer within the range [0..1,000,000,000].

Copyright 2009–2023 by Codility Limited. All Rights Reserved. Unauthorized
copying, publication or disclosure prohibited.
"""
def create_peaks(arr):
    n = len(arr)
    peaks_array = [False] * n
    peaks_index = []
    for i in range(1, n-1):
        if arr[i] > max(arr[i-1], arr[i+1]):
            peaks_array[i] = True
            peaks_index.append(i)
    return peaks_array, peaks_index

def find_peak_distance(peak_indices):
    peak_distance = []
    start = 1
    for i, coordinate in enumerate(peak_indices[start:], start=start):
        delta = coordinate - peak_indices[i-1]
        peak_distance.append(delta)

    return peak_distance


def verify(array_, peaks_array, max_possible_group_count, element_count_in_each_group):
    i = 0
    while i < max_possible_group_count:
        if i == 0:
            new_array = array_[0:element_count_in_each_group]
            start = 0
        elif i*element_count_in_each_group == len(array_):
            new_array = array_[i*element_count_in_each_group:]
            start = (i-1)*element_count_in_each_group
        else:
            new_array = array_[(i-1)*element_count_in_each_group:i*element_count_in_each_group]
            start = (i-1)*element_count_in_each_group

        i += 1
        if not is_peak_in_new_array(peaks_array, start, new_array):
            return False
    return True

def is_peak_in_new_array(peaks_array, start, new_array):
    for j, e in enumerate(new_array, start=start):
        if peaks_array[j]:
            # This section of the original array contains a peak
            return True
    return False


def solution_mine(array_):
    # Score 100%
    peaks_array, peaks_index = create_peaks(array_)
    if len(peaks_index) == 0:
        # No peak in array_
        return 0
    if len(peaks_index) == 1:
        # One peak in array_
        return 1

    peak_distance = find_peak_distance(peaks_index)
    sorted_peak_distance = sorted(peak_distance)
    # Max distance between two peaks
    max_mid_distance = sorted_peak_distance[-1]

    # The left most peak's distance to the start point
    left_distance = peaks_index[0] + 1
    # The right most peak's distance to the end point
    right_distance = len(array_) - peaks_index[-1]

    max_distance = max(left_distance, right_distance, max_mid_distance//2)
    if max_distance == 0:
        return 0

    max_possible_group_count = len(array_)//max_distance
    while len(array_)%max_possible_group_count != 0:
        # make sure max_possible_group_count can be divided by the length of array_
        max_possible_group_count -= 1

    if max_possible_group_count == 1:
        return 1

    # We know len(array_)//max_possible_group_count == int(len(array_)/max_possible_group_count)
    # i.e. max_possible_group_count is divisible by len(array_)
    element_count_in_each_group = len(array_)//max_possible_group_count

    true_or_false = verify(array_, peaks_array, max_possible_group_count, element_count_in_each_group)
    # if true_or_false is True, then each group contains at least one peak
    while not true_or_false:
        max_possible_group_count -= 1
        if max_possible_group_count == 1:
            return max_possible_group_count

        while len(array_)%max_possible_group_count != 0:
            # Again, make sure that max_possible_group_count is divisible by len(array_)
            max_possible_group_count -= 1

        if max_possible_group_count == 1:
            return max_possible_group_count

        element_count_in_each_group = len(array_)//max_possible_group_count
        true_or_false = verify(array_, peaks_array, max_possible_group_count, element_count_in_each_group)

    return max_possible_group_count


def solution_02(A):
    # write your code in Python 3.6
    
    peak_list = []
    
    # find peaks
    for index in range( 1, len(A)-1 ):
        if A[index] > A[index-1] and A[index] > A[index+1]:
            peak_list.append( index )
    
    #print(peak_list)

    for num_block in range( len(A), 0 , -1 ):

        # check 'blocks containing the same number of elements'
        if ( len(A) % num_block == 0):
            
            block_size = int( len(A)/num_block ) 
            ith_block = 0
            num_block_has_peak = 0
            
            for peak_index in peak_list:
                
                # check if any peak is within the ith block
                if int( peak_index/block_size) == ith_block: 
                    num_block_has_peak += 1
                    ith_block += 1
        
            # chek if all blocks have at least one peak
            if num_block_has_peak == num_block:
                return num_block
    
    return 0


def solution_03(A):
    N = len(A)
    if N < 3: return 0
    peaks = []

    for idx in range(1, N-1):
        if A[idx-1] < A[idx] > A[idx+1]:
            peaks.append(idx)

    for size in range(len(peaks), 0, -1):
         if N % size == 0:

            block_len = N // size
            check = [0]*size
            for elem in peaks:
                ptr = elem // block_len
                if check[ptr] == 0:
                    check[ptr] = 1

            if check.count(1) == size:
                return size

    return 0

def solution_04(A):

    length = len(A)

    # array ends can't be peaks, len < 3 must return 0
    if length < 3:
        return 0

    peaks = [0] * length

    # compute a list of 'peaks to the left' in O(n) time
    for index in range(2, length):
        peaks[index] = peaks[index - 1]

        # check if there was a peak to the left, add it to the count
        if A[index - 1] > A[index - 2] and A[index - 1] > A[index]:
            peaks[index] += 1

    # candidate is the block size we're going to test
    for candidate in range(3, length + 1):

        # skip if not a factor
        if length % candidate != 0:
            continue

        # test at each point n / block
        valid = True
        index = candidate
        while index != length:

            # if no peak in this block, break
            if peaks[index] == peaks[index - candidate]:
                valid = False
                break

            index += candidate

        # one additional check since peaks[length] is outside of array
        if index == length and peaks[index - 1] == peaks[index - candidate]:
            valid = False

        if valid:
            return length // candidate

    return 0


if __name__ == '__main__':
    """
    arr = [1,1,2,1,1]
    arr = [1, 2, 3, 4, 3, 4, 1, 2, 3, 4, 6, 2]
    arr = [1, 1, 1, 1, 2, 1, 4, 1, 1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,4, 1, 2, 1, 2,3,4, 1, 2, 1, 1,1]
    arr = [1, 1, 1, 1, 2, 1, 1]
    arr = [1, 1, 2, 1, 2, 1, 1]
    print(solution_mine(arr))
    print(solution_02(arr))
    print(solution_03(arr))
    print(solution_04(arr))
    """

    high = 1_000_000_000
    size = 100_000
    solution_list = [
        solution_mine,
        solution_02,
        solution_03,
        solution_04,
    ]

    import my_test # in house
    import time
    from aquarius.libs import data_generator

    arr = data_generator.create_random_number_array_withiout_same_neibour(high=high, size=size)
    print(f'Array length in test: {len(arr)}')
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
[aquarius] codility_python 207 => p3 L10_Peaks_m.py
Array length in test: 100000
1, solution_mine - 10,000: Time Consumed: 0.0609
2,   solution_02 - 10,000: Time Consumed: 0.0654
3,   solution_03 - 10,000: Time Consumed: 0.033
4,   solution_04 - 10,000: Time Consumed: 0.0339
"""

