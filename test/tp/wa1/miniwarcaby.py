################################################
# PROJEKT ZESPOLOWY 2010/2011
# SEMESTR V
# GRA: MINI WARCABY
# AUTORZY: PIOTR JANKUN, PAWEL KOPOCINSKI
# GRUPA 0815
################################################


# ZMIENNE GLOBALNE
plansza=[['B','#','B','#','B'],['#','#','#','#','#'],['#','#','#','#','#'],['#','#','#','#','#'],['C','#','C','#','C']]
piony = [3,3]  # piony[0] => biale, piony[1] => czarne

# DEFINICJE UZYWANYCH FUNKCJI
# funkcja drukujaca plansze wedlug aktualnego stanu
def drukowaniePlanszy():
    print "    a b c d e\n   "
    for i in range(5):
        tempstr=''
        for j in range(5):
            tempstr=tempstr+plansza[i][j]+' '
        print i+1,' ',tempstr
		

# funkcja przeliczajaca wprowadzone wspolrzedne z notacji szachownicy na macierzowa
def obliczWsp(pozC,pozL):
    if pozL=='a':   #wspolrzedne
               X=0
    elif pozL=='b':
               X=1
    elif pozL=='c':
               X=2
    elif pozL=='d':
               X=3
    elif pozL=='e':
               X=4
    Y=int(pozC)-1
    return Y,X
	
# funkcja opisujaca ruch bialego piona
def ruchBialego():
	mozliwosciBicia = sprawdzBicieBialym()		# sprawdzenie czy jest bicie
	if mozliwosciBicia != 0:
		print "[RUCH BIALEGO] Mozliwosci bicia: %d" % mozliwosciBicia
		wlasciwyPion = 0
		while wlasciwyPion == 0:
			PozycjaPrzed = raw_input("Wybierz pionka, ktory bedzie bil: ")
			X,Y = obliczWsp(PozycjaPrzed[1],PozycjaPrzed[0])
           
			if plansza[X][Y] == 'B' and (plansza[X+1][Y-1] == 'C' or plansza[X+1][Y+1] == 'C') and (plansza[X+2][Y-2] == '#' or plansza[X+2][Y+2] == '#'):	# sprawdzenie czy podany pion moze byc bijacym
				wlasciwyPion = 1
			else:
				print "Zle pole, podaj jeszcze raz."
				wlasciwyPion = 0
		
		poprawnyRuch = 0
		while poprawnyRuch == 0:
			PozycjaPo = raw_input("Podaj pole na ktore chcesz przesunac pionek, by zbic przeciwnika: ")
			X2,Y2 = obliczWsp(PozycjaPo[1],PozycjaPo[0])

			if (X2>=0 and X2<6 and Y2>=0 and Y2<6) and (X == X2-2) and (Y == Y2+2) and (plansza[X2][Y2]=='#') and (plansza[X2-1][Y2+1] == 'C'):  # bicie w lewo
				plansza[X][Y] = '#'
				plansza[X2][Y2] = 'B'
				plansza[X2-1][Y2+1] = '#'
				poprawnyRuch = 1 
			elif (X2>=0 and X2<6 and Y2>=0 and Y2<6) and (X == X2-2) and (Y == Y2-2) and (plansza[X2][Y2]=='#') and (plansza[X2-1][Y2-1] == 'C'): # bicie w prawo
				plansza[X][Y] = '#'
				plansza[X2][Y2] = 'B'
				plansza[X2-1][Y2-1] = '#'
				poprawnyRuch = 1
			else:
				print "Zle pole!!"
				poprawnyRuch = 0
			piony[1] -= 1
		
	else:
		wlasciwyPion = 0
		while wlasciwyPion == 0:
			PozycjaPrzed = raw_input("[RUCH BIALEGO] Wybierz pionka ktorego chcesz przesunac: ")
			X,Y = obliczWsp(PozycjaPrzed[1],PozycjaPrzed[0])
           
			if plansza[X][Y] != 'B':		# sprawdzenie poprawnosci wyboru piona
				print "Zle pole, podaj jeszcze raz."
				wlasciwyPion = 0
			else:
				wlasciwyPion = 1
	
		poprawnyRuch = 0
		while poprawnyRuch == 0:
			PozycjaPo = raw_input("Podaj pole na ktore chcesz przesunac pionek: ")
			X2,Y2 = obliczWsp(PozycjaPo[1],PozycjaPo[0])
			if (X2>=0 and X2<6 and Y2>=0 and Y2<6) and (plansza[X2][Y2]=='#') and (X2==X+1 and (Y2==Y+1 or Y2==Y-1)):	# sprawdzenie czy mozna na dane pole piona przesunac
				plansza[X][Y] = '#'
				plansza[X2][Y2] = 'B'
				poprawnyRuch = 1
			else:
				print "Zle pole!!"
				poprawnyRuch = 0
	drukowaniePlanszy()
	return 'C'
	
	
