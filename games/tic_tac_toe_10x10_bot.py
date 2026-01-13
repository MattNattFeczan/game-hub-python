
PUSTE = 0
BOT = 2
GRACZ = 1
MAX_GLEBOKOSC = 3

def najlepszy_ruch(plansza):
    #Przyjmuje stan planszy i zwraca najlepszy ruch dla bota.
    wynik, ruch = minimax(plansza, MAX_GLEBOKOSC, float('-inf'), float('inf'), True)
    
    #print(f"Bot wybrał ruch {ruch} z oceną {wynik}") #debug
    return ruch


def minimax(plansza, glebokosc, alpha, beta, maksymalizujacy):
    #Minimaks z przycinaniem alfa-beta.
    #alpha - najlepszy wynik jaki bot moze osiagnac we wczesniej sprawdzonych galeziach
    #beta - najnizszy wynik do ktorego gracz moze zmusic bota we wczesniej sprawdzonych galeziach
    zwyciezca = end_game_copy(plansza)
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

    czy_plansza_pusta = True
    for w in range(wiersze):
        for k in range(kolumny):
            if plansza[w][k] != PUSTE:
                czy_plansza_pusta = False
                break
        if not czy_plansza_pusta:
            break

    if czy_plansza_pusta:
        return [(wiersze // 2, kolumny // 2)]  # jesli plansza jest pusta, zagraj na srodku

    for wiersz in range(wiersze):
        for kolumna in range(kolumny):
            if plansza[wiersz][kolumna] == PUSTE and ma_sasiada(plansza, wiersz, kolumna):     #optymalizacja ilosci pol ktore bot bierze pod uwage
                ruchy.append((wiersz, kolumna))

    return ruchy

def ma_sasiada(plansza, wiersz, kolumna):
    #sprawdza czy pole sasiaduje z zajetym polem
    wiersze = len(plansza)
    kolumny = len(plansza[0])
    promien = 1
    wiersz_start = max(0, wiersz - promien)
    wiersz_kon = min(wiersze, wiersz + promien + 1)
    kolumna_start = max(0, kolumna - promien)
    kolumna_kon = min(kolumny, kolumna + promien + 1)

    for w in range(wiersz_start, wiersz_kon):
        for k in range(kolumna_start, kolumna_kon):
            if(plansza[w][k] != PUSTE): #nie trzeba sprawdzac czy plansza[w][k] to sprawdzane pole, bo to pole jest puste
                return True
    return False


def ocena_planszy(plansza):
   #funkcja obliczajaca punkty dla aktualnego stanu, poprzez dodawanie punktow za sytuacje korzystne dla bota i
   #odejmowanie punktow za sytuacje korzystne dla gracza
    suma = 0
    wiersze = len(plansza)
    kolumny = len(plansza[0])
    for w in range(wiersze):
        for k in range(kolumny):

           #sprawdzenie w poziomie
           if k + 4 < kolumny:
               sekwencja = [plansza[w][k+i] for i in range(5)]
               suma += ocena_sekwencji(sekwencja)

           #sprawdzenie w pionie
           if w + 4 < wiersze:
               sekwencja = [plansza[w+i][k] for i in range(5)]
               suma += ocena_sekwencji(sekwencja)

           #sprawdzenie w skosie w prawo i w dol
           if w + 4 < wiersze and k + 4 < kolumny:
               sekwencja = [plansza[w+i][k+i] for i in range(5)]
               suma += ocena_sekwencji(sekwencja)

            # sprawdzenie w skosie w lewo i w dol
           if w + 4 < wiersze and k - 4 >= 0:
               sekwencja = [plansza[w+i][k-i] for i in range(5)]
               suma += ocena_sekwencji(sekwencja)

    return suma


def ocena_sekwencji(sekwencja):
    #funkcja przyznajaca punkty za konkretna sekwencje pieciu pol
    punkty = 0
    pola_bota = sekwencja.count(BOT)
    pola_gracza = sekwencja.count(GRACZ)

    # jesli sekwencja zawiera pola obu grajacych,
    # to nie prowadzi do zwyciestwa i nie jest zagrozeniem
    if pola_bota > 0 and pola_gracza > 0:
        return 0

    #punkty przyznane za sekwencje bota
    if pola_bota == 5:
        punkty += 100000000
    elif pola_bota == 4:
        punkty += 20000
    elif pola_bota == 3:
        punkty += 200
    elif pola_bota == 2:
        punkty += 20
    elif pola_bota == 1:
        punkty += 1

    # punkty odjete za sekwencje gracza
    if pola_gracza == 5:
        punkty -= 100000000
    if pola_gracza == 4:
        punkty -= 30000
    elif pola_gracza == 3:
        punkty -= 300
    elif pola_gracza == 2:
        punkty -= 30
    elif pola_gracza == 1:
        punkty -= 1

    return punkty


def end_game_copy(board):
    for wiersz in range(10):
        for kolumna in range(10):
            na_polu = board[wiersz][kolumna]
            if na_polu == 0:
                continue
                
            if kolumna + 4 < 10:
                if (board[wiersz][kolumna + 1] == na_polu and
                        board[wiersz][kolumna + 2] == na_polu and
                        board[wiersz][kolumna + 3] == na_polu and
                        board[wiersz][kolumna + 4] == na_polu):
                    return na_polu
                
            if wiersz + 4 < 10:
                if (board[wiersz + 1][kolumna] == na_polu and
                        board[wiersz + 2][kolumna] == na_polu and
                        board[wiersz + 3][kolumna] == na_polu and
                        board[wiersz + 4][kolumna] == na_polu):
                    return na_polu
                
            if wiersz + 4 < 10 and kolumna + 4 < 10:
                if (board[wiersz + 1][kolumna + 1] == na_polu and
                        board[wiersz + 2][kolumna + 2] == na_polu and
                        board[wiersz + 3][kolumna + 3] == na_polu and
                        board[wiersz + 4][kolumna + 4] == na_polu):
                    return na_polu

            if wiersz + 4 < 10 and kolumna - 4 >= 0:
                if (board[wiersz + 1][kolumna - 1] == na_polu and
                        board[wiersz + 2][kolumna - 2] == na_polu and
                        board[wiersz + 3][kolumna - 3] == na_polu and
                        board[wiersz + 4][kolumna - 4] == na_polu):
                    return na_polu
    return 0