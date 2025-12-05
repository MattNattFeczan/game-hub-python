import random
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
ostatni_trafiony=(None, None)
wspolrzedne_poczatku=(None, None)
statek_na_celowniku=0
ktory_z_rzedu=0
def zaktualizuj_pozostale_pola():
	pozostale=[]
	for i in range (10):
		for j in range (10):
			if plansza[i][j]!=-1:
				pozostale.append((i,j))
	return pozostale
def czy_zostaly_statki(od): #sprawdz czy jest sens dalej szukac reszty statku
    for i in range (od, 5):
        if(pozostale_statki[i]):
            return True
    return False  
#def zatopiony():  #zaznacz pola wokoło zatopionego statku
def losuj(losowanie):
	strzal=random.choice(losowanie)
	i, j=strzal
	return i,j
def kontynuuj(i,j): #jesli trafiony strzelaj dalej
    global ktory, ktory_z_rzedu
    if ktory_z_rzedu==1:
        while ktory<4:
            print("ekstra")
            test_i=i+sprawdz_obok_x[ktory]
            test_j=j+sprawdz_obok_y[ktory] 
            ktory+=1
            if test_i>-1 and test_j>-1 and test_i<10 and test_j<10 and plansza[test_i][test_j]!=-1:
                return test_i, test_j
        return (None, None)
    else:
        return (None, None)
		    #do pomyslenia
def strzelaj():
    global statek_na_celowniku, ostatni_trafiony, ktory_z_rzedu, ktory
    losowanie=zaktualizuj_pozostale_pola()
    i,j=(None, None)
    if statek_na_celowniku and ostatni_trafiony is not None and czy_zostaly_statki(ktory_z_rzedu):
        i,j=kontynuuj(ostatni_trafiony[0],ostatni_trafiony[1])
    if not statek_na_celowniku or i is None or not czy_zostaly_statki(ktory_z_rzedu):
        statek_na_celowniku=0
        ktory_z_rzedu=0
        ktory=0
        i,j=losuj(losowanie)
    plansza[i][j]=-1
    if original[i][j]==1:
        #print("trafiony")
        ktory_z_rzedu+=1
        statek_na_celowniku=1
        ostatni_trafiony=(i,j)
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
