"""All libs here are about numbers, int, prime, & float, etc."""
from aquarius.codility_python import my_test # in house

import inspect
import time
from math import sqrt

def find_prime_factors(n):
    """Very efficient"""
    a_set = set()
    c = 2
    while(n > 1):
        if(n % c == 0):
            a_set.add(c)
            n = n / c
        else:
            c = c + 1

    return a_set
 
def is_prime_1(number):
    """
    Not efficient. Don't use
    When n = 2_147_483_647
    This method takes ~130 seconds to complete
    """
    if not isinstance(number, int):
        return False

    if number == 1:
        return True

    for i in range(2, int(number/2)+1):
        # If num is divisible by any number between
        # 2 and n / 2, it is not prime
        if number % i == 0:
            return False
    else:
        return True


def is_prime_2(number, itr=None):
    """
    Efficient with a caveat:
    if number > 994012, then it'll throw an error:
        [Previous line repeated 995 more times]
        Recursive function Call
        RecursionError: maximum recursion depth exceeded while calling a Python object
    """
    function_name = inspect.currentframe().f_code.co_name
    up_limit = 994_012
    if number > up_limit:
        # Cannot handle this number
        print(f'{function_name}(): Cannot handle this number: "{number}"')
        print(f'The largest number this method can handle: {up_limit}')
        return 'N/A'

    if not isinstance(number, int):
        return False

    if number == 1:
        return True

    if not itr:
        itr = int(sqrt(number)+1)

    if itr == 1:
        #base condition
        return True
    if number % itr == 0:
        #if given number divided by itr or not
        return False
    if is_prime_2(number,itr-1) == False:
        # When number = 2_147_483_647
        return False

    return True


def is_prime_3(number):
    """
    Very efficient
    When n = 2_147_483_647
    This method takes 0.0054 seconds to complete
    """
    if not isinstance(number, int):
        return False

    if number == 1:
        return True

    for i in range(2, int(sqrt(number)) + 1):
        if (number % i == 0):
            return False
    else:
        return True


def is_prime_4(number):
    """
    Very efficient
    When n = 2_147_483_647
    This method takes 0.0054 seconds to complete
    """
    if not isinstance(number, int):
        return False

    if number == 1:
        return True

    # Loop through all numbers from 2 to the square root of n (rounded down to the nearest integer)
    for i in range(2, int(number**0.5)+1):
        # If number is divisible by any of these numbers, return False
        if number % i == 0:
            return False
    # If number is not divisible by any of these numbers, return True
    return True


def find_largest_prime(number):
    """To find a largest prime that is less or equal {number}"""
    while not is_prime_4(number):
        number -= 1

    return number

def find_all_primes_in_range_1(start=1, end=2_147_483_647):
    # Has performance issue
    #start = 993997
    #end = 994027
    a_set = set()
    for i in range(start+1, end):
        if is_prime_4(i):
            a_set.add(i)

    if len(a_set) == 0:
        return None
    return a_set

def find_all_primes_in_range_2(start=1, end=10_000_000): #end=2_147_483_647
    # When end is too large, say 500_000_000, it has performance issue.
    #import sympy
    #return list(sympy.sieve.primerange(start, end))
    # draft
    return list(sorted(set(range(start,end+1)).difference(set((p * f) for p in range(2, int(end ** 0.5) + 2) for f in range(2, int(end/p) + 1)))))

def find_all_primes_in_range_3(start=1, end=2_147_483_647):
    # Super Low efficient
    # https://www.faceprep.in/c/find-prime-numbers-in-a-given-range-in-c-c-java-and-python-faceprep/
    list_ = []
    while start < end:
        flag = 0
        for i in range(2, int(start/2), 1):
            if start%i == 0:
                flag = 1
                break
        if flag == 0:
            list_.append(i)
        start += 1

    return list_


def find_all_primes_in_range_4(start=1, end=2_147_483_647):
    # Low efficient
    list_ = []
    # MAKING SURE THAT a IS ODD BEFORE WE BEGIN
    # THE LOOP
    a = start
    b = end
    if a == 2:
        list_.append(2)
    if (a % 2 == 0):
        a+=1
    # NOTE : WE TRAVERSE THROUGH ODD NUMBERS ONLY
    for i in range(a,b+1,2):
        # flag variable to tell
        # if i is prime or not
        flag = 1
        # WE TRAVERSE TILL SQUARE ROOT OF j only.
        # (LARGEST POSSIBLE VALUE OF A PRIME FACTOR)
        j = 2
        while(j * j <= i):
            if (i % j == 0):
                flag = 0
                break
            j+=1
        # flag = 1 means i is prime
        # and flag = 0 means i is not prime
        if (flag == 1):
            list_.append(i)

    return list_

