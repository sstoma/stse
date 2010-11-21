#!/usr/bin/python -tt

#funkcja mistakePrinter sluzy do rysowania szubienicy gdy uzytkownik poda litere, ktora juz istnieje lub
#ktorej nie ma w hasle
def mistakePrinter(number):
    if number==1:
        print '######################'
        print '#                    #'
        print '#  1               \ #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                    #'
        print '######################'
    if number==2:
        print '######################'
        print '#                    #'
        print '#  2      ---------\ #'
        print '#         |        | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                    #'
        print '######################'
    if number==3:
        print '######################'
        print '#                    #'
        print '# 3       ---------\ #'
        print '#         |        | #'
        print '#       /---\      | #'
        print '#       |   |      | #'
        print '#       \---/      | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                    #'
        print '######################'
    if number==4:
        print '######################'
        print '#                    #'
        print '# 4       ---------\ #'
        print '#         |        | #'
        print '#       /---\      | #'
        print '#       |   |      | #'
        print '#       \---/      | #'
        print '#         |        | #'
        print '#         |        | #'
        print '#         |        | #'
        print '#         |        | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                    #'
        print '######################'
    if number==5:
        print '######################'
        print '#                    #'
        print '# 5       ---------\ #'
        print '#         |        | #'
        print '#       /---\      | #'
        print '#       |   |      | #'
        print '#       \---/      | #'
        print '#       --|--      | #'
        print '#      /  |  \     | #'
        print '#     /   |   \    | #'
        print '#         |        | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                  | #'
        print '#                    #'
        print '######################'
    if number==6:
        print '######################'
        print '#                    #'
        print '# 6       ---------\ #'
        print '#         |        | #'
        print '#       /---\      | #'
        print '#       |   |      | #'
        print '#       \---/      | #'
        print '#       --|--      | #'
        print '#      /  |  \     | #'
        print '#     /   |   \    | #'
        print '#         |        | #'
        print '#        / \       | #'
        print '#       /   \      | #'
        print '#      /     \     | #'
        print '#                  | #'
        print '#                  | #'
        print '#                    #'
        print '######################'
    if number==7:
        print '######################'
        print '#                    #'
        print '# 7       ---------\ #'
        print '#         |        | #'
        print '#       /---\      | #'
        print '#       |X X|      | #'
        print '#       \---/      | #'
        print '#       --|--      | #'
        print '#      /  |  \     | #'
        print '#     /   |   \    | #'
        print '#         |        | #'
        print '#        0U0       | #'
        print '#       / U \      | #'
        print '#      /  U  \     | #'
        print '#                  | #'
        print '#  !! HANGOVER !!  | #'
        print '#  !! GAMEOVER !!  | #'
        print '#                    #'
        print '######################'
    return

