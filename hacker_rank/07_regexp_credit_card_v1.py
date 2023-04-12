"""
https://www.hackerrank.com/challenges/validating-credit-card-number/problem?isFullScreen=true
Better solutions:
    https://www.hackerrank.com/challenges/validating-credit-card-number/forum
    https://www.golinuxcloud.com/validating-credit-card-numbers-python/
"""
import re
def is_valid(number):
    if '-' in number:
        temp = number.split('-')
        if len(temp) != 4:
            print('Invalid')
        else:
            for x in temp:
                if len(x) != 4 or not x.isdigit():
                    print('Invalid')
                    break
            else:
                candidate = ''.join(temp)
                final_verification(candidate)

    else:
        if not number.isdigit():
            print('Invalid')
        else:
            if len(number) != 16:
                print('Invalid')
            elif not number.startswith('4') and not number.startswith('5') and not number.startswith('6'):
                print('Invalid')
            else:
                final_verification(number)

def final_verification(number):
    matches = [x[0] for x in re.findall(r'((.)\2+)', number)]
    if len(matches) > 0:
        for x in matches:
            if len(x) > 3:
                print('Invalid')
                return

    print('Valid')

def main():
    flag = 1
    if flag:
        n = int(input())
        for i in range(n):
            number = input()
            is_valid(number)

    else:
        number_list = [
            '4123456789123456',
            '5123-4567-8912-3456',
            '61234-567-8912-3456',
            '4123356789123456',
            '5133-3367-8912-3456',
            '5123 - 3567 - 8912 - 3456',
            '7165863385679329',
            '6175824393389297',
            '5252248277877418',
            '9563584181869815',
            '5179123424576876',
        ]
        for number in number_list:
            is_valid(number)


if __name__ == '__main__':
    """
    https://www.hackerrank.com/challenges/validating-credit-card-number/problem?isFullScreen=true
    Sample Input
    6
    4123456789123456
    5123-4567-8912-3456
    61234-567-8912-3456
    4123356789123456
    5133-3367-8912-3456
    5123 - 3567 - 8912 - 3456

    Sample Output
    Valid
    Valid
    Invalid
    Valid
    Invalid
    Invalid
    """
    main()
