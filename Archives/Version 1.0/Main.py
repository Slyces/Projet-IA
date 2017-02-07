# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille & Loizel Antoine'
__version__ = ''
__date__ = '26/01/2017'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr & antoine.loizel@etu.u-bordeaux.fr'
__status__ = 'TD'
# =============================================================================

from typing import Tuple

# Constantes
BLANC = 0
NOIR = 1
VIDE = None
COULEURS = {BLANC: "O", NOIR: "X", VIDE:"_"}

class Case(object):
    def __init__(self, position: int, contenu= VIDE):
        self.__valeur = VIDE
        self.valeur = contenu
        self.__position = position
        self.__voisinage = {}
        self.__invcolor = {BLANC: NOIR, NOIR: BLANC, VIDE: VIDE}
        self.__voisins = set()

    @property
    def position(self):
        return self.__position

    @property
    def valeur(self):
        return self.__valeur

    @valeur.setter
    def valeur(self, value):
        if value in COULEURS.keys():
            self.__valeur = value

    @property
    def voisinage(self):
        return self.__voisinage.copy()

    @property
    def voisins(self):
        return list(self.__voisins)

    @property
    def estLibre(self):
        return self.__valeur == VIDE

    @property
    def estBloquee(self):
        return (not self.estLibre) and not (True in [voisin.estLibre for voisin in self.voisins])

    def estAccessible(self, color):
        return self.estLibre and color in [voisin.valeur for voisin in self.voisins]

    def force(self, color):
        return 0 if not self.estAccessible(color) else sum([voisin.valeur == self.__invcolor[color]
                                                            for voisin in self.voisins])
    
    @voisins.setter
    def voisins(self, arg: Tuple[int, 'Case']):
        if type(arg) is tuple and len(arg) == 2:
            index, cell = arg
            if type(index) is int and index >= 0 and type(cell) is Case \
                                    and index not in self.voisinage.keys():
                self.__voisins.add(cell)
                self.__voisinage[index] = cell
                cell.voisins = (index+4) % 8, self

    def __str__(self):
        return COULEURS[self.valeur]

    def __repr__(self):
        return "Case en position {i} et de contenu {c}".format(i=self.position, c=self.valeur)

class Plateau(object):
    def __init__(self, x: int, h: int= 5):
        h = 5 if h%2 == 0 else h
        self.__h, self.__x = h, x
        self.__len = h * x + (h//2)**2
        self.__cells = []

        # Construction du plateau
        for k in range(len(self)):
            self.__cells.append(Case(k))

        for a in range(h):
            for b in range(self.__length(a)):
                if a < h // 2:
                    L = [(5, (1, 0)), (3, (1, 1)), (2, (0, 1))]
                elif a == h//2 :
                    L = [(2, (0, 1))]
                else :
                    L = [(1, (-1, 1)), (2, (0, 1)), (7, (-1, 0))]
                for (k, (i, j)) in L:
                    if 0 <= a + i < h and 0 <= b + j < self.__length(a+i):
                        self[a,b].voisins = k, self[a+i, b+j]

    def __length(self, ligne: int):
        h = self.__h
        return self.__x + ligne if ligne <= h // 2 else self.__x + h - 1 - ligne

    def keys(self):
        return [self.pos2coord(x) for x in range(len(self))]

    @property
    def largeur(self):
        return self.__x

    @property
    def hauteur(self):
        return self.__h

    @property
    def configuration(self):
        return self.__cells.copy()

    @property
    def libres(self):
        return list(filter(lambda x: x.estLibre, self.configuration))

    def jouables(self, color):
        return list(filter(lambda x: x.estAccessible(color), self.configuration))

    def jouablesTriees(self, color):
        J = self.jouables(color)
        J.sort(key = lambda x: x.force(color), reverse=True)
        return J

    def evaluation(self, color):
        from random import randint
        return randint(1,35)

    def pos2coord(self, k: int):
        l = self.__x
        for i in range(self.__h):
            if 0 <= k < l:
                return i, k
            k -= l
            l += 1 if i < self.__h // 2 else -1

    def coord2pos(self, i: int, j: int):
        l = self.__h // 2
        return sum([self.__x + k if k <= l else self.__x + l - k%l for k in range(i)]) + j

    def __getitem__(self, index):
        if type(index) is int:
            return self.__cells[index]
        elif type(index) is tuple and len(index) == 2:
            return self.__cells[self.coord2pos(*index)]

    def __len__(self):
        return self.__len

    def __repr__(self):
        return "Plateau({h},{l})".format(h=self.hauteur, l=self.largeur)

    def __str__(self):
        k = max(map(len, COULEURS.values()))
        s = ''
        for i in range(self.hauteur):
            s += abs(i - self.hauteur // 2) * ' '*(k+2)
            for j in range(self.__length(i)):
                s += COULEURS[self[i,j].valeur].center(k, ' ') + ' '*(k+4)
            s += '\n'
        return s


"""
╳╲╱│┃━━━
    __
 ╱    ╲
 ┃      ┃
 ╲ __ ╱
"""


if __name__ == "__main__":
    # print("Partie 1")
    # c = Case(23)  # ok équivalent à Case(23, VIDE)
    # d = Case(1, NOIR)  # ok ça doit marcher
    # e = Case(2.5, "blanc")  # je ne sais pas ce qui se passe
    # print(c.valeur)  # affiche la valeur de la constante VIDE
    # c.valeur = BLANC
    # print(c.valeur)  # affiche la valeur de la constante BLANC
    # print(d.valeur)  # affiche la valeur de la constante NOIR
    # d.valeur = "vert"
    # print(d.valeur)  # affiche la valeur de la constante NOIR
    #
    # print("Partie 2")
    # a = Case(1)
    # b = Case(5, NOIR)
    # c = Case(7)
    # print("On attend [ ]", a.voisins)  # affiche [ ]
    # print("On attend { }", a.voisinage)  # affiche { }
    # print("On attend [ ]", b.voisins)  # affiche [ ]
    # print("On attend { }", b.voisinage)  # affiche { }
    # a.voisins = 2, b
    # print("On attend [ b ]", a.voisins)  # affiche [ b ]
    # print("On attend {2: b}", a.voisinage)  # affiche {2: b}
    # print("On attend [ a ]", b.voisins)  # affiche [ a ]
    # print("On attend {6: a}", b.voisinage)  # affiche {6: a}
    # b.voisins = 6, c
    # print("On attend [ a ]", b.voisins)  # affiche [ a ]
    # print("On attend {6: a}", b.voisinage)  # affiche {6: a}
    # print("On attend [ ]", c.voisins)  # affiche [ ]
    # print("On attend { }", c.voisinage)  # affiche { }
    p = Plateau(5, 7)

    print("=======")
    print(repr(p[17]))
    print(p[17].voisins)
    for cell in p[17].voisins :
        print(p.pos2coord(cell.position))
    print(repr(p))
    print(p)
