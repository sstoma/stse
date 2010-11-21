# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os, random, TicTacToeClass

clear = lambda: os.system('cls')

def zaznacz( x, y ):															#ta f-cja jest wywolywana przez gracza podczas gry
   isNotSet = game.set(x,y)														#wstawienie elementu w wybrane m-ce ( o ile mozliwe)
   clear()
   print "\nAby wykonac ruch wpisz 'zaznacz( wiersz, kolumna )' "
   game.show()
   if isNotSet == 2:														    #sprawdzenie rezultatu wstawienia- przypadek,gdy gra zostala juz zakonczona
     print "\nGra zostala zakonczona. Aby zagrac jeszcze raz wpisz 'reset()'"
   elif isNotSet == 1:															#wstawienie by³o mo¿liwe
      check = game.check()																#sprawdzenie wyniku gry
      if check == 0:																	#gdy brak jeszcze wyniku
         player = game.nextStep()                                                       
         print "Teraz kolej gracza: " + str(player)										
      elif check == 1:                                                                  #gdy wygral gracz 1
         print "Wygral gracz 1 napisz 'reset()' aby zagrac jeszcze raz"
      elif check == 2:																	#gdy wygral gracz 2
         print "Wygral gracz 2 napisz 'reset()' aby zagrac jeszcze raz"
      else:
         print "Remis"																	#gdy remis
   elif isNotSet == 0 :															#wstawienie nie by³o mozliwe, z powodu zajêtego juz pola
      print "Pole juz zaznaczone! Sproboj ponownie :)"
   else:																	    #wstawienie nie by³o mozliwe, z powodu wykroczenia poza plansze
      print "Wprowadzany index wykracza poza plansze"
   pass


   
def reset():                                                                   #umozliwia rozpoczecie gry od nowa
    clear()
    print "\nAby wykonac ruch wpisz 'zaznacz( wiersz, kolumna )'"
    first = random.randint(1, 2)
    game.reset(first)
    game.show()
    print "Teraz kolej gracza: " + str(first)
    pass

clear()

print '''

Witamy w grze kolko i krzyzyk!

Pola planszy oznaczne sa wspolrzednymi od 1 do 3 w wierszach i kolumnach.

Gracz 1 = kolko = 'o'

Gracz 2 = krzyzyk = 'x'

'''

print "Trwa losowanie ktory gracz rozpocznie...\n"
first = random.randint(1, 2)													#losowanie gracza zaczynaj¹cego
print '''Zaczyna gracz: ''' + str(first) + '''

Oto plansza:'''

game = TicTacToeClass.TicTacToe( first )
game.show()
print '''Aby wykonac ruch wpisz 'zaznacz( wiersz, kolumna )'

Teraz kolej gracza: ''' + str(first)








