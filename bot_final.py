import random
import bisect
import sys

class Bot:
    def __init__(self):
        self.plansza=[[0]*10 for i in range(10)] #0 gdy pole nieodkryte -1 gdy pudlo -2 gdy trafiony
        self.statki_bota=[[0]*10 for i in range(10)]  #0 woda w p.p. kazde pole zawiera dlugosc statku 
        self.pozostale_statki=[0, 4, 3, 2, 1, 0] # indeks to dlugosc, wartosc to liczba pozostalych statkow o danej dlugosci
        self.statek=[] #posortowane wspolrzedne trafionych pol konkretnego statku, ktory nalezy dobic
        self.ktory=0
        self.trafione_pola=0 #ile zatopionych pol
        self.sprawdz_obok_x=[1,-1,0,0]
        self.sprawdz_obok_y=[0,0,1,-1]
        
    def reset(self):
        self.plansza=[[0]*10 for i in range(10)] 
        self.statki_bota=[[0]*10 for i in range(10)] 
        self.pozostale_statki=[0, 4, 3, 2, 1, 0]
        self.statek=[]
        self.ktory=0
        self.trafione_pola=0
        self.ustaw_statki()
        
    def mozna_ustawic(self, x, y, poziomy, dlugosc):
        if poziomy:
            if y+dlugosc>9: return 0
            for i in range (-1, dlugosc+1):
                if -1<y+i<10:
                    if self.statki_bota[x][y+i]: return 0
                    if x+1<10:
                        if self.statki_bota[x+1][y+i]: return 0
                    if x-1>-1:
                        if self.statki_bota[x-1][y+i]: return 0    
        else:
            if x+dlugosc>9: return 0
            for i in range (-1, dlugosc+1):
                if -1<x+i<10:
                    if self.statki_bota[x+i][y]: return 0
                    if y+1<10:
                        if self.statki_bota[x+i][y+1]: return 0
                    if y-1>-1:
                        if self.statki_bota[x+i][y-1]: return 0    
        return 1

    def ustaw_statki(self):
        statki_do_ustawienia=[4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        for i in range (10):
            mozna=0
            poziomy=0
            x_pocz=0
            y_pocz=0
            while not mozna:
                x_pocz=random.randint(0, 9)
                y_pocz=random.randint(0, 9)
                poziomy=random.randint(0, 1)
                mozna=self.mozna_ustawic(x_pocz, y_pocz, poziomy, statki_do_ustawienia[i]) 
            for j in range (statki_do_ustawienia[i]):
                if poziomy:
                    self.statki_bota[x_pocz][y_pocz+j]=statki_do_ustawienia[i]
                else:
                    self.statki_bota[x_pocz+j][y_pocz]=statki_do_ustawienia[i]

    def zaktualizuj_pozostale_pola(self):
        pozostale=[]
        szachownica=self.czy_zostaly_statki(2)
        for i in range (10):
            for j in range (10):
                if self.plansza[i][j]==0:
                    if szachownica:
                        if not (i+j)%2:
                            pozostale.append((i,j))
                    else:
                        pozostale.append((i,j))   
        if not pozostale: # na wszelki wypadek chociaz to raczej niemozliwe
            for i in range (10):
                for j in range (10):
                    if self.plansza[i][j]==0:
                        pozostale.append((i,j))
        return pozostale

    def czy_zostaly_statki(self, od): #czy sa jeszcze jakies statki dluzsze lub rowne od
        for i in range (od, 6):
            if(self.pozostale_statki[i]):
                return True
        return False  
        
    def zatop(self):
        x_pocz, y_pocz=self.statek[0]
        x_kon, y_kon=self.statek[-1]
        for i in range(x_pocz-1, x_kon+2):
            for j in range(y_pocz-1, y_kon+2):
                if -1<i<10 and -1<j<10:
                    if self.plansza[i][j]!=-2:
                        self.plansza[i][j]=-1

    def kontynuuj(self): #jesli trafiony strzelaj dalej
        if len(self.statek)==1:
            i,j=self.statek[0]
            while self.ktory<4:
                test_i=i+self.sprawdz_obok_x[self.ktory]
                test_j=j+self.sprawdz_obok_y[self.ktory] 
                self.ktory+=1
                if -1<test_i<10 and -1<test_j<10 and self.plansza[test_i][test_j]==0:
                    return test_i, test_j  
            return None, None
        else:
            x_pocz, y_pocz=self.statek[0]
            x_kon, y_kon=self.statek[-1]
            if x_pocz-x_kon==0:
                if y_pocz-1>-1 and self.plansza[x_pocz][y_pocz-1]==0:
                    return x_pocz, y_pocz-1
                elif y_kon+1<10 and self.plansza[x_pocz][y_kon+1]==0:
                    return x_pocz, y_kon+1
            elif y_pocz-y_kon==0:
                if x_pocz-1>-1 and self.plansza[x_pocz-1][y_pocz]==0:
                    return x_pocz-1, y_pocz
                elif x_kon+1<10 and self.plansza[x_kon+1][y_pocz]==0:
                    return x_kon+1, y_pocz
            return None, None

    def strzelaj(self):
        losowanie=self.zaktualizuj_pozostale_pola() #czy moze byc puste?
        i,j=(None, None)
        if self.statek:
            i,j=self.kontynuuj()
        if i is None: #jesli zamiast if wstawic else nie sprawdzalby czy kontynuuj zwrocilo none
            self.ktory=0
            self.statek=[]
            if not losowanie: 
                print('brak wolnych pol', file=sys.stderr)
                return None, None
            i,j=random.choice(losowanie)
        return i, j
            
            
    def zrob_cos_z_wynikami(self, trafiony, x, y): #trafiony powinno byc rowne dlugosci trafionego statku
        if not trafiony:
            self.plansza[x][y]=-1
        else:
            self.ktory=0
            self.trafione_pola+=1
            self.plansza[x][y]=-2
            bisect.insort(self.statek, (x, y))
            if len(self.statek)==trafiony or not self.czy_zostaly_statki(len(self.statek)+1):
                self.zatop()
                self.pozostale_statki[len(self.statek)]-=1
                self.statek=[]
                #print('trafiony zatopiony')
                
