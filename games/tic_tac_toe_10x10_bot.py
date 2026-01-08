from tic_tac_toe_10x10 import end_game

PUSTE = 0
BOT = 2
GRACZ = 1
MAX_GLEBOKOSC = 3

def najlepszy_ruch(plansza):
    #Przyjmuje stan planszy i zwraca najlepszy ruch dla bota.
    wynik, ruch = minimax(plansza, MAX_GLEBOKOSC, float('-inf'), float('inf'), True)
    
    print(f"Bot wybrał ruch {ruch} z oceną {wynik}") #debug
    
    return ruch
def minimax(plansza, glebokosc, alpha, beta, maksymalizujacy):
    #Minimaks z przycinaniem alfa-beta.
    #alpha - najlepszy wynik jaki bot moze osiagnac we wczesniej sprawdzonych galeziach
    #beta - najnizszy wynik do ktorego gracz moze zmusic bota we wczesniej sprawdzonych galeziach
    zwyciezca = end_game(plansza)
    if zwyciezca == BOT:
        return 1000000, None
    elif zwyciezca == GRACZ: return -1000000, None
    
    if glebokosc == 0:
        return ocena_planszy(plansza), None
    
    mozliwe_ruchy = sprawdz_mozliwe_ruchy(plansza)
    if not mozliwe_ruchy:
        return 0, None  #remis, brak mozliwych ruchow
    
    najlepszy = None #najlepszy ruch do zwrocenia
    
    if(maksymalizujacy):
        max_wynik = float('-inf')
        for ruch in mozliwe_ruchy:
            wiersz, kolumna = ruch
            plansza[wiersz][kolumna] = BOT
            
            wynik_temp, _  = minimax(plansza, glebokosc - 1, alpha, beta, False )
            plansza[wiersz][kolumna] = PUSTE
            
            if wynik_temp > max_wynik:
                max_wynik = wynik_temp
                najlepszy = ruch
            
            alpha = max(alpha, wynik_temp)
            if beta <= alpha:
                break  #gracz nie wybierze tej galezi, bo ma dostepny nizszy wynik we wczesniej sprawdzonych galeziach
        return max_wynik, najlepszy
                
            
    else:
        min_wynik = float('inf')
        for ruch in mozliwe_ruchy:
            wiersz, kolumna = ruch
            plansza[wiersz][kolumna] = GRACZ
            
            wynik_temp, _ = minimax(plansza, glebokosc - 1, alpha, beta, True)
            plansza[wiersz][kolumna] = PUSTE
            
            if wynik_temp < min_wynik:
                min_wynik = wynik_temp
                najlepszy = ruch
            
            beta = min(beta, wynik_temp)
            if beta <= alpha:
                break  #bot nie wybierze tej galezi, bo ma dostepny wyzszy wynik we wczesniej sprawdzonych galeziach
        return min_wynik, najlepszy

def sprawdz_mozliwe_ruchy(plansza):
    ruchy = []
    wiersze = len(plansza)
    kolumny = len(plansza[0])

    for wiersz in range(wiersze):
        for kolumna in range(kolumny):
            if plansza[wiersz][kolumna] == PUSTE: #and ma_sasiada(plansza, wiersz, kolumna):     optymalizacja pol ktore bot bierze pod uwage
                ruchy.append((wiersz, kolumna))

    return ruchy

    
    