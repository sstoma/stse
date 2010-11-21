def wczytaj_dane(plik):
    """ funkcja wczytujaca dane z pliku 'plik' do tablicy """
    i=0
    zmienna={}
    file=open(plik)                         #otworz plik
    string=file.readline()                  #wczytywanie znaku
    while string:
        zmienna[i]=int(string)              #konwersja string na int
        i=i+1
        string=file.readline()
    file.close()                            #zamkniecie pliku
    return zmienna                          #zwrucenie do programu tablicy
    
def zapisz_dane(plik,dane):
    i=0
    file=open(plik,'a')
    try:
    	int(dane[0])
    except ValueError:
    	file.write(dane)
    else:
    	for i in range(len(dane)):
			file.write(str(dane[i])+' ')
    file.write('\n')
    file.close()
    
# Funkcja wydajaca reszte
# @param integer kwota, jest to kwota, ktora nalezy wydac
# @param array kasa, tablica z dostepnymi monetami

def wydawaj(kwota, kasa):
	reszty = [0, 0, 0, 0, 0]
	kasa_temp = kasa
	flaga = 1
	while kwota > 0 and flaga > 0:
		if kasa[0] > 0 and kwota >= 25:
			kwota = kwota - 25
			kasa[0] = kasa[0] - 1
			reszty[0] = reszty[0] + 1
		elif kasa[1] > 0 and kwota >= 10:
			kwota = kwota - 10
			kasa[1] = kasa[1] - 1
			reszty[1] = reszty[1] + 1
		elif kasa[2] > 0 and kwota >= 5:
			kwota = kwota - 5
			kasa[2] = kasa[2] - 1
			reszty[2] = reszty[2] + 1
		elif kasa[3] > 0 and kwota >= 2:
			kwota = kwota - 2
			kasa[3] = kasa[3] - 1
			reszty[3] = reszty[3] + 1
		elif kasa[4] > 0 and kwota >= 1:
			kwota = kwota - 1
			kasa[4] = kasa[4] - 1
			reszty[4] = reszty[4] + 1
		else:
			flaga = 0
	if flaga > 0:
		zapisz_dane("reszty.txt", reszty)
	else:
		kasa = kasa_temp
		reszty = 'NIE'
		zapisz_dane("reszty.txt", reszty)


if __name__ == "__main__":
    import sys
    plik="kwoty.txt"
    kwoty = wczytaj_dane(plik)
    kasa = wczytaj_dane("kasa.txt")
    i = 0
    	
    file=open('reszty.txt','w')
    file.write('')
    file.close()
    	
    for i in kwoty:
	wydawaj(kwoty[i], kasa)