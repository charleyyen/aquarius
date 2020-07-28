#! /usr/bin/python

import re

myfile = "/home/cyan/temp/notes4W3schools.txt"
f = open(myfile, "r")
contents = f.readlines()

str2append = "Here comes another newly appended line."
i = 1
for line in contents:
    length = len(line)
    newLine = line.strip('\n')
    newLen1 = len(newLine)
    if(newLen1 == 0):
        continue
    if(re.search("import", line)):
        print (i, "#"+newLine+"#")
        newLine = newLine+". "+str2append
        print ("===--->>>"+str(i), newLine)
    else:
        print(i, newLine)
    i += 1

f.close()
