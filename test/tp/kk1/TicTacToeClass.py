class TicTacToe:
   __count = 1       # liczba krokow
   __turn = 0	     #kolej gracza
   __table = 0	     #plansza
   __flag = 0        #flaga do sprawdzenia czy gra zakonczona
   __copy = '-'
   
   
   
   def __init__(self, firstPlayer):
      self.__turn = firstPlayer
      self.__table = [0]*3
      for x in range(len(self.__table)):
         self.__table[x]=[0]*3  
      pass
   
      
   def reset(self, firstPlayer):		#umozliwia ponowne rozpoczecie gry
      self.__flag = 0
      self.__turn = firstPlayer
      self.__count = 1
      self.__table = [0]*3
      for x in range(len(self.__table)):
         self.__table[x]=[0]*3
      pass
      
   def set(self,x,y):				#wstawia element w zaznaczone m-ce ( o ile to mozliwe)
      if self.__flag == 1:			#sprawdza czy jest juz zwyciezca, jak jest nie wstawia nowego elementu
         return 2
      if x > 3 or x < 0 or y > 3 or y < 0:      #sprawdza czy nie przekroczono zakresu
         return None
      if self.__table[x-1][y-1] == 0:           #wstawia element
         self.__table[x-1][y-1] = self.__turn
         return 1
      else:										#sprawdza tez czy cos juzjest w danym m-cu
         return 0
      pass
  
   def nextStep(self):				#ustawia kolejnego gracza i zwieksza liczbe krokow
      if self.__turn == 1:
         self.__turn = 2
      else:
         self.__turn = 1
                 
      self.__count += 1
      return self.__turn
      pass

   def show(self):
    #  wyswietla plansze
      self.__copy = ['-']*3
      for x in range(3):
         self.__copy[x]=['-']*3
         
      print self.__copy[1][2]   
      
      for i in range(3):
         for j in range(3):
            if self.__table[i][j]==1: 
              self.__copy[i][j]='o'
            elif self.__table[i][j]==2: 
                self.__copy[i][j]='x'
                        
      print "\n"
      print "      [1] [2] [3]"
      print "     -------------"
      print   " [1] | " + self.__copy[0][0] + " | " + self.__copy[0][1] + " | " + self.__copy[0][2] + " | "
      print "\n [2] | " + self.__copy[1][0] + " | " + self.__copy[1][1] + " | " + self.__copy[1][2] + " | "
      print "\n [3] | " + self.__copy[2][0] + " | " + self.__copy[2][1] + " | " + self.__copy[2][2] + " | "
      print "     -------------"
      print "\n"
      pass
   
   def check(self):			#sprawdza wyniki gry
      if ( self.__count < 5 ):          #jesli l. krokow jest < od 5 to nie ma co jeszcze sprawdzac
         return 0
      
      countOne = 0
      countTwo = 0 
      for i in range(3):	        #sprawdza w poziomie
         for j in range(3):
            if self.__table[i][j] == 1:
               countOne += 1
            elif self.__table[i][j] == 2: 
               countTwo += 1
         if countOne == 3:
            self.__flag = 1             #jesli jest juz wynik to ustawia flage
            return 1
         elif countTwo == 3:
            self.__flag = 1
            return 2
         else:
            countOne = 0
            countTwo = 0	           
      
      for i in range(3):	        #w pionie
         for j in range(3):
            if self.__table[j][i] == 1:
               countOne += 1
            elif self.__table[j][i] == 2:
               countTwo += 1
         if countOne == 3:
            self.__flag = 1
            return 1
         elif countTwo == 3:
            self.__flag = 1
            return 2
         else:
            countOne = 0
            countTwo = 0
      j = 0
      for i in range(3):	        #w skosie z gory w dol
         if self.__table[i][j] == 1:
            countOne += 1
         elif self.__table[i][j] == 2:
            countTwo += 1
         j += 1
      
      if countOne == 3:
         self.__flag = 1
         return 1
      elif countTwo == 3:
         self.__flag = 1
         return 2

      countOne = 0
      countTwo = 0
      j = 2
      
      for i in range(3):               #w skosie z dolu w gore
         if self.__table[i][j] == 1:
            countOne += 1
         elif self.__table[i][j] == 2:
            countTwo += 1
         j -= 1
      
      if countOne == 3:
         self.__flag = 1
         return 1
      elif countTwo == 3:
         self.__flag = 1
         return 2

      if self.__count == 9:       #gdy remis
         self.__flag = 1
         return None

      return 0                    #gdy gra nie zakonczona
   pass