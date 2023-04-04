"""
https://www.hackerrank.com/challenges/re-start-re-end/problem?isFullScreen=true

Task
You are given a string S.
Your task is to find the indices of the start and end of string k in S.

Input Format

The first line contains the string S.
The second line contains the string k.

Constraints:
    0 < len(S) < 100
    0 < len(k) < len(S)

Output Format

Print the tuple in this format: (start_index, end_index).
If no match is found, print (-1, -1).

Sample Input:

aaadaa
aa

Sample Output

(0, 1)
(1, 2)
(4, 5)
"""
S = input()
k = input()

array_ = []
for i in range(len(S)):
    if S[i:].startswith(k):
        array_.append((i, i+len(k)-1))

if array_:
    for e in array_:
        print(e)
else:
    print((-1, -1))

