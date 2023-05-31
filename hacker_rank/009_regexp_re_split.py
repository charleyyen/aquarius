"""
https://www.hackerrank.com/challenges/re-split/problem?isFullScreen=true
"""
import re

regex_pattern = r"[.,\s]+"

print("\n".join(re.split(regex_pattern, input())))
