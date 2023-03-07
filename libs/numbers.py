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
    up_limit = 994_012
    if number > up_limit:
        # Cannot handle this number
        print(f'Cannot handle this number: "{number}"')
        print(f'The largest number this method can handle: {up_limit}')
        return None

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

def find_all_primes_in_range_2(start=1, end=2_147_483_647):
    #import sympy
    #return list(sympy.sieve.primerange(start, end))
    # draft
    return list(sorted(set(range(start,end+1)).difference(set((p * f) for p in range(2, int(end ** 0.5) + 2) for f in range(2, int(end/p) + 1)))))

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
        #print(method, answer, elapsed)
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
    i_0 = 100
    i_1 = 10_000_000
    start = time.time()
    primes_in_set = find_all_primes_in_range_1(start=i_0, end=i_1)
    elapsed = round(time.time() - start, 4)
    print(f'1. All primes between {i_0} and {i_1} (Total count: {len(primes_in_set)})')
    print(f'Time consumed: {elapsed}')
    start = time.time()
    primes_in_set = find_all_primes_in_range_2(start=i_0, end=i_1)
    print(f'2. All primes between {i_0} and {i_1} (Total count: {len(primes_in_set)})')
    #:\n{sorted(list(primes_in_set))}')
    print(f'Time consumed: {elapsed}')
    print()

if __name__ == '__main__':
    number = 994013 - 1

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
