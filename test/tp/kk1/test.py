# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os, random, TicTacToeClass

clear = lambda: os.system('cls')

def zaznacz( x, y ):
   isNotSet = game.set(x,y)  
   clear()
   print "\nAby wykonac ruch wpisz 'zaznacz( wiersz, kolumna )' "
   game.show()
   if isNotSet == 2:
     print "\nGra zostala zakonczona. Aby zagrac jeszcze raz wpisz 'reset()'"
   elif isNotSet == 1:
     check = game.check()
     if check == 0:
       player = game.nextStep()
       print "Teraz kolej gracza: " + str(player)
     elif check == 1:
       print "Wygral gracz 1 napisz 'reset()' aby zagrac jeszcze raz"
     elif check == 2:
       print "Wygral gracz 2 napisz 'reset()' aby zagrac jeszcze raz"
     else:
       print "Remis"
   elif isNotSet == 0 :
      print "Pole juz zaznaczone! Sproboj ponownie :)"
   else:
      print "Wprowadzany index wykracza poza plansze"
   pass


   
def reset():
    clear()
    game.__flag=0
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
first = random.randint(1, 2)
print '''Zaczyna gracz: ''' + str(first) + '''

Oto plansza:'''

game = TicTacToeClass.TicTacToe( first )
game.show()
print '''Aby wykonac ruch wpisz 'zaznacz( wiersz, kolumna )'

Teraz kolej gracza: ''' + str(first)


zaznacz(1,2)
zaznacz(2,1)
zaznacz(1,1)
zaznacz(2,2)
zaznacz(1,3)


raw_input('Wcisnij Enter, aby zaczac kolejny test.')
reset()

zaznacz(1,3)
zaznacz(2,2)
zaznacz(3,3)
zaznacz(1,1)
zaznacz(2,3)


raw_input('Wcisnij Enter, aby zaczac kolejny test.')
reset()

zaznacz(1,1)
zaznacz(2,1)
zaznacz(2,2)
zaznacz(1,3)
zaznacz(3,3)

raw_input('Wcisnij Enter, aby zaczac kolejny test.')
reset()

zaznacz(3,1)
zaznacz(2,3)
zaznacz(2,2)
zaznacz(2,1)
zaznacz(1,3)

raw_input('Wcisnij Enter, aby zaczac kolejny test.')
reset()

zaznacz(2,2)
zaznacz(1,3)
zaznacz(1,1)
zaznacz(3,3)
zaznacz(2,3)
zaznacz(2,1)
zaznacz(3,2)
zaznacz(1,2)
zaznacz(3,1)

raw_input('Wcisnij Enter, aby zaczac kolejny test.')

reset()

zaznacz(2,2)
zaznacz(3,3)
zaznacz(3,1)
zaznacz(2,2)
zaznacz(3,2)
zaznacz(1,3)		
zaznacz(1,1)				#proba wstawienia nowego elementu do planszy po zakonczonej rozgrywce

raw_input('Wcisnij Enter, aby zaczac kolejny test.')
reset()

zaznacz(1,1)
zaznacz(1,2)
zaznacz(2,1)
zaznacz(2,2)
zaznacz(2,1)				#proba wstawienia elementu w pole juz zaznaczone

raw_input('Wcisnij Enter, aby zaczac kolejny test.')
reset()

zaznacz(3,1)
zaznacz(3,2)
zaznacz(2,2)
zaznacz(1,3)
zaznacz(4,5)              #proba przekroczenia indeksu planszy

raw_input('Wcisnij Enter, aby zaczac kolejny test.')
reset()

print "\n Teraz zapraszam Ciebie do testowania gry."