# funkcja opisujaca ruch czarnego piona
def ruchCzarnego():
	mozliwosciBicia = sprawdzBicieCzarnym()		# sprawdzenie czy jest bicie
	if mozliwosciBicia != 0:
		print "[RUCH CZARNEGO] Mozliwosci bicia: %d" % mozliwosciBicia
		
		wlasciwyPion = 0
		while wlasciwyPion == 0:
			PozycjaPrzed = raw_input("Wybierz pionka, ktory bedzie bil: ")
			X,Y = obliczWsp(PozycjaPrzed[1],PozycjaPrzed[0])
           
			if plansza[X][Y] == 'C' and (plansza[X-1][Y-1] == 'B' or plansza[X-1][Y+1] == 'B') and (plansza[X-2][Y-2] == '#' or plansza[X-2][Y+2] == '#'):  # sprawdzenie czy podany pion moze byc bijacym
				wlasciwyPion = 1
			else:
				print "Zle pole, podaj jeszcze raz."
				wlasciwyPion = 0
				
		poprawnyRuch = 0
		while poprawnyRuch == 0:
			PozycjaPo = raw_input("Podaj pole na ktore chcesz przesunac pionek, by zbic przeciwnika: ")
			X2,Y2 = obliczWsp(PozycjaPo[1],PozycjaPo[0])

			if (X2>=0 and X2<6 and Y2>=0 and Y2<6) and (X == X2+2) and (Y == Y2+2) and (plansza[X2][Y2]=='#') and (plansza[X2+1][Y2+1] == 'B'):  # bicie w lewo
				plansza[X][Y] = '#'
				plansza[X2][Y2] = 'C'
				plansza[X2+1][Y2+1] = '#'
				poprawnyRuch = 1
			elif (X2>=0 and X2<6 and Y2>=0 and Y2<6) and (X == X2+2) and (Y == Y2-2) and (plansza[X2][Y2]=='#') and (plansza[X2+1][Y2-1] == 'B'): # bicie w prawo
				plansza[X][Y] = '#'
				plansza[X2][Y2] = 'C'
				plansza[X2+1][Y2-1] = '#'
				poprawnyRuch = 1
			else:
				print "Zle pole!!"
				poprawnyRuch = 0
			
			piony[0] -= 1
		
	else:
		wlasciwyPion = 0
		while wlasciwyPion == 0:
			PozycjaPrzed = raw_input("[RUCH CZARNEGO] Wybierz pionka ktorego chcesz przesunac: ")
			X,Y = obliczWsp(PozycjaPrzed[1],PozycjaPrzed[0])
           
			if plansza[X][Y]!='C':		# sprawdzenie poprawnosci wyboru piona
				print "Zle pole, podaj jeszcze raz."
				wlasciwyPion = 0
			else:
				wlasciwyPion = 1
        
		poprawnyRuch = 0
		while poprawnyRuch == 0:
			PozycjaPo = raw_input("Podaj pole na ktore chcesz przesunac pionek: ")
			X2,Y2 = obliczWsp(PozycjaPo[1],PozycjaPo[0])
			if (X2>=0 and X2<6 and Y2>=0 and Y2<6) and (plansza[X2][Y2]=='#') and (X2==X-1 and (Y2==Y-1 or Y2==Y+1)):	# sprawdzenie czy mozna na dane pole piona przesunac
				plansza[X][Y] = '#'
				plansza[X2][Y2] = 'C'
				poprawnyRuch = 1
			else:
				print "Zle pole!!"
				poprawnyRuch = 0
	drukowaniePlanszy()
	return 'B'
	
	
