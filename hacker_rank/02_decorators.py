"""
https://www.hackerrank.com/challenges/decorators-2-name-directory/problem

Let's use decorators to build a name directory! You are given some
information about N people. Each person has a first name, last name, age
and sex. Print their names in a specific format sorted by their age in
ascending order i.e. the youngest person's name should be printed first.
For two people of the same age, print them in the order of their input.

For Henry Davids, the output should be:
Mr. Henry Davids

For Mary George, the output should be:
Ms. Mary George

Input Format

The first line contains the integer N, the number of people.

N lines follow each containing the space separated values of the first
name, last name, age and sex, respectively.

Constraints: 1 <= N <= 10

Output Format:
Output N names on separate lines in the format described above in ascending
order of age.

Sample Input

3
Mike Thomson 20 M
Robert Bustle 32 M
Andria Bustle 30 F

Sample Output

Mr. Mike Thomson
Ms. Andria Bustle
Mr. Robert Bustle

Concept

For sorting a nested list based on some parameter, you can use the
itemgetter library. You can read more about it at this site:
http://stackoverflow.com/questions/409370/sorting-and-grouping-nested-lists-in-python?answertab=votes#tab-top
"""
import operator # This line is given by the hackerrank, but it's not used.

def person_lister(f):
    def inner(people):
        # If we did not cast x[2] into INT in the next line, it'd pass first 7 tests but fail
        # the last 3 tests. Why? Why not fail all tests? It does not make sense!!
        people.sort(key=lambda x: int(x[2]))
        #data = sorted(people, key=lambda person: int(person[2])) # another way to sort
        sorted_people = []
        for person in people:
            sorted_people.append(f(person))
        
        return sorted_people

    return inner


@person_lister
def name_format(person):
    return ("Mr. " if person[3] == "M" else "Ms. ") + person[0] + " " + person[1]


def read_inputs(string_):
    people = []
    temp = string_.split("\n")
    for i, e in enumerate(temp, start=1):
        if len(e) > 0 and not e.strip().isdigit():
            people.append(e.split())

    return people
    
if __name__ == '__main__':
    # In reality, uncomment the following 2 lines and comment out the rest
    #people = [input().split() for i in range(int(input()))]
    #print(*name_format(people), sep='\n')

#    people = [['Mike', 'Thomson', '20', 'M'], ['Robert', 'Bustle', '32', 'M'], ['Andria', 'Bustle', '30', 'F']]
#    people = [['Laura', 'Moser', '52', 'F'], ['Ted', 'Moser', '50', 'M'], ['Yena', 'Dixit', '50', 'F'], ['Diya', 'Mirza', '50', 'F'], ['Rex', 'Dsouza', '49', 'M']]
    string_ = \
"""
10
Jake Jake 42 M
Jake Kevin 57 M
Jake Michael 91 M
Kevin Jake 2 M
Kevin Kevin 44 M
Kevin Michael 100 M
Michael Jake 4 M
Michael Kevin 36 M
Michael Michael 15 M
Micheal Micheal 6 M
"""
    people = read_inputs(string_)
    print(*name_format(people), sep='\n')

