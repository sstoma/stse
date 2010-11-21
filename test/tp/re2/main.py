#!/usr/bin/env python

from InOutOperations import InOutOperations
from RestGiving import RestGiving

#testowanie metod klasy 
#testObj = IOOperations('kasa.txt', 'reszty.txt')
#stringList = testObj.readAllLines()
#print testObj.readLine(1)
#print testObj.readLine(2)
#testObj.writeOutputFile(testObj.readAllLines())
#testObj.updateDataFile(['1','2','3','4','5'])
#testObj.closeFiles()

inOutObj = InOutOperations()
restObj = RestGiving(inOutObj.readAllLines('kwoty.txt'), inOutObj.readAllLines('kasa.txt'))
restList, statusList = restObj.giveRest()
#restList = ['0','1','2','3']
inOutObj.writeLinesToFile('reszty.txt', restList)
inOutObj.writeLinesToFile('kasa.txt', statusList)
#kwotylista = [37, 2, 10, 59]  # te listy pobierz z pliku, ja wpisalem na sztywno
#kasalista = [10, 10, 4, 5, 10]


#nowyobj = RestGiving(kwotylista, kasalista) # tutaj je uzyj jako parametry
#wynik=nowyobj.giveRest() # a to juz mozna zapisac do pliku
#print wynik