# funkcja sprawdzajaca czy bialy pion powinien bic
def sprawdzBicieBialym():
	mozliwosciBicia = 0
	for wiersz in range(5):			# przechodzenie szachownicy
		for kolumna in range(5):	
			if wiersz < 3 and plansza[wiersz][kolumna] == 'B':			# sprawdzamy mozliwosc bicia tylko do 3 wiersza bo dalej nie da rady bic
				if kolumna == 0 or kolumna == 1:	# ewentualne bicie mozliwe tylko w prawo
					if plansza[wiersz+1][kolumna+1] == 'C' and plansza[wiersz+2][kolumna+2] == '#':
						mozliwosciBicia += 1
				elif kolumna == 3 or kolumna == 4:	# ewentualne bicie mozliwe tylko w lewo
					if plansza[wiersz+1][kolumna-1] == 'C' and plansza[wiersz+2][kolumna-2] == '#':
						mozliwosciBicia += 1
				else:								# bicie ze srodka mozliwe w prawo i lewo
					if (plansza[wiersz+1][kolumna+1] == 'C' and plansza[wiersz+2][kolumna+2] == '#') or (plansza[wiersz+1][kolumna-1] == 'C' and plansza[wiersz+2][kolumna-2] == '#'):
						mozliwosciBicia += 1
	return mozliwosciBicia

	
# funkcja sprawdzajaca czy czarny pion powinien bic
def sprawdzBicieCzarnym():
	mozliwosciBicia = 0
	for wiersz in range(5):			# przechodzenie szachownicy
		for kolumna in range(5):
			if wiersz > 1 and plansza[wiersz][kolumna] == 'C':			# sprawdzamy mozliwosc bicia powyzej 1 wiersza bo dalej nie da rady bic
				if kolumna == 0 or kolumna == 1:	# ewentualne bicie mozliwe tylko w prawo
					if plansza[wiersz-1][kolumna+1] == 'B' and plansza[wiersz-2][kolumna+2] == '#':
						mozliwosciBicia += 1
				elif kolumna == 3 or kolumna == 4:	# ewentualne bicie mozliwe tylko w lewo
					if plansza[wiersz-1][kolumna-1] == 'B' and plansza[wiersz-2][kolumna-2] == '#':
						mozliwosciBicia += 1
				else:								# bicie ze srodka mozliwe w prawo i lewo
					if (plansza[wiersz-1][kolumna+1] == 'B' and plansza[wiersz-2][kolumna+2] == '#') or (plansza[wiersz-1][kolumna-1] == 'B' and plansza[wiersz-2][kolumna-2] == '#'):
						mozliwosciBicia += 1
	return mozliwosciBicia
						

# funkcja sprawdzajaca czy gra powinna toczyc sie dalej
def sprawdzKoniec():
	koniecB = 0
	koniecC = 0
	
	if piony[0] == 0 or piony[1] == 0:
		return 0
	else:
		for i in range(5):
			if plansza[4][i] == 'B':
				koniecB += 1
				if koniecB == piony[0]:
					return 0
			elif plansza[0][i] == 'C':
				koniecC += 1
				if koniecC == piony[1]:
					return 0
			else:
				return 1

		
		
		
		
# glowna funkcja programu
def main():
	drukowaniePlanszy()
	czyjRuch='B'
	gramyDalej = 1
	
	while gramyDalej:
		if czyjRuch == 'B':
			czyjRuch = ruchBialego()
		else:
			czyjRuch = ruchCzarnego()
		
		gramyDalej = sprawdzKoniec()
	
	if piony[0]	== 0:
		print "Wygral czarny"
	elif piony[1] == 0:
		print "Wygral bialy"	
	else:
		print "Remis"
	
	
	
if __name__ == '__main__':
  main()