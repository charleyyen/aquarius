"""
# Binary Gap

A binary gap within a positive integer N is any maximal sequence of consecutive zeros that is surrounded by ones at
both ends in the binary representation of N.

For example,
The number 9 has binary representation 1001 and contains a binary gap of length 2.
The number 529 has binary representation 1000010001 and contains two binary gaps: one of length 4 and one of length 3.
The number 20 has binary representation 10100 and contains one binary gap of length 1.
The number 15 has binary representation 1111 and has no binary gaps.
The number 32 has binary representation 100000 and has no binary gaps.

Write a function:

    def solution(N)

that, given a positive integer N, returns the length of its longest binary gap.
The function should return 0 if N doesn't contain a binary gap.

For example, given N = 1041 the function should return 5, because N has binary representation 10000010001 and so its
 longest binary gap is of length 5. Given N = 32 the function should return 0, because N has binary representation
 '100000' and thus no binary gaps.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [1..2,147,483,647].

Copyright 2009–2022 by Codility Limited. All Rights Reserved.
Unauthorized copying, publication or disclosure prohibited.
"""
from parameterized import parameterized

def solution(N):
    """
    Determines the maximal 'binary gap' in an integer.

    :param N: [int] A positive integer (between 1 and maxint).
    :return: [int] The length of the longest sequence of zeros in the binary representation of the integer.

    Convert the int to a binary whose type is actually astring
    Loop through the binary string.
    When we see the first 1, record the position index - start
    When we see the next 1 at position i, then the gap is i - start - 1
       If the gap is larger than the previous gap, assign the new gap value to gap
    When we run out of characters, return the gap which should be the largest one.

    This solution scored 100%
    """
    binary_string = bin(N)
    gap = 0
    start = 0
    for i in range(2, len(binary_string)):
        if start:
            if binary_string[i] == '1':
                if gap < i - start - 1:
                    gap = i - start - 1
                start = i
        else:
            if binary_string[i] == '1':
                start = i

    return gap


###############################################################
# Note: As reference, below is another implementation credited
# to https://github.com/johnmee/codility
###############################################################
#def solution(N):
#    """Determines the maximal 'binary gap' in an integer.
#
#    :param N: [int] A positive integer (between 1 and maxint).
#    :return: [int] The length of the longest sequence of zeros in the binary representation of the integer.
#
#    Convert the int to a string of 0/1 chars.
#    Loop through the chars in the string.
#    When we see a zero, start the gap counter.
#    When we see a one, compare with the biggest gap, and save the bigger; reset the gap counter.
#    When we run out of characters, return the biggest gap.
#    """
#    # Convert the number to a string containing '0' and '1' chars.
#    binary_string = str(bin(N))[2:]
#
#    gap = max_gap = 0
#    for char in binary_string:
#        if char == "0":
#            gap += 1
#        else:
#            max_gap = max(gap, max_gap)
#            gap = 0
#
#    return max_gap


class TestGap:
    """A pytest class to test solution()"""

    @staticmethod
    def generate_scenarios():
        """contruct a dictionary used as parameterized inputs"""
        list_ = {
                9: 2,
                529: 4,
                20: 1,
                15: 0,
                32: 0,
                1041: 5,
                1: 0,
                5: 1,
                6: 0,
                328: 2,
                11: 1,
                19: 2,
                42: 1,
                1162: 3,
                51712: 2,
                561892: 3,
                66561: 9,
                6291457: 20,
                74901729: 4,
                805306369: 27,
                1376796946: 5,
                1073741825: 29,
                1610612737: 28,
                }

        for key, value in list_.items():
            yield key, value


    @parameterized.expand(generate_scenarios())
    def test_solution(self, key, value):
        """test solution using pytest"""
        assert solution(key) == value
