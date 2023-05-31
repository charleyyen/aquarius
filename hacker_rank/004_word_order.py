"""
https://www.hackerrank.com/challenges/word-order/problem?isFullScreen=true
"""
#import os

def get_word_order(word_list):
    word_hash = {}
    for word in word_list:
        if word not in word_hash.keys():
            word_hash[word] = 1
        else:
            word_hash[word] += 1

    print(len(word_hash))
    for k, v in word_hash.items():
        print(v, end=' ')
    print()

if __name__ == '__main__':
    """
    https://www.hackerrank.com/challenges/word-order/problem?isFullScreen=true
    Sample inputs:
    4
    bcdef
    abcdefg
    bcde
    bcdef
    """
    """
    n = int(input())
    word_list = []
    for i in range(n):
        word_list.append(input().strip())

    print(f'n: {n}, word_list length: {len(word_list)}')
    print(f'word_list:\n{word_list}')
    """
    word_list = ['bcdef', 'abcdefg', 'bcde', 'bcdef']
    get_word_order(word_list)

