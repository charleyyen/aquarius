"""
https://www.hackerrank.com/challenges/no-idea/problem?isFullScreen=true
"""
def summary():
    mode, love, hate = get_input()
    happiness = 0
    for x in mode:
        if x in love:
            happiness +=1
        if x in hate:
            happiness -=1
    print(happiness)

def get_input():
    line_1 = input().strip()
    line_2 = input().strip()
    line_3 = input().strip()
    line_4 = input().strip()
    mode = line_2.split(' ')
    # If w/o using set() in the following two lines, it'd throw timeout errors
    love = set(line_3.split(' '))
    hate = set(line_4.split(' '))
    return mode, love, hate

if __name__ == '__main__':
    summary()
