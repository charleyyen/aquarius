"""
# GenomicRangeQuery

Find the minimal nucleotide from a range of sequence DNA.

## Problem Description

A DNA sequence can be represented as a string consisting of the letters A, C, G and T, which
correspond to the types of successive nucleotides in the sequence. Each nucleotide has an _impact
factor_, which is an integer. Nucleotides of types A, C, G and T have impact factors of 1, 2, 3 and 4,
respectively. You are going to answer several queries of the form: What is the minimal impact factor of
nucleotides contained in a particular part of the given DNA sequence?

The DNA sequence is given as a non-empty string S = S[0]S[1]...S[N-1] consisting of N characters.
There are M queries, which are given in non-empty arrays P and Q, each consisting of M integers. The
K-th query (0 ≤ K < M) requires you to find the minimal impact factor of nucleotides contained in the
DNA sequence between positions P[K] and Q[K] (inclusive).

For example, consider string S = CAGCCTA and arrays P, Q such that:
    P[0] = 2    Q[0] = 4
    P[1] = 5    Q[1] = 5
    P[2] = 0    Q[2] = 6

The answers to these M = 3 queries are as follows:

        The part of the DNA between positions 2 and 4 contains nucleotides G and C (twice),
        whose impact factors are 3 and 2 respectively, so the answer is 2.

        The part between positions 5 and 5 contains a single nucleotide T, whose impact factor
        is 4, so the answer is 4.

        The part between positions 0 and 6 (the whole string) contains all nucleotides, in
        particular nucleotide A whose impact factor is 1, so the answer is 1.

Write a function:

    def solution(S, P, Q)

that, given a non-empty string S consisting of N characters and two non-empty arrays P and Q
consisting of M integers, returns an array consisting of M integers specifying the consecutive answers
to all queries.

Result array should be returned as an array of integers.

For example, given the string S = CAGCCTA and arrays P, Q such that:
    P[0] = 2    Q[0] = 4
    P[1] = 5    Q[1] = 5
    P[2] = 0    Q[2] = 6

the function should return the values [2, 4, 1], as explained above.

Write an efficient algorithm for the following assumptions:

        N is an integer within the range [1..100,000];
        M is an integer within the range [1..50,000];
        each element of arrays P and Q is an integer within the range [0..N - 1];
        P[K] ≤ Q[K], where 0 ≤ K < M;
        string S consists only of upper-case English letters A, C, G, T.

Copyright 2009–2022 by Codility Limited. All Rights Reserved.
Unauthorized copying, publication or disclosure prohibited.
---

## The problem

I find this descripton hard to digest.  In my own words they're saying:

We'll give you a string, and a list of slices (array indexes) for that string;
What is the "smallest" character in each slice. Change the character to a
known value (A=1, C=2, G=3, T=4) before returning it.

So, it's just a min-value problem, but with a lot of distracting words.
"Find the minimum value in these subsets of a sequence of values."

## The Solutions

The naive solution is to step though every query, pull out the sliced
sequence, sort the string, and the value we need is the first char;
convert it to its number; collect all the results. Done.

Note: the numerical values assigned to the characters, fortunately, sort in
the same order as their character values. We can sort for the
'smallest' character, before converting into their respective integers.

If you're happy with 62%, see the "slow_solution" below. O(N * M)
https://app.codility.com/demo/results/trainingWUE2T7-GUD/

So, how to speed things up?

The naive solution is revisiting slices of the input repeatedly.  If we collect
some metadata, we remove the need for re-visits.

Let's do a "pre-pass" of the sequence, collecting the data we need to answer the
queries quickly.  Enter the "prefix sum" concept...

For the "prefix sum", we step through the char sequence, keeping a count of the
characters we have seen to that point.  For "CAGCCTA" that looks like:

    A = [0,0,1,1,1,1,1,2]
    C = [0,1,1,1,2,3,3,3]
    G = [0,0,0,1,1,1,1,1]
    T = [0,0,0,0,0,0,1,1]

Now, when we can ask "Are there any 'C' types between index 1 and 3?" we can
lookup two values (1=1 & 3=1) in C for the answer (No), without looping over
the actual sequence.

See 'fast_solution'. Score 100/100. O(N+M).
https://codility.com/demo/results/trainingH6PA4P-5V7/
"""
import random
import string
from aquarius.libs import split_array

# maximum number of neucleotides in a sequence
MAX_N = 100000
# maximum number of queries
MAX_M = 50000

def create_impact_matrix():
    letters_used = string.ascii_uppercase + string.ascii_lowercase
    hash_ = {}
    list_ = []
    for i, e in enumerate(letters_used, start=1):
        hash_[e] = i
        list_.append((e, i))

    return hash_, list_

# impact factor of each neucleotide
IMPACT1 = {"A": 1, "C": 2, "G": 3, "T": 4}
def solution_1(S, P, Q):
    # Task Score 62% Correctness 100% Performance 0%

    # almost_all_same_letters GGGGGG..??..GGGGGG..??..GGGGGG
    # TIMEOUT ERROR Killed. Hard limit reached: 7.000 sec.
    # large_random large random string, length
    # TIMEOUT ERROR Killed. Hard limit reached: 7.000 sec.
    # extreme_large all max ranges
    # TIMEOUT ERROR Killed. Hard limit reached: 7.000 sec.

    answers = []
    for i in range(len(P)):
        substring = S[P[i]:Q[i]+1]
        answers.append(IMPACT1[sorted(substring)[0]])

    return answers

