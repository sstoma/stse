#!/usr/bin/env python

resztyFileHandle = open('reszty.txt', 'r')
resztyStringList = resztyFileHandle.readlines()
kwotyFileHandle = open('kwoty.txt', 'r')
kwotyStringList = kwotyFileHandle.readlines()
nominaly = [ 25, 10, 5, 2, 1]

i = 0
for line in resztyStringList:
    resztyStringList[i] = line.replace(' ', '')
    i += 1

i = 0
for line in resztyStringList:
    resztyStringList[i] = line.replace('\n', '')
    i += 1

i = 0
for line in kwotyStringList:
    kwotyStringList[i] = line.replace('\n', '')
    i += 1

j = 0
for line in resztyStringList:
    answer, i = 0, 0
    for char in line:
        answer += int(char)*nominaly[i]
        i += 1
    if answer == int(kwotyStringList[j]):
        print 'TAK! Kwota oczekiwana: '+kwotyStringList[j]+', kwota otrzymana z reszty.txt: '+str(answer)
    else:
        print 'NIE! Kwota oczekiwana: '+kwotyStringList[j]+', kwota otrzymana z reszty.txt: '+str(answer)
    j += 1
    