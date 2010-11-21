class RestGiving:
    '''wydawanie reszt algorytmem zachlannym'''

    reszty=[]  #zwracana lista reszt
    nominaly=[25, 10, 5, 2, 1]
    
    def __init__(self, kwoty_do_wydania, stan_kasy):
        self.kwoty=kwoty_do_wydania  # przypisania do list prywatnych
        self.kasa=stan_kasy

    def giveRest(self):
        for i in range(len(self.kwoty)):    # dla kazdej kwoty wykonujemy operacje
            pozostalo=self.kwoty[i]
            do_wydania=[0, 0, 0, 0, 0]         #pojedynczy ciag reszt 
            for j in range(5):                  #dla kazdego nominalu
                while self.kasa[j]-do_wydania[j]>0 and pozostalo>=self.nominaly[j]:
                    pozostalo -= int(self.nominaly[j])
                    do_wydania[j]+=1
                    
            if pozostalo==0:
                tempstr=""
                for k in range(5):
                    self.kasa[k]-=do_wydania[k]
                    tempstr = tempstr + `do_wydania[k]` + ' '   #generowanie ciagu reszt
                self.reszty.append(tempstr)
            else:
                self.reszty.append('  NIE  ')
        return self.reszty, self.kasa