IMPACT2 = {"A": 1, "C": 2, "G": 3, "T": 4}
def solution_2(S, P, Q): # The same as the above
    # Task Score 62% Correctness 100% Performance 0%
    answers = []
    for i in range(len(P)):
        unique_substring = ''.join(set(S[P[i]:Q[i]+1]))
        answers.append(IMPACT2[sorted(unique_substring)[0]])

    return answers

#IMPACT3 = {"A": 1, "C": 2, "G": 3, "T": 4}
IMPACT3, nothing = create_impact_matrix()
def solution_3(S, P, Q):
    # Score 100%, which is a surpise.
    # Reason: IMPACT3 is a dictionary so the keys are not sorted.
    answers = []
    for i in range(len(P)):
        substring = S[P[i]:Q[i]+1]
        for x, y in IMPACT3.items():
            if x in substring:
                answers.append(y)
                break

    return answers

#IMPACT4 = [("A", 1), ("C", 2), ("G", 3), ("T", 4)]
nothing, IMPACT4 = create_impact_matrix()
def solution_4(S, P, Q):
    # Score 100%, which is NOT a surpise. However, IMPACT4 as a list is actually manually sorted,
    # which is not an ideal way to implement.
    answers = []
    for i in range(len(P)):
        substring = S[P[i]:Q[i]+1]
        for x in IMPACT4:
            if x[0] in substring:
                answers.append(x[1])
                break

    return answers

#IMPACT5 = {"A": 1, "C": 2, "G": 3, "T": 4}
IMPACT5, nothing = create_impact_matrix()
def solution_5(S, P, Q):
    # Score 100%. This version sorts IMPACT5 before looping through it, which could slow down
    # the performance a bit. But it should guarantee the result is correct
    answers = []
    for i in range(len(P)):
        substring = S[P[i]:Q[i]+1]
        for k in sorted(IMPACT5.keys()):
            if k in substring:
                answers.append(IMPACT5[k])
                break

    return answers

if __name__ == '__main__':
    import time
    import numpy as np

    #create_impact_matrix()
    #exit()
    summary = {}

    #MAX_N = MAX_M = 11 

    string_used = string.ascii_uppercase + string.ascii_lowercase
    print(string_used)
    list_ = list(string_used)
    random.shuffle(list_)
    string_used = ''.join(list_)
    print(string_used)

    #S = split_array.create_random_alphabet_string(letters_used='ACGT', size=MAX_N)
    S = split_array.create_random_alphabet_string(letters_used=string_used, size=MAX_N)
    P, Q = split_array.create_a_pair_of_random_array(low=0, high=len(S), size=MAX_M)

    print(f'S length: {len(S)}, P/Q length: {len(P)}')

    if len(S) < 10:
        print(f'S length: {len(S)}, S: {S}')
    else:
        print(f'S length: {len(S)}, S[:5]: {S[:5]}, S[-5:]: {S[-5:]}')
    if len(P) < 10:
        print(f'P length: {len(P)}, P: {P}')
        print(f'Q length: {len(Q)}, Q: {Q}')
    else:
        print(f'P length: {len(P)}, P[:5]: {P[:5]}, P[-5:]: {P[-5:]}')
        print(f'Q length: {len(Q)}, Q[:5]: {Q[:5]}, Q[-5:]: {Q[-5:]}')

    print()
    for j, solution in enumerate([solution_3, solution_4, solution_5], start=1):
        method = str(solution).split()[1]
        start = time.time()
        answer = solution(S, P, Q)
        elapsed = round(time.time() - start, 4)
        summary[j] = (method, answer, elapsed)
        if len(answer) < 10:
            print(f'==-->>j: {j}, {summary[j][0]} - {summary[j][2]}, #{summary[j][1]}#')
        else:
            print(f'==-->>j: {j}, {summary[j][0]} - {summary[j][2]}, First 5: {summary[j][1][:5]}, Last 5: {summary[j][1][-5:]}')

    print()
    arr0 = np.array(summary[1][1])
    if len(arr0) < 10:
        print(f'==>>1, arr0 length: {len(arr0)}, #{arr0}')
    else:
        print(f'==>>1, arr0 length: {len(arr0)}, First 5: {arr0[:5]}, Last 5: {arr0[-5:]}')
    for j in (2, 3):
        arr = np.array(summary[j][1])
        if len(arr0) < 10:
            print(f'-->>{j}, arr  length: {len(arr)}, #{arr}')
        else:
            print(f'-->>{j}, arr  length: {len(arr)}, First 5: {arr[:5]}, Last 5: {arr[-5:]}')
        assert np.array_equal(arr0, arr)

    set0 = set(arr0)
    int_ = random.randint(len(arr0)//10, len(arr0))
    print(f'int_: {int_}, length: {len(set0)}, set0: {set0}')
    print(f'section at {int_}: {arr0[int_:int_+100]}')
#    P = [2,5,0]
#    Q = [4,5,6]
#    S = 'CAGCCTA'
#    findings = solution(S, P, Q)
#    print(f'findings: {findings}')

