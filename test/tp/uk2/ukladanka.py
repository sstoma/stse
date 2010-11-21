class Puzzle:
    
    plansza = [[0,0,0],[0,0,0],[0,0,0]] #inicjazlizowanie planszy
    
    wzor = [['1','2','3'],['4','5','6'],['7','8','*']] #wzorzec rozwiazania
    
    kierunek = 0
    
    p = [0, 0]
    
    def __init__(self):
        file = open('plansza.txt', 'r')
        for i in range(3):
            temp = file.readline()
            for j in range(3):
                self.plansza[i][j] = temp[j] #wypelnianie planszy z pliku
                if self.plansza[i][j] == '*':
                    self.p=[i, j] #ustawienie kursora
        file.close()

    def rysuj(self): #funkcja wyswietlajaca biezacy stan gry
        for i in range(3):
            print '%s%s%s'%(self.plansza[i][0],self.plansza[i][1],self.plansza[i][2])
        return
    
    def stan_gry(self): #wykrywanie konca gry
        koniec = True
        for i in range(3): 
            for j in range(3):
                if self.plansza[i][j] != self.wzor[i][j]:
                    koniec = False
        if koniec:
            return False
        else:
            return True

    def przesun(self, r): #obsluga przesuniec
        if (r==2 and self.p[0]!=2): #w dol
            self.plansza[self.p[0]][self.p[1]] = self.plansza[self.p[0]+1][self.p[1]]
            self.plansza[self.p[0]+1][self.p[1]] = '*'
            self.p[0] = self.p[0]+1
        elif (r==4 and self.p[1]!=0): #w lewo
            self.plansza[self.p[0]][self.p[1]] = self.plansza[self.p[0]][self.p[1]-1]
            self.plansza[self.p[0]][self.p[1]-1] = '*'
            self.p[1] = self.p[1]-1
        elif (r==6 and self.p[1]!=2): #w prawo
            self.plansza[self.p[0]][self.p[1]] = self.plansza[self.p[0]][self.p[1]+1]
            self.plansza[self.p[0]][self.p[1]+1] = '*'
            self.p[1] = self.p[1]+1
        elif (r==8 and self.p[0]!=0): #w gore
            self.plansza[self.p[0]][self.p[1]] = self.plansza[self.p[0]-1][self.p[1]]
            self.plansza[self.p[0]-1][self.p[1]] = '*'
            self.p[0] = self.p[0]-1
        else:
            print '\nWybierz poprawny kierunek!\n'
        return

    def graj(self): #gra
        self.rysuj()
        while(self.stan_gry()):
            self.kierunek = int(raw_input('Wybierz przesuniecie:\
            \n8 - w gore\n6 - w prawo\n4 - w lewo\n2 - w dol\
            \nwpisz:'))
            self.przesun(self.kierunek)
            self.rysuj()
        print "\nGratulacje! ;)"
        return

#init
graj = Puzzle()
graj.graj()