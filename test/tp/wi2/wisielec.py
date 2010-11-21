import re, os, traceback, random
from random import randint

class Wczytywaczka(object):
    def __init__(self, plik):
        self.__dane = self.__wczytaj(plik)
            
    def __wczytaj(self, plik):
        try:
            file = open(plik, 'r')
            hasla = file.readlines()
            file.close()
        except:
            print "Podano nieprawidlowa nazwe pliku z haslami"
        return hasla
        
    def losuj(self):
        nr_hasla = randint(0, len(self.__dane)-1)
        return self.__dane[nr_hasla]
    
class Wisielec(object):
    def __init__(self, plik):
        self.__wczytywaczka = Wczytywaczka(plik)
        self.__start()
    
    def __start(self):
        quit = False
        while not quit:
            haslo = self.__wczytywaczka.losuj()
            haslo = re.sub('[^a-z^A-Z]+', '', haslo).lower()
            self.__graj(haslo)
            koniec = None
            while not koniec in ['t','n']:
                koniec = raw_input('Czy chcesz grac dalej? (t/n)')
                if koniec == 'n':
                    quit = True
            
    
    def __graj(self, haslo):
        trafione = {}
        nietrafione = []
        rysownik = Rysownik(haslo)
        wygrana = None
        while wygrana == None:
            literka = raw_input('Podaj litere: ')
            wynik = self.__sprawdzLitere(haslo, literka, trafione, nietrafione)
            if wynik == None:
                rysownik.zle()
            elif wynik[1] == True:
                rysownik.dobrze(wynik[0])
            else:
                print 'Uzyles juz litery %s, wybierz inna' % wynik[0]
                continue
            wygrana = self.__sprawdzStan(trafione, nietrafione, haslo)
        if wygrana == True:
            print 'Brawo, wygrales!'
        else:
            print 'Niestety, przegrales!, rozwiazanie to: %s' % haslo
       
    def __sprawdzLitere(self, haslo, litera, trafione, nietrafione):
        if re.search(litera, haslo) and litera not in trafione.iterkeys() and litera not in nietrafione:
            trafione[litera] = len(re.findall(litera, haslo))
            return (litera,True)
        elif litera in trafione or litera in nietrafione:
            return (litera,False)
        else:
            nietrafione.append(litera)
            return None
    
    def __sprawdzStan(self, trafione, nietrafione, haslo):
        trafienia = 0
        for i in trafione.itervalues():
            trafienia += i
        if trafienia == len(haslo):
            return True
        if len(nietrafione) > 5:
            return False
        return None
     
class Rysownik(object):
    def __init__(self, haslo):
        self.__haslo = haslo
        self.__przygotujSzubienice()
        self.__szubienicaLicznik = 0
        wyraz = '_'
        for i in range(0,len(haslo)-1):
            wyraz += ' _'
        self.__wyraz = wyraz
        self.__rysuj()
    
    def __przygotujSzubienice(self):
        self.__szubienica = []
        self.__szubienica.append(' ------\n |    |\n |\n |\n |\n_|_')
        self.__szubienica.append(' ------\n |    |\n |    o\n |\n |\n_|_')
        self.__szubienica.append(' ------\n |    |\n |    o\n |    |\n |\n_|_')
        self.__szubienica.append(' ------\n |    |\n |    o\n |   /|\n |\n_|_')
        self.__szubienica.append(' ------\n |    |\n |    o\n |   /|\\\n |\n_|_')
        self.__szubienica.append(' ------\n |    |\n |    o\n |   /|\\\n |   /\n_|_')
        self.__szubienica.append(' ------\n |    |\n |    o\n |   /|\\\n |   / \\\n_|_')
    
    def zle(self):
        self.__szubienicaLicznik += 1
        self.__rysuj()
    
    def dobrze(self, litera):
        wyraz = self.__wyraz.split(' ')
        haslo = re.findall('.', self.__haslo)
        indeksy = []
        for i in range(0,len(haslo)):
            if str(litera) == str(haslo[i]):
                indeksy.append(i)
        for indeks in indeksy:
            wyraz[indeks] = litera
        self.__wyraz = ''
        for i in range(0,len(wyraz)):
            self.__wyraz += wyraz[i]
            if i < len(wyraz)-1:
                self.__wyraz += ' '
        self.__rysuj()
                
    def __rysuj(self):
        self.__clearscreen()
        print self.__szubienica[self.__szubienicaLicznik] + '\n\n' + self.__wyraz
    
    def __clearscreen(self,linijek=100):
        if os.name == "posix":
            os.system('clear')
        elif os.name in ("nt", "dos", "ce"):
            os.system('CLS')
        else:
            print '\n' * linijek
    
    
if __name__ == '__main__':
    klasa = Wisielec('slowa.txt')