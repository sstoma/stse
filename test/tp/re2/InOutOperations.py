#!/usr/bin/env python

class InOutOperations:
    
    def readAllLines(self, fileName):
        try:
            fileHandle = open(fileName, 'r')
            stringList = fileHandle.readlines()
            i = 0
            for line in stringList:
                stringList[i] = int(line.replace('\n', ''))
                i += 1
            fileHandle.close()
            return stringList
        except IOError:
            print 'Nie mozna otworzyc podanego pliku'
    
    def writeLinesToFile(self, fileName, stringList):
        try:
            fileHandle = open(fileName, 'w')
            counter = 0
            for line in stringList:
                if counter == len(stringList)-1:
                    fileHandle.write(str(line))
                else:
                    fileHandle.write(str(line)+'\n')
                counter+=1
            fileHandle.close()
        except IOError:
            print 'Nie mozna zapisac do podanego pliku'
            
