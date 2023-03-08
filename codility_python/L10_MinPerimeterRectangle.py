"""
An integer N is given, representing the area of some rectangle.

The area of a rectangle whose sides are of length A and B is A * B,
and the perimeter is 2 * (A + B).

The goal is to find the minimal perimeter of any rectangle whose area
equals N. The sides of this rectangle should be only integers.

For example, given integer N = 30, rectangles of area 30 are:

        (1, 30), with a perimeter of 62,
        (2, 15), with a perimeter of 34,
        (3, 10), with a perimeter of 26,
        (5, 6), with a perimeter of 22.

Write a function:

    def solution(N)

that, given an integer N, returns the minimal perimeter of any rectangle
whose area is exactly equal to N.

For example, given an integer N = 30, the function should return 22, as explained above.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [1..1,000,000,000].

Copyright 2009–2023 by Codility Limited. All Rights Reserved. Unauthorized
copying, publication or disclosure prohibited. 
"""

def solution(area):
    width = int(area**0.5)
    i, j = width, width
    while area%i != 0 and area%j != 0:
        i += 1
        j -= 1

    width = i if area%i == 0 else j
    return 2*(width + int(area/width))

if __name__ == '__main__':
    area = 101
    answer = solution(area)
    print(f'answer: {answer}')
