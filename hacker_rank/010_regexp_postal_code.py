#! /usr/bin/python

# https://www.hackerrank.com/challenges/validating-postalcode/problem?isFullScreen=true
# https://www.hackerrank.com/challenges/validating-postalcode/problem?h_r=next-challenge&h_v=zen&h_r=next-challenge&h_v=zen

import re

# To match only integers range from 100000 to 999999 inclusive. All 4 lines are equally Ok.
#regex_integer_in_range = r"^([1-9][0-9][0-9][0-9][0-9][0-9]|9[0-9][0-9][0-9][0-9][0-9])$"
#regex_integer_in_range = r"^([1-8]\d{5}|9\d{5})$"
#regex_integer_in_range = r"^([1-9]\d{5}|9\d{5})$"
regex_integer_in_range = r"^([1-9]\d{5})$"

#The next line is to find alternating repetitive digits pairs in a given string.
# Ref: 
# 1) https://stackoverflow.com/questions/49325509/how-to-find-alternating-repetitive-digit-pair
# 2) https://regex101.com/r/JpdXdl/2
regex_alternating_repetitive_digit_pair = r"(\d)(?=\d\1)"	# Do not delete 'r'.


import re
P = input()

print (bool(re.match(regex_integer_in_range, P))
and len(re.findall(regex_alternating_repetitive_digit_pair, P)) < 2)
