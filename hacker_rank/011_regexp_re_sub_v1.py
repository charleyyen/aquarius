import re

# https://www.hackerrank.com/challenges/re-sub-regex-substitution/problem

def convert(line):
    line = re.sub(r"(?<= )&&(?= )", " and ", line)
    line = re.sub(r"(?<= )\|\|(?= )", " or ", line)
    return line


if __name__ == '__main__':
    n = input()
    list_ = []
    for i in range(int(n)):
        raw_line = input()
        line = raw_line.strip()
        if len(line) > 0 and line.strip()[0] != '#' \
                and line.strip()[0] != "&" and line.strip()[0] != "\|" \
                and line.strip()[-1] != "&" and line.strip()[-1] != "\|":
            line = convert(raw_line)
            list_.append(line)
        else:
            list_.append(raw_line)

    #print(f'{"*"*50}')
    for l in list_:
        print(l)

"""
Input:
10
x  && &   &x
x&|&&|&| ||x
x| |&&|  &&x
x& &   &| &x
x& &&&&||| x
x&|&  |    x
x &  & |&&&x
x|&|& &    x
x & &|| &||x
x |&|&&|&||x

Output:
x  and &   &x
x&|&&|&| ||x
x| |&&|  &&x
x& &   &| &x
x& &&&&||| x
x&|&  |    x
x &  & |&&&x
x|&|& &    x
x & &|| &||x
x |&|&&|&||x
"""
