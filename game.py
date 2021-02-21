import random


class Tile(object):
    """ reprezentacja kostki """

    def __init__(self, left=0, right=0):
        self.left = left
        self.right = right

    def __repr__(self):
        return '%s | %s' % (self.left, self.right)


class Game:
    """ gra wlasciwa """

    def __init__(self, gracz_1, gracz_2):
        self.domino = [Tile(0, 0), Tile(0, 1), Tile(0, 2), Tile(0, 3), Tile(0, 4), Tile(0, 5), Tile(0, 6),
                       Tile(1, 1), Tile(1, 2), Tile(1, 3), Tile(1, 4), Tile(1, 5), Tile(1, 6),
                       Tile(2, 2), Tile(2, 3), Tile(2, 4), Tile(2, 5), Tile(2, 6),
                       Tile(3, 3), Tile(3, 4), Tile(3, 5), Tile(3, 6),
                       Tile(4, 4), Tile(4, 5), Tile(4, 6),
                       Tile(5, 5), Tile(5, 6),
                       Tile(6, 6)]

        random.shuffle(self.domino)

        # czyja kolej
        self.turn = 0
        # nazwy graczy
        self.imiona = [gracz_1, gracz_2]
        # gracze
        self.gracze = []

        # rozdanie początkowych kostek
        for i in range(len(self.imiona)):
            self.gracze.append(Player())
            for k in range(7):
                self.gracze[i].pobierz_kostke(self)

        # czy koniec
        self.koniec = None
        # kostki na stole
        self.na_stole = []

    def start(self, tile=None):
        self.ruch_gracza(tile)
        if self.czy_zakonczyc_gre():
            return True

        self.zmiana_gracza()

    # wybieranie kostki i usuniecie z puli
    def wybierz_kostke(self, domino):
        kos = random.sample(self.domino, 1)[0]
        self.domino.remove(kos)
        return kos

    # ruch gracza
    def ruch_gracza(self, tile=None):
        # print('gracze:', self.gracze)
        # print('tura:', self.turn)

        if tile:
            self.poloz_na_stole(self.gracze[self.turn].odrzuc_kostke(tile))

        else:
            self.dobierz_kostke_ze_stosu()
        self.turn = (self.turn + 1) % 2

    # zmiana gracza
    def zmiana_gracza(self):
        pass
        # self.turn = (self.turn + 1) % 2

    def poloz_na_stole(self, t):
        if not self.na_stole:
            self.na_stole.append(t)

        elif t.left == self.na_stole[0].left:
            t.left, t.right = t.right, t.left
            self.na_stole.insert(0, t)

        elif t.left == self.na_stole[-1].right:
            self.na_stole.append(t)

        elif t.right == self.na_stole[0].left:
            self.na_stole.insert(0, t)

        elif t.right == self.na_stole[-1].right:
            t.left, t.right = t.right, t.left
            self.na_stole.append(t)

        print(self.na_stole)

    # dobranie z puli
    def dobierz_kostke_ze_stosu(self):

        if len(self.domino) != 0:
            self.gracze[self.turn].pobierz_kostke(self)

        else:
            self.zmiana_gracza()

        self.zmiana_gracza()

    # sprawdzanie czy koniec gry
    def czy_zakonczyc_gre(self):
        print('pozostało klocków:', len(self.gracze[0].domino_gracza))
        print('pozostało klocków:', len(self.gracze[1].domino_gracza))

        for player_number in range(2):
            if len(self.gracze[player_number].domino_gracza) == 0:
                self.koniec = True
                return True


class Player:
    """ gracz """

    # kostki w ręce gracza
    def __init__(self):
        self.domino_gracza = list()

    def __repr__(self):
        return str(self.domino_gracza)

    # dobieranie
    def pobierz_kostke(self, g):
        self.domino_gracza.append(g.wybierz_kostke(g))

    # pozbycie sie kostki z reki gracza
    def odrzuc_kostke(self, wybrana_kostka):
        # zwracany jest index
        return self.domino_gracza.pop(wybrana_kostka)

    def wyloz_kostke(self, tile):
        for t in self.domino_gracza:
            if t == tile:
                return tile
        raise AssertionError('Brak pasującej kostki')