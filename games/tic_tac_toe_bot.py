from tic_tac_toe_10x10 import end_game

PUSTE = 0
BOT = 2
GRACZ = 1
MAX_GLEBOKOSC = 3

def najlepszy_ruch(plansza, gracz):
    #Przyjmuje stan planszy i zwraca najlepszy ruch dla danego gracza.
    wynik, ruch = minimax(plansza, MAX_GLEBOKOSC, float('-inf'), float('inf'), True)
    
    print(f"Bot wybrał ruch {ruch} z oceną {wynik}") #debug
    
    return ruch
def minimax(plansza, glebokosc, alpha, beta, maksymalizujacy):
    #Minimaks z przycinaniem alfa-beta. 
    zwyciezca = end_game(plansza)
    if zwyciezca == BOT:
        return 1000000, None
    elif zwyciezca == GRACZ: return -1000000, None
    
    if glebokosc == 0:
        return ocena_planszy(plansza), None
    
    mozliwe_ruchy = zbadaj_mozliwe_ruchy(plansza)
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
                break  #beta (maksimum na ktore pozwoli gracz w tej galezi) jest mniejsza 
                       #niz alpha (minimum jakie bot potrafi osiagnac w tej galezi) wiec jej nie sprawdzamy
        return (max_wynik, najlepszy)
                
            
    else:
        min_wynik = float('inf')
        for ruch in mozliwe_ruchy:
            wiersz, kolumna = ruch
            plansza[wiersz][kolumna] = GRACZ
            
            wynik_temp, ruch = minimax(plansza, glebokosc - 1, alpha, beta, True)
            plansza[wiersz][kolumna] = PUSTE
            
            if wynik_temp < min_wynik:
                min_wynik = wynik_temp
                najlepszy = ruch
            
            beta = min(beta, wynik_temp)
            if beta <= alpha:
                break  #identyczne uzasadnienie jak wyzej
        return min_wynik, najlepszy
    

    
    