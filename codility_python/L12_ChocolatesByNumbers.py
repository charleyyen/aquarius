"""
Two positive integers N and M are given. Integer N represents the number
of chocolates arranged in a circle, numbered from 0 to N − 1.

You start to eat the chocolates. After eating a chocolate you leave only
a wrapper.

You begin with eating chocolate number 0. Then you omit the next M − 1
chocolates or wrappers on the circle, and eat the following one.

More precisely, if you ate chocolate number X, then you will next eat
the chocolate with number (X + M) modulo N (remainder of division).

You stop eating when you encounter an empty wrapper.

For example, given integers N = 10 and M = 4. You will eat the following
chocolates: 0, 4, 8, 2, 6.

The goal is to count the number of chocolates that you will eat, following
the above rules.

Write a function:

    def solution(N, M)

that, given two positive integers N and M, returns the number of chocolates
that you will eat.

For example, given integers N = 10 and M = 4. the function should return
5, as explained above.

Write an efficient algorithm for the following assumptions:

        N and M are integers within the range [1..1,000,000,000].

Copyright 2009–2023 by Codility Limited. All Rights Reserved. Unauthorized
copying, publication or disclosure prohibited.
"""
def get_greatest_common_divisor(N, M):
    """
    The Euclidean algorithm is used here, which is a way to find the greatest common divisor
    of two positive integers, N and M

    Formal description of the Euclidean algorithm

    Input Two positive integers, N and M.
    Output The greatest common divisor, gcd, of N and M.
    Internal computation
        Divide N by M and get the remainder, r. If r == 0, report M as the GCD of N and M.
        Replace N by M and replace M by r. Return to the previous step, which is a recursive call.
    ref: https://sites.math.rutgers.edu/~greenfie/gs2004/euclid.html
    """
    remainder = N%M
    if remainder:
        return get_greatest_common_divisor(M, remainder)
    return M

def solution(N, M):
    greatest_common_divisor = get_greatest_common_divisor(N, M)
    return int(N/greatest_common_divisor)

if __name__ == '__main__':
    print(solution(15,16))
