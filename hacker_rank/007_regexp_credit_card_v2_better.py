#! /usr/bin/python

# https://www.hackerrank.com/challenges/validating-credit-card-number/problem?h_r=next-challenge&h_v=zen

#import string
'''
    has_2_or_more_upper = bool(re.search(r'[A-Z]{2,}', uid))
    has_3_or_more_digits = bool(re.search(r'\d{3,}', uid))
    has_10_proper_elements = bool(re.search(r'^[a-zA-Z0-9]{10}$', uid))
    no_repeats = not bool(re.search(r'(.)\1', uid))

► It must start with a 4,5, or 6.
► It must contain exactly 16 digits.
► It must only consist of digits (0-9).
► It may have digits in groups of 4, separated by one hyphen "-".
► It must NOT use any other separator like ' ' , '_', etc.
► It must NOT have 4 or more consecutive repeated digits.
'''

import re

def isValid(uid):
    startWith456 = bool(re.search(r'^[4-6]', uid))
    #print (f'startWith456: {startWith456}')
#    exact16WithHyphen = bool(re.search(r'(^\d{4,}\-){3,}\d{4,}$', uid))
    exact16WithHyphen = bool(re.search(r'^\d{4,}\-\d{4,}\-\d{4,}\-\d{4,}$', uid))
    #print (f'exact16WithHyphen: {exact16WithHyphen}')
    exact16 = bool(re.search(r'^\d{16,}$', uid))
    #print (f'exact16: {exact16}')

    len16or19 = len(uid)

    x = uid.replace('-', "")
    no_repeats = not bool(re.search(r'(.)\1\1\1', x))
    #print (f'no_repeats: {no_repeats}')


    if startWith456 and (exact16WithHyphen or exact16) and no_repeats and (len16or19 == 16 or len16or19 == 19):
#    if startWith456 and exact16 and (len16or19 == 16 or len16or19 == 19):
#    if startWith456 and (exact16WithHyphen or exact16) and (len16or19 == 16 or len16or19 == 19):
        return "Valid"
    return "Invalid"

if __name__ == '__main__':
    k = int(input())
    for _ in range(k):
        str =  input().strip()
        print(isValid(str))

