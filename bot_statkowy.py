import random
import bisect
original=[[0]*10 for i in range(10)]
class bot:
    def __init__(self):
        self.plansza=[[0]*10 for i in range(10)]
        self.statki_bota = [[0]*10 for _ in range(10)]
        self.pozostale_statki=[0, 4, 3, 2, 1, 0]
        self.statek=[]
        self.ktory=0
        self.trafione_pola=0
        self.sprawdz_obok_x=[1,-1,0,0]
        self.sprawdz_obok_y=[0,0,1,-1]
    def reset(self):
        self.__init__()

    def mozna_ustawic(self, x, y, poziomy, dlugosc):
        if poziomy:
            if y+dlugosc>9: return 0
            for i in range (-1, dlugosc+1):
                if y+i>-1 and y+i<10:
                    if self.statki_bota[x][y+i]: return 0
                    if x+1<10:
                        if self.statki_bota[x+1][y+i]: return 0
                    if x-1>-1:
                        if self.statki_bota[x-1][y+i]: return 0    
        else:
            if x+dlugosc>9: return 0
            for i in range (-1, dlugosc+1):
                if x+i>-1 and x+i<10:
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
        #szachownica=[]
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
        return pozostale

    def czy_zostaly_statki(self, od): #sprawdz czy jest sens dalej szukac reszty statku
        for i in range (od, 6):
            if(self.pozostale_statki[i]):
                return True
        return False  
        
    def zatop(self):
        x_pocz, y_pocz=self.statek[0]
        x_kon, y_kon=self.statek[-1]
        for i in range(x_pocz-1, x_kon+2):
            for j in range(y_pocz-1, y_kon+2):
                if i>-1 and i<10 and j>-1 and j<10:
                    if self.plansza[i][j]!=-2:
                        self.plansza[i][j]=-1

    def kontynuuj(self): #jesli trafiony strzelaj dalej
        if len(self.statek)==1:
            i,j=self.statek[0]
            while self.ktory<4:
                test_i=i+self.sprawdz_obok_x[self.ktory]
                test_j=j+self.sprawdz_obok_y[self.ktory] 
                self.ktory+=1
                if test_i>-1 and test_j>-1 and test_i<10 and test_j<10 and self.plansza[test_i][test_j]!=-1 and self.plansza[test_i][test_j]!=-2:
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
        losowanie=self.zaktualizuj_pozostale_pola()
        i,j=(None, None)
        if self.statek:
            i,j=self.kontynuuj()
        if i is None: #jesli zamiast if wstawic else nie sprawdzalby czy kontynuuj zwrocilo none
            self.ktory=0
            self.statek=[]
            i,j=random.choice(losowanie)
        if original[i][j]>0:
            self.ktory=0
            self.trafione_pola+=1
            if self.trafione_pola==20:
                #print('zwyciestwo')
                return 2
            self.plansza[i][j]=-2
            bisect.insort(self.statek, (i, j))
            if len(self.statek)==original[i][j]:
                self.zatop()
                self.pozostale_statki[len(self.statek)]-=1
                self.statek=[]
                print('trafiony zatopiony')
            elif not self.czy_zostaly_statki(len(self.statek)+1):
                self.zatop()
                print('brak dluzszych statkow')
                self.pozostale_statki[len(self.statek)]-=1
                self.statek=[]
            return 1
        else:
            self.plansza[i][j]=-1
            return 0
    
'''ustaw_statki()
original=statki_bota
for j in range(10):
    for k in range(10):
        print(statki_bota[j][k],end=" ")
    print('\n')
print('\n')
print('\n') 
for i in range (100):
    if strzelaj()==2:
        print(i)
        exit()
    for j in range(10):
        for k in range(10):
            if plansza[j][k]==-2: print("S",end=" ")
            if plansza[j][k]==-1: print("X",end=" ")
            if plansza[j][k]==0: print("~",end=" ")
        print('\n')
    print(pozostale_statki[1], ' ', pozostale_statki[2], ' ', pozostale_statki[3], ' ', pozostale_statki[4], ' ') '''
wyniki = []
bot=bot()
for _ in range(1000):
    bot.reset()
    bot.ustaw_statki()
    original = [row[:] for row in bot.statki_bota]
    for t in range(100):
        if bot.strzelaj() == 2:
            wyniki.append(t+1)
            break

print("Średnia:", sum(wyniki)/len(wyniki))
print("Min:", min(wyniki))
print("Max:", max(wyniki))

