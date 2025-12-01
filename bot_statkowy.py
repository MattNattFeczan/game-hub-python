plansza=[[0]*10 for i in range(10)]
original=[[0]*10 for i in range(10)]
pozostale_statki=[0, 4, 3, 2, 1] #indeks to dlugosc statku
ostatni_trafiony
def zaktualizuj_pozostale_pola():
	pozostale=[]
	for i in range (10):
		for j in range (10):
			if plansza[i][j]!=-1:
				pozostale.append((i,j))
	return pozostale
def strzelaj():
	losuj=zaktualizuj_pozostale_pola()
	strzal=random.choice(losuj)
	i, j=strzal
	plansza[i][j]=-1
	while original[i][j]==1:
		ostatni_trafiony=(i, j)
		losuj=zaktualizuj_pozostale_pola()
		if pozostale_statki[1]!=0 or pozostale_statki[2]!=0 or pozostale_statki[3]!=0 or pozostale_statki[4]!=0:
			strzal=
		else:
			strzal=random.choice(losuj)	
		i, j=strzal
		plansza[i][j]=-1