#funkcja puzzles zawiera hasla do odgadniecia, wraz z kategoriami
def puzzles(level):
    import random
    if level==1:
        questions=[('zwierzeta', 'pies'),
                   ('zwierzeta', 'kot'),
                   ('zwierzeta', 'sarna'),
                   ('zwierzeta', 'dzik'),
                   ('zwierzeta', 'borsuk'),
                   ('zwierzeta', 'byk'),
                   ('zwierzeta', 'tygrys'),
                   ('zwierzeta', 'lew'),
                   ('miasta', 'londyn'),
                   ('miasta', 'szczecin'),
                   ('miasta', 'berlin'),
                   ('miasta', 'praga'),
                   ('miasta', 'madryt'),
                   ('miasta', 'kielce'),
                   ('miasta', 'gdynia'),
                   ('miasta', 'rzym'),
                   ('miasta', 'moskwa'),
                   ('panstwa', 'rosja'),
                   ('panstwa', 'grecja'),
                   ('panstwa', 'kanada'),
                   ('panstwa', 'chiny'),
                   ('panstwa', 'gruzja'),
                   ('panstwa', 'meksyk'),
                   ('panstwa', 'chile'),
                   ('panstwa', 'japonia'),
                   ('imiona', 'tomasz'),
                   ('imiona', 'marek'),
                   ('imiona', 'jacek'),
                   ('imiona', 'dawid'),
                   ('imiona', 'marcin'),
                   ('imiona', 'anna'),
                   ('imiona', 'szymon')]
        number=random.randint(0,len(questions)-1)
    if level==2:
        questions=[('panstwa', 'tunezja'),
                   ('panstwa', 'hiszpania'),
                   ('panstwa', 'senegal'),
                   ('panstwa', 'australia'),
                   ('panstwa', 'wenezuela'),
                   ('panstwa', 'holandia'),
                   ('panstwa', 'mongolia'),
                   ('panstwa', 'boliwia'),
                   ('miasta', 'houston'),
                   ('miasta', 'dakar'),
                   ('miasta', 'sydney'),
                   ('miasta', 'barcelona'),
                   ('miasta', 'wellington'),
                   ('miasta', 'kingston'),
                   ('miasta', 'chicago'),
                   ('miasta', 'bydgoszcz'),
                   ('miasta', 'katowice'),
                   ('miasta', 'szanghaj'),
                   ('miasta', 'bogota'),
                   ('czynnosc', 'gotowanie'),
                   ('czynnosc', 'odkurzanie'),
                   ('czynnosc', 'prasowanie'),
                   ('zwierzeta', 'antylopa'),
                   ('zwierzeta', 'pantera'),
                   ('zwierzeta', 'orangutan'),
                   ('rzeka', 'loara'),
                   ('rzeka', 'odra'),
                   ('rzeka', 'warta'),
                   ('rzeka', 'missisipi'),
                   ('rzeka', 'missouri'),
                   ('rzeka', 'mekong'),
                   ('rzeka', 'jenisej'),
                   ('rzeka', 'indus'),
                   ('rzeka', 'parana'),
                   ('rzeka', 'amazonka'),
                   ('rzeka', 'tamiza')]
        number=random.randint(0,len(questions)-1)
    if level==3:
        questions=[('miasta', 'sao paulo'),
                   ('miasta', 'buenos aires'),
                   ('miasta', 'rio de janeiro'),
                   ('miasta', 'port elizabeth'),
                   ('miasta', 'trypolis'),
                   ('miasta', 'tunis'),
                   ('miasta', 'lizbona'),
                   ('miasta', 'liverpool'),
                   ('miasta', 'glasgow'),
                   ('miasta', 'sztokholm'),
                   ('miasta', 'johannesburg'),
                   ('miasta', 'bangkok'),
                   ('panstwa', 'burkina faso'),
                   ('panstwa', 'arabia saudyjska'),
                   ('panstwa', 'nowa zelandia'),
                   ('panstwa', 'portugalia'),
                   ('panstwa', 'norwegia'),
                   ('panstwa', 'dominikana'),
                   ('panstwa', 'argentyna'),
                   ('aktorki i aktorzy', 'cezary pazura'),
                   ('aktorki i aktorzy', 'patrick swayze'),
                   ('aktorki i aktorzy', 'sean connery'),
                   ('aktorki i aktorzy', 'mel gibson'),
                   ('aktorki i aktorzy', 'angelina jolie'),
                   ('wykonawcy', 'michael jackson'),
                   ('wykonawcy', 'justin timberlake'),
                   ('wykonawcy', 'eros ramazzotti'),
                   ('wykonawcy', 'justin bieber'),
                   ('wykonawcy', 'kylie minogue'),
                   ('wykonawcy', 'britney spears'),
                   ('wykonawcy', 'jennifer loper')]
        number=random.randint(0,len(questions)-1)
    if level==4:
        questions=[('miasta', 'police'),
                   ('miasta', 'gryfino'),
                   ('miasta', 'karaczi'),
                   ('miasta', 'bamako'),
                   ('miasta', 'rabat'),
                   ('miasta', 'monachium'),
                   ('miasta', 'valencia'),
                   ('miasta', 'lizbona'),
                   ('miasta', 'rejkjavik'),
                   ('miasta', 'canberra'),
                   ('miasta', 'tirana'),
                   ('miasta', 'sarajewo'),
                   ('miasta', 'bruksela'),
                   ('miasta', 'nairobi'),
                   ('panstwa', 'sierra leone'),
                   ('panstwa', 'trinidad i tobago'),
                   ('panstwa', 'chorwacja'),
                   ('panstwa', 'gwatemala'),
                   ('panstwa', 'honduras'),
                   ('panstwa', 'kazachstan'),
                   ('panstwa', 'kirgistan'),
                   ('panstwa', 'lesotho'),
                   ('panstwa', 'lichtenstein'),
                   ('panstwa', 'luksemburg'),
                   ('panstwa', 'mauretania'),
                   ('panstwa', 'san marino'),
                   ('czynnosc', 'grabienie'),
                   ('wykladowcy', 'leonard rozenberg'),
                   ('wykladowcy', 'imed el frey'),
                   ('wykladowcy', 'mariusz kapruziak'),
                   ('wykladowcy', 'mykhaylo fedorov'),
                   ('wykladowcy', 'dariusz burak'),
                   ('wykladowcy', 'krzysztof siedlicki'),
                   ('wykladowcy', 'krzysztof kraska'),
                   ('wykladowcy', 'maciej poliwoda'),
                   ('wykladowcy', 'wlodzimierz chocianowicz'),
                   ('wykladowcy', 'jerzy pejas')]
        number=random.randint(0,len(questions)-1)
    if level==5:
        questions=[('miasta', 'lidzbark'),
                   ('miasta', 'nowe warpno'),
                   ('miasta', 'lublin'),
                   ('miasta', 'nowy targ'),
                   ('miasta', 'caracas'),
                   ('miasta', 'montevideo'),
                   ('miasta', 'taszkent'),
                   ('miasta', 'lublana'),
                   ('miasta', 'waszyngton'),
                   ('panstwa', 'sierra leone'),
                   ('panstwa', 'wyspy marshala'),
                   ('panstwa', 'turkmenistan'),
                   ('panstwa', 'tanzania'),
                   ('panstwa', 'salwador'),
                   ('panstwa', 'sri lanka'),
                   ('panstwa', 'nikaragua'),
                   ('panstwa', 'zjednoczone emiraty arabskie'),
                   ('czynnosc', 'grabienie'),
                   ('wykladowcy', 'antoni wilinski'),
                   ('wykladowcy', 'alexandr tariov'),
                   ('wykladowcy', 'piotr dziurzanski'),
                   ('wykladowcy', 'krzysztof malecki'),
                   ('wykladowcy', 'witold mackow'),
                   ('wykladowcy', 'teresa podhorska'),
                   ('wykladowcy', 'pawel forczmanski'),
                   ('wykladowcy', 'radoslaw mantiuk'),
                   ('wykladowcy', 'natalia ratuszniak'),
                   ('wykladowcy', 'dariusz burak'),
                   ('wykladowcy', 'romualda lizak')]
        number=random.randint(0,len(questions)-1)
    if level==6:
        questions=[('miasta', 'port louis'),
                   ('miasta', 'ottawa'),
                   ('miasta', 'juande'),
                   ('znani polacy', 'mariusz pudzianowski'),
                   ('znani polacy', 'hubert urbanski'),
                   ('znani polacy', 'zygmunt chajzer'),
                   ('znani polacy', 'kamil durczok'),
                   ('znani polacy', 'lech walesa'),
                   ('znani polacy', 'adam malysz'),
                   ('znani polacy', 'miroslav klose'),
                   ('znani polacy', 'lukas podolski'),
                   ('znani polacy', 'emmanuel olisadebe'),
                   ('politycy', 'wladimir putin'),
                   ('politycy', 'borys jelcyn'),
                   ('politycy', 'donald tusk'),
                   ('politycy', 'bill clinton'),
                   ('politycy', 'barack obama'),
                   ('politycy', 'ryszard kalisz'),
                   ('politycy', 'andrzej lepper'),
                   ('politycy', 'jacek kurski'),
                   ('politycy', 'zbigniew ziobro'),
                   ('politycy', 'jan rokita'),
                   ('wykonawcy', 'anna maria jopek'),
                   ('wykonawcy', 'golec uorkiestra'),
                   ('wykonawcy', 'ich troje'),
                   ('wykonawcy', 'brathanki'),
                   ('wykonawcy', 'kelly family'),
                   ('wykonawcy', 'anita lipnicka'),
                   ('wykonawcy', 'marek grechuta'),
                   ('wykonawcy', 'maanam')]
        number=random.randint(0,len(questions)-1)
    if level==7:
        questions=[('miasta', 'thimphu'),
                   ('miasta', 'quito'),
                   ('miasta', 'kinszasa'),
                   ('miasta', 'naypyidaw'),
                   ('miasta', 'bandarsri begawan'),
                   ('miasta', 'wagabudu'),
                   ('znani polacy', 'radoslaw majdan'),
                   ('znani polacy', 'kuba wojewodzki'),
                   ('znani polacy', 'michal figurski'),
                   ('znani polacy', 'jola rutowicz'),
                   ('znani polacy', 'ojciec rydzyk'),
                   ('znani polacy', 'monika pyrek'),
                   ('politycy', 'roman giertych'),
                   ('politycy', 'angela merkel'),
                   ('politycy', 'tony blair'),
                   ('politycy', 'jacques chirac'),
                   ('politycy', 'nicolas sarkozy'),
                   ('politycy', 'silvio berlusconi'),
                   ('politycy', 'gerhard schroder'),
                   ('politycy', 'jerzy buzek'),
                   ('wykonawcy', 'stahursky'),
                   ('wykonawcy', 'george michael'),
                   ('wykonawcy', 'simply red'),
                   ('wykonawcy', 'piotr rubik'),
                   ('wykonawcy', 'krzysztof krawczyk'),
                   ('wykonawcy', 'andrea bocelli'),
                   ('wykonawcy', 'amy winehouse'),
                   ('wykonawcy', 'lady gaga'),
                   ('wykonawcy', 'justyna steczkowska'),
                   ('wykonawcy', 'maryla rodowicz')]
        number=random.randint(0,len(questions)-1)
    return questions[number]


