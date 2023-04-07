from datetime import datetime
import os

def time_delta(t1, t2):
    x = datetime.strptime(t1,"%a %d %b %Y %H:%M:%S %z")
    y = datetime.strptime(t2,"%a %d %b %Y %H:%M:%S %z")

    return str(int(abs((x-y).total_seconds())))

if __name__ == '__main__':
    """
    https://www.hackerrank.com/challenges/python-time-delta/problem?isFullScreen=true
    Sample inputs:
    2
    Sun 10 May 2015 13:54:36 -0700
    Sun 10 May 2015 13:54:36 -0000
    Sat 02 May 2015 19:54:36 +0530
    Fri 01 May 2015 13:54:36 -0000
    """
    t1 = "Sun 10 May 2016 13:54:36 -0700"
    t2 = "Sun 10 Feb 2016 13:54:36 -0000"
    delta = time_delta(t1, t2)
    print(f'delta: {delta}')
    #fptr = open(os.environ['OUTPUT_PATH'], 'w')
    #t = int(input())
    #for t_itr in range(t):
    #    t1 = input()
    #    t2 = input()
    #    delta = time_delta(t1, t2)
    #    fptr.write(delta + '\n')

    #fptr.close()
