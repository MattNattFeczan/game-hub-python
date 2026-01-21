PUSTE = 0
BOT = 2
GRACZ = 1
MAX_GLEBOKOSC = 4

def najlepszy_ruch(plansza):
    #Przyjmuje stan planszy i zwraca najlepszy ruch dla bota.
    wynik, ruch = minimax(plansza, MAX_GLEBOKOSC, float('-inf'), float('inf'), True)

    return ruch


def minimax(plansza, glebokosc, alpha, beta, maksymalizujacy):
    #Minimaks z przycinaniem alfa-beta.
    #alpha - najlepszy wynik jaki bot moze osiagnac we wczesniej sprawdzonych galeziach
    #beta - najnizszy wynik do ktorego gracz moze zmusic bota we wczesniej sprawdzonych galeziach
    zwyciezca = end_game_copy(plansza)
    if zwyciezca == BOT:
        return 1000000000 + glebokosc, None
    elif zwyciezca == GRACZ: return -2000000000, None

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
    wiersze = len(plansza)
    kolumny = len(plansza[0])
    kierunki_glowne = [(1, 0), (0, 1), (1, 1), (1, -1)]
    kandydaci = []
    srodek_planszy = (4.5, 4.5)

    for w in range(wiersze):
        for k in range(kolumny):
            if plansza[w][k] == PUSTE:
                waga = 0
                ma_sasiada = False

                max_linia_gracza = 0
                max_linia_bota = 0

                for dr, dc in kierunki_glowne:

                    #sprawdzamy jak dlugie powstana linie w obie strony
                    #gracz:
                    dlugosc_g = 0
                    #strona 1
                    for i in range(1, 5):
                        r, c = w + dr * i, k + dc * i
                        if 0 <= r < wiersze and 0 <= c < kolumny and plansza[r][c] == GRACZ:
                            dlugosc_g += 1
                        else:
                            break
                    #strona 2
                    for i in range(1, 5):
                        r, c = w - dr * i, k - dc * i
                        if 0 <= r < wiersze and 0 <= c < kolumny and plansza[r][c] == GRACZ:
                            dlugosc_g += 1
                        else:
                            break

                    #to samo  dla bota
                    dlugosc_b = 0
                    for i in range(1, 5):
                        r, c = w + dr * i, k + dc * i
                        if 0 <= r < wiersze and 0 <= c < kolumny and plansza[r][c] == BOT:
                            dlugosc_b += 1
                        else:
                            break
                    for i in range(1, 5):
                        r, c = w - dr * i, k - dc * i
                        if 0 <= r < wiersze and 0 <= c < kolumny and plansza[r][c] == BOT:
                            dlugosc_b += 1
                        else:
                            break

                    if dlugosc_g > 0: ma_sasiada = True
                    if dlugosc_b > 0: ma_sasiada = True

                    max_linia_gracza = max(max_linia_gracza, dlugosc_g)
                    max_linia_bota = max(max_linia_bota, dlugosc_b)

                    #sprawdzamy czy sa dziury w ktore powinno sie zagrac
                    p1r, p1c = w + dr, k + dc
                    p2r, p2c = w - dr, k - dc
                    if 0 <= p1r < wiersze and 0 <= p1c < kolumny and \
                            0 <= p2r < wiersze and 0 <= p2c < kolumny:
                        if plansza[p1r][p1c] == GRACZ and plansza[p2r][p2c] == GRACZ:
                            waga += 200
                        elif plansza[p1r][p1c] == BOT and plansza[p2r][p2c] == BOT:
                            waga += 100


                #przyznajemy wagi zeby odpowiednio sortowac ruchy
                if max_linia_gracza >= 4: waga += 100000
                if max_linia_bota >= 4:   waga += 100000

                if max_linia_gracza == 3: waga += 10000
                if max_linia_bota == 3:   waga += 10000

                if max_linia_gracza == 2: waga += 1000
                if max_linia_bota == 2:   waga += 1000

                if ma_sasiada: waga += 10

                #bonus za centrum planszy
                dist = abs(w - srodek_planszy[0]) + abs(k - srodek_planszy[1])
                waga += max(0, 5 - (dist // 2))

                if ma_sasiada or waga > 2:
                    kandydaci.append(((w, k), waga))

    if not kandydaci:
        return [(wiersze // 2, kolumny // 2)]

    kandydaci.sort(key=lambda x: x[1], reverse=True)

    #sprawdzamy tylko najlepszych kandydatow na ruch zeby przyspieszyc czas obliczen
    najlepsi_kandydaci = kandydaci[:13]

    ruchy = [x[0] for x in najlepsi_kandydaci]

    return ruchy


def ocena_planszy(plansza):
    # funkcja obliczajaca punkty dla aktualnego stanu, poprzez dodawanie punktow za sytuacje korzystne dla bota i
    # odejmowanie punktow za sytuacje korzystne dla gracza
    #traktowanie sekwecnji jako napis pozwala na dokladniejsze sprawdzanie wzorcow
    wiersze = len(plansza)
    kolumny = len(plansza[0])
    suma = 0

    WAGI = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 2, 2, 2, 2, 2, 2, 1, 0],
        [0, 1, 2, 3, 3, 3, 3, 2, 1, 0],
        [0, 1, 2, 3, 4, 4, 3, 2, 1, 0],
        [0, 1, 2, 3, 4, 4, 3, 2, 1, 0],
        [0, 1, 2, 3, 3, 3, 3, 2, 1, 0],
        [0, 1, 2, 2, 2, 2, 2, 2, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    linie_do_oceny = []

    #poizom
    for w in range(wiersze):
        linia = "".join(str(plansza[w][k]) for k in range(kolumny))
        linie_do_oceny.append(linia)
        for k in range(kolumny):
            if plansza[w][k] == BOT:
                suma += WAGI[w][k]
            elif plansza[w][k] == GRACZ:
                suma -= WAGI[w][k]
    #pion
    for k in range(kolumny):
        linia = "".join(str(plansza[w][k]) for w in range(wiersze))
        linie_do_oceny.append(linia)

    #skos
    for k in range(kolumny - 4):
        linia = "".join(str(plansza[i][k + i]) for i in range(min(wiersze, kolumny - k)))
        linie_do_oceny.append(linia)
    for w in range(1, wiersze - 4):
        linia = "".join(str(plansza[w + i][i]) for i in range(min(kolumny, wiersze - w)))
        linie_do_oceny.append(linia)
    for k in range(4, kolumny):
        linia = "".join(str(plansza[i][k - i]) for i in range(min(wiersze, k + 1)))
        linie_do_oceny.append(linia)
    for w in range(1, wiersze - 4):
        linia = "".join(str(plansza[w + i][kolumny - 1 - i]) for i in range(min(kolumny, wiersze - w)))
        linie_do_oceny.append(linia)

    for linia in linie_do_oceny:
        suma += ocen_linie_string(linia)

    return suma


def ocen_linie_string(linia):
    #funckja przyznaje punkty za konkretne wzorce w linii
    punkty = 0

    #piatki
    if '22222' in linia: return 1000000000
    if '11111' in linia: return -2000000000

    #otwrte czworki
    if '022220' in linia: punkty += 10000000
    if '011110' in linia: punkty -= 20000000

    #czworki z dziura
    if '20222' in linia or '22022' in linia or '22202' in linia: punkty += 10000000
    if '10111' in linia or '11011' in linia or '11101' in linia: punkty -= 20000000

    #czworki otwarte z jednej strony
    if '02222' in linia or '22220' in linia: punkty += 10000000
    if '01111' in linia or '11110' in linia: punkty -= 20000000

    punkty += linia.count('02220') * 500000
    punkty -= linia.count('01110') * 800000


    punkty += linia.count('00222') * 5000
    punkty += linia.count('22200') * 5000
    punkty -= linia.count('00111') * 6000
    punkty -= linia.count('11100') * 6000

    punkty += linia.count('0220') * 500
    punkty -= linia.count('0110') * 600

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