#funkcja convertToList zamienia stringa (losowo pobrane haslo na wybranym levelu) na liste
#oraz wyswietla kategorie z jakiej pochodzi haslo
def convertToList(level):
    question=puzzles(level)
    print ''
    print 'KATEGORIA:', question[0]
    myList=[]
    for i in range(len(question[1])):
        myList.append(question[1][i])
    return myList

#funkcja playGame jest odpowiedzialna za przebieg gry

def playGame(myList):
    wordPrivate=myList #lista, ktora przechowuje niezmieniona postac hasla.
    wordPublic=[]      #lista wypelniona kreskami, w miejscach gdzie nie zostala odgadnieta litera
    wordPublic.extend(wordPrivate) #utworzenie niezaleznej kopii
    for i in range(len(wordPublic)): #petla w ktorej przygotowujemy odpowiednia postac hasla
        if wordPrivate[i]!=' ':
            wordPublic[i]='_'
        if wordPrivate[i]==wordPrivate[0]:
            wordPublic[i]=wordPrivate[0]
        if wordPrivate[i]==wordPrivate[len(wordPublic)-1]:
            wordPublic[i]=wordPrivate[len(wordPublic)-1]
    wordPublic[0]=wordPrivate[0]
    wordPublic[len(wordPublic)-1]=wordPrivate[len(wordPublic)-1]
    mistakes=0 #licznik bledow
    points=0    #flaga, zmienna pomocnicza, ktora uzyskuje wartosc 1 w przypadku, gdy uzytkownik rozwiaze haslo
    givenChars=[] #lista przechowujaca wszystkie znaki, ktore podal uzytkownik podczas jednej gry
    while True:   #petla gry
        print ''
        toPrint=' '.join(str(n) for n in wordPublic) #wyswietla haslo bez [ ]
        print toPrint
        char=raw_input('PODAJ ZNAK: ') #pobieranie znaku z klawiatury
        flagGood=0    #flaga, zmienna pomocnicza, ktora przyjumje wartosc 1 gdy uzytkownik poda litere, ktora jest poprawna i nie byla wczesniej podana
        flagRepeat=0  #flaga, zmienna pomocnicza, ktora przyjumje wartosc 1 gdy uzytkownik poda litere, ktora podal juz wczesnij
        for j in range(len(wordPrivate)): #petla poszukujaca podanego znaku w hasle
            if wordPrivate[j]==char:    #warunek sprawdza czy znak znajduje sie w hasle
                for k in range(len(givenChars)): #petla sprawdza podany znak, nie jest juz zapisany w hasle
                    if givenChars[k]==char: 
                        flagRepeat=1
                if (char==wordPrivate[0]) or (char==wordPrivate[len(wordPublic)-1]): #warunek sprawdza, czy podany znak nie jest pierwsza lub ostatnia litera hasla
                    flagRepeat=1
                if flagRepeat==0:
                    wordPublic[j]=wordPrivate[j] #jesli powyzsze warunki zostaly spelnione przypisuje znak
                    flagGood=1
        givenChars.append(char) #dodaje podany znak do tablicy "podanych znakow" :P
        if char=='3': #warunek sprawdza czy chcemy opuscic gre, natychmiastowo
            break
        if flagGood==0:  
            mistakes=mistakes+1 #jesli znak byl bledny, zwiekszamy liczbe blendych prob
            if mistakes==7:     #jesli liczba blednych prob jest rowna 7, konczymy gre ze skutkiem smiertelnym
                toPrint=''.join(str(n) for n in wordPrivate)
                print ''
                print 'ROZWIAZANIE: '+toPrint #drukuje rozwiazanie na ekran
                print ''
            mistakePrinter(mistakes)
            if mistakes==7:
                break
        if wordPrivate==wordPublic: #jesli warunek jest spelniony, wygralismy
            print ''
            print 'GRATULACJE!'
            toPrint=''.join(str(n) for n in wordPublic)
            print 'ROZWIAZANIE: '+toPrint
            points=1
            break
    return points

