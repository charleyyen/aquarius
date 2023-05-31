#! /usr/bin/python

# https://www.hackerrank.com/challenges/matrix-script/problem?h_r=next-challenge&h_v=zen&h_r=next-challenge&h_v=zen&h_r=next-challenge&h_v=zen
# this implementation is copied from the discussion area in the link above
import re

n = int(input())
for _ in range(n):
    s = input().strip()
#    print("-----------------")
    print(bool(re.match(("^[+?|\-?]?\d*\.\d+$"), s)))

print("\n")

