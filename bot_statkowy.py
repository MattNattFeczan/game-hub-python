import random
import bisect
#plansza=[[0]*10 for i in range(10)]
plansza=[
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
]
original=[
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 1, 1, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
]
#original=[[0]*10 for i in range(10)]
pozostale_statki=[0, 4, 3, 2, 1] #indeks to dlugosc statku
sprawdz_obok_x=[1,-1,0,0]
sprawdz_obok_y=[0,0,1,-1]
ktory=0
ostatni_trafiony=None, None
statek=[]
statek_na_celowniku=0
ktory_z_rzedu=0
def zaktualizuj_pozostale_pola():
	pozostale=[]
	for i in range (10):
		for j in range (10):
			if plansza[i][j]!=-1 and plansza[i][j]!=-2:
				pozostale.append((i,j))
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
    global ktory, ktory_z_rzedu, pozostale_statki
    if ktory_z_rzedu==1:
        while ktory<4:
            print("ekstra")
            test_i=i+sprawdz_obok_x[ktory]
            test_j=j+sprawdz_obok_y[ktory] 
            ktory+=1
            if test_i>-1 and test_j>-1 and test_i<10 and test_j<10 and plansza[test_i][test_j]!=-1 and plansza[test_i][test_j]!=-2:
                return test_i, test_j
        if i+1<10: plansza[i+1][j]=-1 #zatop statek
        if i-1>-1: plansza[i-1][j]=-1
        if j+1<10: plansza[i][j+1]=-1
        if j-1>-1: plansza[i][j-1]=-1
        pozostale_statki[1]-=1
        return None, None
    else:
        x_pocz, y_pocz=statek[0]
        x_kon, y_kon=statek[-1]
        if x_pocz-x_kon==0:
            if y_pocz-1>-1 and plansza[x_pocz][y_pocz-1]!=-1 and plansza[x_pocz][y_pocz-1]!=-2:
                return x_pocz, y_pocz-1
            elif y_pocz+1<10 and plansza[x_pocz][y_pocz+1]!=-1 and plansza[x_pocz][y_pocz+1]!=-2:
                return x_pocz, y_pocz+1
            for i in range (len(statek)): #zatop
                if x_pocz-1>-1:
                    plansza[x_pocz-1][y_pocz+i]=-1
                if x_pocz+1<10:
                    plansza[x_pocz-1][y_pocz+i]=-1
        elif y_pocz-y_kon==0:
            if x_pocz-1>-1 and plansza[x_pocz-1][y_pocz]!=-1 and plansza[x_pocz-1][y_pocz]!=-2:
                return x_pocz-1, y_pocz
            elif x_pocz+1>-1 and plansza[x_pocz+1][y_pocz]!=-1 and plansza[x_pocz+1][y_pocz]!=-2:
                return x_pocz+1, y_pocz
            for i in range (len(statek)): #zatop
                if y_pocz-1>-1:
                    plansza[x_pocz+i][y_pocz-1]=-1
                if y_pocz+1<10:
                    plansza[x_pocz+i][y_pocz+1]=-1
        pozostale_statki[ktory_z_rzedu]-=1
        return None, None
def strzelaj():
    global statek, ktory_z_rzedu, ktory
    losowanie=zaktualizuj_pozostale_pola()
    i,j=(None, None)
    if statek and czy_zostaly_statki(ktory_z_rzedu):
        i,j=kontynuuj(statek[-1][0], statek[-1][1])
    if not statek or not czy_zostaly_statki(ktory_z_rzedu) or i is None: #jesli zamiast if wstawic else nie sprawdzalby czy kontynuuj zwrocilo none
        ktory_z_rzedu=0
        ktory=0
        statek=[]
        i,j=losuj(losowanie)
    plansza[i][j]=-1
    if original[i][j]==1:
        plansza[i][j]=-2
        bisect.insort(statek, (i, j))
        ktory_z_rzedu+=1
        return 1
    else:
        return 0
for i in range(10):
    if strzelaj()==1:
        for j in range(10):
            for k in range(10):
                print(plansza[j][k],end=" ")
            print('\n')
        print('\n')     