def find_all_primes_in_range_5(start=1, end=2_147_483_647):
#def find_all_primes_in_range_5(start=2, end=30):
    # High efficient
    prime = [True for i in range(end+1)]
    p = start 
    while p * p <= end:
        # If prime[p] is not changed, then it is a prime
        if prime[p]:
            # Updating all multiples of p
            for i in range(p * p, end+1, p):
                prime[i] = False
        p += 1

    list_ = []
    for p in range(2, end+1):
        if prime[p]:
            list_.append(p)
    return list_

# --- test ---
def test_is_prime(number=0):
    if number == 0:
        n = 2_147_483_647
    else:
        n = number

    function_name = inspect.currentframe().f_code.co_name
    print(f'In {function_name}(), number: {number}')

    method_list = [
        #is_prime_1,
        is_prime_2,
        is_prime_3,
        is_prime_4,
    ]
    summary = []
    for j, a_method in enumerate(method_list, start=1):
        method = str(a_method).split()[1]
        start = time.time()
        answer = a_method(n)
        elapsed = round(time.time() - start, 4)
        print(method, answer, elapsed)
        summary.append((method, answer, elapsed))
    my_test.display_summary(summary)
    print()


def test_find_prime_factors(number=0):
    if number == 0:
        n = 2_147_483_647
    else:
        n = number

    function_name = inspect.currentframe().f_code.co_name
    print(f'In {function_name}(), number: {number}')

    start = time.time()
    answer = find_prime_factors(number)
    elapsed = round(time.time() - start, 4)
    print(answer, elapsed)
    print()

def test_find_largest_prime(number=0):
    if number == 0:
        n = 2_147_483_647
    else:
        n = number

    function_name = inspect.currentframe().f_code.co_name
    print(f'In {function_name}(), number: {n}')

    start = time.time()
    answer = find_largest_prime(n)
    elapsed = round(time.time() - start, 4)
    print(f'The largest prime before {n} is {answer}')
    print(f'Time consumed: {elapsed}')
    print()


def test_find_all_primes_in_range():
    i_0 = 2
    i_1 = 100_000_000
    method_list = [
        #find_all_primes_in_range_1,
        #find_all_primes_in_range_2,
        #find_all_primes_in_range_3,
        #find_all_primes_in_range_4,
        find_all_primes_in_range_5,
    ]

    for j, a_method in enumerate(method_list, start=1):
        method = str(a_method).split()[1]
        start = time.time()
        answer = a_method(start=i_0, end=i_1)
        elapsed = round(time.time() - start, 4)
        print(f'{method}, {len(answer)}, {answer[:5]}, {answer[-5:]}, {elapsed}')

    """
    i_0 = 2
    i_1 = 1_000_000
    find_all_primes_in_range_4, 78498, [2, 3, 5, 7, 11], [999953, 999959, 999961, 999979, 999983], 8.6215
    find_all_primes_in_range_5, 78498, [2, 3, 5, 7, 11], [999953, 999959, 999961, 999979, 999983], 0.2018

    i_0 = 2
    i_1 = 10_000_000
    find_all_primes_in_range_5, 664579, [2, 3, 5, 7, 11], [9999937, 9999943, 9999971, 9999973, 9999991], 2.365

    i_0 = 2
    i_1 = 100_000_000
    find_all_primes_in_range_5, 5761455, [2, 3, 5, 7, 11], [99999931, 99999941, 99999959, 99999971, 99999989], 24.9535
    """


if __name__ == '__main__':
    number = 994013 - 1
    number = 999983

    #test_find_prime_factors(number=number)
    #test_find_largest_prime(number=number)

    #test_is_prime(number=number)
    """
    n=2_147_483_647
    1, is_prime_1 - True: Time Consumed: 129.8231
    2, is_prime_2 - True: Time Consumed: 0.0054
    3, is_prime_4 - True: Time Consumed: 0.0054
    """

    test_find_all_primes_in_range()
