#-------------------------------------------
#			Gra warcaby
#	Daniel Kraszewski i Piotr Drews
#			  I1-32/B
#-------------------------------------------


import sys

kolory = ['bialy', 'czarny']
figury = ['B', 'C']

class pionek:
	rodzaj = -1
	
	def __init__(self, typ):
		self.rodzaj = typ
	
	def figura(self):
		return figury[self.rodzaj]


class plansza:
	pionki = [[None]*5 for i in xrange(5)]
	ilosc = [3, 3]
	
	def __init__(self):
		self.pionki[0][0] = pionek(1)
		self.pionki[0][2] = pionek(1)
		self.pionki[0][4] = pionek(1)
		
		self.pionki[4][0] = pionek(0)
		self.pionki[4][2] = pionek(0)
		self.pionki[4][4] = pionek(0)
	
	def wyswietl(self):
		a = 5
		for i in self.pionki:
			sys.stdout.write(str(a) + '  ')
			a -= 1
			for j in i:
				if j is None:
					sys.stdout.write('+')
				else:
					sys.stdout.write(j.figura())
				sys.stdout.write(' ')
			sys.stdout.write('\n')
		sys.stdout.write('\n   A B C D E\n')

def main():
	gra = plansza()
	gracz = 0
	
	print 'Witaj!'
	print 'Rozpoczynamy rozgrywke, aby wykonac ruch wprowadz dane w formacie \nA1B2 gdzie A1 to pozycja pionka, B2 to docelowa pozycja.\n'
	
	while gra.ilosc[0] > 0 and gra.ilosc[1] > 0:
		gra.wyswietl()
		while True:
			dane = raw_input('\n[' + kolory[gracz] + '] Wprowadz swoj ruch: ').lower()
			if len(dane) is not 4:
				print 'Bledne dane!'
			elif dane[0] < 'a' or dane[0] > 'e' or dane[2] < 'a' or dane[2] > 'e' or dane[1] < '1' or dane[1] > '5' or dane[3] < '1' or dane[3] > '5':
				# ten warunek mozna by zamienic na test wyrazenia regularnego
				print 'Bledne dane!'
			else:
				xp = ord(dane[0]) - ord('a')
				yp = 4 - (int(dane[1]) - 1)
				xc = ord(dane[2]) - ord('a')
				yc = 4 - (int(dane[3]) - 1)
				#print str(yp) + ', ' + str(xp)
				roznicax = abs(xp - xc)
				roznicay = abs(yp - yc)
				
				if gra.pionki[yp][xp] is None:
					print 'W pozycji ' + dane[0:2] + ' nie ma pionka!'
				elif gra.pionki[yp][xp].rodzaj is not gracz:
					print 'To nie twoj pionek ;)'
				elif gra.pionki[yc][xc] is not None:
					print 'Miejsce do wykonania ruchu jest zajete!'
				elif roznicax is not 1 or roznicay is not 1:
					if roznicax is 2 and roznicay is 2:
						xz = (xp + xc) / 2;
						yz = (yp + yc) / 2;
						gra.pionki[yz][xz] = None;
						
						if gracz is 0:
							gra.ilosc[1] -= 1
							gracz = 1
						else:
							gra.ilosc[0] -= 1
							gracz = 0
						
						gra.pionki[yc][xc] = gra.pionki[yp][xp];
						gra.pionki[yp][xp] = None;
						sys.stdout.write('\n')
						break;
						
					else:
						print 'Nie mozna wykonac tego ruchu!'
				else:
					gra.pionki[yc][xc] = gra.pionki[yp][xp];
					gra.pionki[yp][xp] = None;
					sys.stdout.write('\n')
					
					if gracz is 0:
						gracz = 1
					else:
						gracz = 0
					break;
					
	gra.wyswietl()
	sys.stdout.write('\n')
	
	if gra.ilosc[0] <= 0:
		print 'Zwyciezyly czarne!'
	elif gra.ilosc[1] <= 0:
		print 'Zwyciezyly biale!'
	else:
		print 'Remis lub blad ;)'


if __name__ == '__main__':
	main()