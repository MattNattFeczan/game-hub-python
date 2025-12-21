import random
import bisect
plansza=[[0]*10 for i in range(10)]
original=[
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 1, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
]
statki_bota=[[0]*10 for i in range(10)]
pozostale_statki=[0, 4, 3, 2, 1] #indeks to dlugosc statku
sprawdz_obok_x=[1,-1,0,0]
sprawdz_obok_y=[0,0,1,-1]
ktory=0
statek=[]
trafione_pola=0
def reset():
    global statek, ktory, ktory_z_rzedu
    statek=[]
    ktory=0
    ktory_z_rzedu=0
    pozostale_statki[1]=4
    pozostale_statki[2]=3
    pozostale_statki[3]=2
    pozostale_statki[4]=1
    for i in range (10):
        for j in range (10):
            plansza[i][j]=0
            statki_bota[i][j]=0
            original[i][j]=0

def mozna_ustawic(x, y, poziomy, dlugosc):
    if poziomy:
        if y+dlugosc>9: return 0
        for i in range (-1, dlugosc+1):
            if y+i>-1 and y+i<10:
                if statki_bota[x][y+i]: return 0
                if x+1<10:
                    if statki_bota[x+1][y+i]: return 0
                if x-1>-1:
                    if statki_bota[x-1][y+i]: return 0    
    else:
        if x+dlugosc>9: return 0
        for i in range (-1, dlugosc+1):
            if x+i>-1 and x+i<10:
                if statki_bota[x+i][y]: return 0
                if y+1<10:
                    if statki_bota[x+i][y+1]: return 0
                if y-1>-1:
                    if statki_bota[x+i][y-1]: return 0    
    return 1

def ustaw_statki():
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
            mozna=mozna_ustawic(x_pocz, y_pocz, poziomy, statki_do_ustawienia[i]) 
        for j in range (statki_do_ustawienia[i]):
            if poziomy:
                statki_bota[x_pocz][y_pocz+j]=1
            else:
                statki_bota[x_pocz+j][y_pocz]=1

def zaktualizuj_pozostale_pola():
    szachownica=[]
    pozostale=[]
    for i in range (10):
        for j in range (10):
            if plansza[i][j]==0:
                if not (i+j)%2:
                    szachownica.append((i,j))
                else:
                    pozostale.append((i,j))
    if szachownica:
        return szachownica
    return pozostale

def czy_zostaly_statki(od): #sprawdz czy jest sens dalej szukac reszty statku
    for i in range (od, 5):
        if(pozostale_statki[i]):
            return True
    return False  
def losuj(losowanie):
	strzal=random.choice(losowanie)
	i, j=strzal
	return i,j

def kontynuuj(i,j): #jesli trafiony strzelaj dalej
    global ktory
    if len(statek)==1:
        while ktory<4:
            test_i=i+sprawdz_obok_x[ktory]
            test_j=j+sprawdz_obok_y[ktory] 
            ktory+=1
            if test_i>-1 and test_j>-1 and test_i<10 and test_j<10 and plansza[test_i][test_j]!=-1 and plansza[test_i][test_j]!=-2:
                return test_i, test_j
        for a in range (-1, 2): #zatop statek
            for b in range (-1, 2):
                if i+a>-1 and i+a<10 and j+b>-1 and j+b<10 and plansza[i+a][j+b]!=-2: plansza[i+a][j+b]=-1
        pozostale_statki[1]-=1
        return None, None
    else:
        x_pocz, y_pocz=statek[0]
        x_kon, y_kon=statek[-1]
        if x_pocz-x_kon==0:
            if y_pocz-1>-1 and plansza[x_pocz][y_pocz-1]!=-1 and plansza[x_pocz][y_pocz-1]!=-2:
                return x_pocz, y_pocz-1
            elif y_kon+1<10 and plansza[x_pocz][y_kon+1]!=-1 and plansza[x_pocz][y_kon+1]!=-2:
                return x_pocz, y_kon+1
            for i in range (-1, len(statek)+1): #zatop
                if y_pocz+i>-1 and y_pocz+i<10:
                    if x_pocz-1>-1:
                        plansza[x_pocz-1][y_pocz+i]=-1
                    if x_pocz+1<10:
                        plansza[x_pocz+1][y_pocz+i]=-1
        elif y_pocz-y_kon==0:
            if x_pocz-1>-1 and plansza[x_pocz-1][y_pocz]!=-1 and plansza[x_pocz-1][y_pocz]!=-2:
                return x_pocz-1, y_pocz
            elif x_kon+1<10 and plansza[x_kon+1][y_pocz]!=-1 and plansza[x_kon+1][y_pocz]!=-2:
                return x_kon+1, y_pocz
            for i in range (-1, len(statek)+1): #zatop
                if x_pocz+i>-1 and x_pocz+i<10:
                    if y_pocz-1>-1:
                        plansza[x_pocz+i][y_pocz-1]=-1
                    if y_pocz+1<10:
                        plansza[x_pocz+i][y_pocz+1]=-1
        pozostale_statki[len(statek)]-=1
        return None, None

def strzelaj():
    global statek, ktory, trafione_pola
    losowanie=zaktualizuj_pozostale_pola()
    i,j=(None, None)
    if statek and czy_zostaly_statki(len(statek)):
        i,j=kontynuuj(statek[-1][0], statek[-1][1])
    if i is None: #jesli zamiast if wstawic else nie sprawdzalby czy kontynuuj zwrocilo none
        ktory=0
        statek=[]
        i,j=losuj(losowanie)
    plansza[i][j]=-1
    if original[i][j]==1:
        if plansza[i][j]==-2: print('pomocy')
        trafione_pola+=1
        if trafione_pola==20:
            #print('zwyciestwo')
            return 2
        plansza[i][j]=-2
        bisect.insort(statek, (i, j))
        return 1
    else:
        return 0
       
ustaw_statki()
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
    #for j in range(10):
     #   for k in range(10):
      #      if plansza[j][k]==-2: print("S",end=" ")
       #     if plansza[j][k]==-1: print("X",end=" ")
        #    if plansza[j][k]==0: print("~",end=" ")
        #print('\n')
    #print(pozostale_statki[1], ' ', pozostale_statki[2], ' ', pozostale_statki[3], ' ', pozostale_statki[4], ' ')     