def initialize(level): #funkcja, ktora inicjalizuje gre na konkretnym poziomie
    myList=convertToList(level)
    points=playGame(myList)
    return points
    
def main():

    print '###################'
    print '#                 #'
    print '#   TOMASZ IDZI   #'
    print '#  MAREK STREICH  #'
    print '#  HANGOVER v1.0  #'
    print '#                 #'
    print '###################'

    points=1
    while True: #petla obslugujaca interfejs gry
        print ''
        if points==1:
            print 'START GAME '+str(points)+'/7: [1]'
            print '          HELP: [2]'
            print '          EXIT: [3]'
        if (points>1) and (points<8):
            print 'PLAY LEVEL '+str(points)+'/7: [1]'
            print '          HELP: [2]'
            print '          EXIT: [3]'
        if points>=8:
            print 'GRATULACJE! GRA UKONCZONA.'
            print 'WCISNIJ PRZYCISK "3" ABY KONTYNUOWAC.'
        choice=raw_input('')
        if choice=='1':
            if points>7:
                points=points-1
            points=points+initialize(points)
        if choice=='2':
            print ''
            print '1. MENU'
            print 'Aby ropoczac nowa gre, wpisz "1" i zatwierdz Enterem.'
            print 'Aby wyswietlic pomoc, wpisz "2" i zatwierdz Enterem.'
            print 'Aby wyjsc z gry, wpisz "3" i zatwierdz Enter.'
            print ''
            print '2. CEL GRY'
            print 'Celem gry jest odgadniecie ukrytych hasel,'
            print 'na siedmiu roznch poiomach zaawansowania.'
            print ''
            print '3. ZASADY GRY'
            print 'Dla ulatwienia odkryta zostala pierwsza oraz ostatnia'
            print 'litera hasla, a takze wszystkie ich powtorzenia.'
            print 'Rowniez dla ulatwienia podane zostaja kategorie pytan.'
            print 'Haslo wypelniamy wpisujac pojedyncze litery.'
            print 'Jesli wpisana litera znajduje sie w hasle,'
            print 'wowczas zostaje ona odkryta. Jesli litera nie znajduje'
            print 'sie w hasle, wowczas wyswietlana jest tzw. "skucha".'
            print '"Skucha" nastepuje takze w dwoch innych przypadkach:'
            print '- podana zostala litera, ktora jest juz odkryta.'
            print '- podano litere, ktora zostala podana wczesniej.'
            print 'W trakcie gry mozna sie pomylic maksymalnie szesc razy.'
            print 'Hasla nie zawieraja polskich liter oraz liczb.'
            print ''
            print '4. OBSLUGA'
            print 'W oknie dialogowym nalezy podawac pojedyncze litery.'
            print 'W kazdej chwili mozna opuscic gre, poprzez wcisniecie'
            print 'klawisza "3".'
            print ''
            print '5. GRA'
            print 'Autorami gry sa Marek Streich oraz Tomasz Idzi.'
            print 'Gra zostala utworzona na poczatku listopada 2010.'
            print 'Wiemy, co oznacza angielskie slowo "Hangover",'
            print 'jego uzycie nie wynika z braku znajomosci jezyka.'
            
        if choice=='3':
            break    

if __name__ == '__main__':
  main()
