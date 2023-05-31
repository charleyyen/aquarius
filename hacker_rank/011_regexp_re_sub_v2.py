import re

# https://www.hackerrank.com/challenges/re-sub-regex-substitution/problem
# More Pythonic way!!!!

text = []
for _ in range(int(input())):
    text.append(input())
text = "\n".join(text)

text = re.sub(r"(?<= )([&]{2}|[|]{2})(?= )", lambda x: "and" if x.group() == "&&" else "or", text)
# the syntax (?<= ) is part of a regular expression pattern and is known as a positive lookbehind assertion.
# It is used to match a specific pattern only if it is preceded by another pattern.
# Here's how it works:
#    (?<= ) is a positive lookbehind assertion that matches a space character (" ") !!before!! the desired pattern.
#    It does not consume any characters during matching, meaning the space character itself is not included in
#    the final match.
#
# the syntax (?= ) is part of a regular expression pattern and is known as a positive lookahead assertion.
# It is used to match a specific pattern only if it is followed by another pattern.
# Here's how it works:
#    (?= ) is a positive lookahead assertion that matches a space character (" ") !!after!! the desired pattern.
#    It does not consume any characters during matching, meaning the space character itself is not included in
#    the final match.
print(text)

