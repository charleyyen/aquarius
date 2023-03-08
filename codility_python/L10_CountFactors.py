"""
A positive integer D is a factor of a positive integer N if there exists
an integer M such that N = D * M.

For example, 6 is a factor of 24, because M = 4 satisfies the above condition (24 = 6 * 4).

Write a function:

    def solution(N)

that, given a positive integer N, returns the number of its factors.

For example, given N = 24, the function should return 8, because 24 has 8 factors,
namely 1, 2, 3, 4, 6, 8, 12, 24. There are no other factors of 24.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [1..2,147,483,647].

Copyright 2009–2023 by Codility Limited. All Rights Reserved. Unauthorized
copying, publication or disclosure prohibited.
"""
import math

def find_prime_factors(number):
    list_ = []
    c = 2 
    while(number > 1): 
        if(number % c == 0): 
            list_.append(c)
            number = number / c 
        else:
            c = c + 1 

    return list_


def is_prime(number):
    for i in range(2, int(number**0.5)+1):
        if number % i == 0:
            return False
    return True


def solution_mine(number):
    """
    This is the most efficient!!
    """
    if number == 1:
        return 1
    if is_prime(number):
        return 2

    factors = find_prime_factors(number)
    # factors is a list containing all prime factors
    # e.g.
    # number = 2_147_483_647 - 1 = 2_147_483_646
    # factors: [2, 3, 3, 7, 11, 31, 151, 331]
    # Theory:
    # If N = a_1^n_1 * a_2^n_2 * ... * a_m^n_m
    #   where a_1, a_2, ... , a_m are all primes
    #     and n_1, n_2, ... , n_m are all integers
    # then the total number of factors are
    #   (n_1 + 1) * (n_2 + 1) * ... * (n_m + 1)
    # Therefore, when number == 2_147_483_646, then
    # factors: [2, 3, 3, 7, 11, 31, 151, 331]
    # the total factor counts are:
    # 2*3*2*2*2*2*2 = 2^6 * 3 = 64 * 3 = 192

    factor_count = {}
    for i in factors:
        if i not in factor_count.keys():
            factor_count[i] = 2
        else:
            factor_count[i] += 1

    return math.prod(factor_count.values())

def solution_1(N):
    """
    Credit to: https://github.com/Mickey0521/Codility-Python/blob/master/CountFactors.py
    """
    # write your code in Python 3.6

    my_dictionary = {}

    # be careful about the range
    # O(n)
    '''
    for n in range( 1, N+1 ):
        if N % n == 0:
            my_dictionary[n] = True
    '''

    # O( log(n) )
    # be careful: we need to check 'math.sqrt(N)+1'
    for n in range( 1, int( math.sqrt(N) ) +1 ):
        if N % n ==0:
            my_dictionary[n] = True
            another_factor = int( N/n )
            my_dictionary[another_factor] = True

    # print(my_dictionary)

    num_factors = len( my_dictionary )

    return num_factors

def solution_2(N):
    """
    Credit to: https://github.com/shihsyun/codility_lessons/blob/master/Lesson10/count_factors.py
    """
    # write your code in Python 3.6
    # 參考codility附的教材，利用平方根方式求因數。
    # more detail please check it out at https://codility.com/media/train/8-PrimeNumbers.pdf .

    if N == 1:
        return 1

    count = 0
    i = 1

    while i**2 < N:
        if N % i == 0:
            count += 2

        i += 1

    if i**2 == N:
        count += 1

    return count


def solution_3(N):
    """
    Credit to: https://github.com/Dineshkarthik/codility-training/blob/master/Lesson%2010%20-%20Prime%20and%20composite%20numbers/count_factors.py
    """
    result = 0
    if N > 0:
        i = 1
        factors = []
        while i**2 <= N:
            if N % i == 0:
                if (N / i) != i:
                    factors.append(i)
                    factors.append(N / i)
                else:
                    factors.append(i)
            i += 1
        result = len(factors)
    return result


if __name__ == '__main__':
    # N is an integer within the range [1..2,147,483,647].
    number = 2_147_483_647 - 1
    # factors: [2, 3, 3, 7, 11, 31, 151, 331]

    solution_list = [
        solution_mine,
        solution_1,
        solution_2,
        solution_3,
    ]
    import my_test # in house
    import time

    summary = []
    for j, solution in enumerate(solution_list, start=1):
        method = str(solution).split()[1]
        start = time.time()
        answer = solution(number)
        elapsed = round(time.time() - start, 4)
        #print(method, answer, elapsed)
        summary.append((method, answer, elapsed))
    my_test.display_summary(summary)
    '''
    A. Number = 2_147_483_646
    1, solution_mine - 192: Time Consumed: 0.0001
    2,    solution_1 - 192: Time Consumed: 0.0063
    3,    solution_2 - 192: Time Consumed: 0.0207
    4,    solution_3 - 192: Time Consumed: 0.02

    B. Number = 2_147_483_647
    1, solution_mine - 2: Time Consumed: 0.0061
    2,    solution_1 - 2: Time Consumed: 0.0058
    3,    solution_2 - 2: Time Consumed: 0.0201
    4,    solution_3 - 2: Time Consumed: 0.0201
    '''
