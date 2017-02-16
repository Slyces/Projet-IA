# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille & Loizel Antoine'
__version__ = ''
__date__ = '26/01/2017'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'\
            '& antoine.loizel@etu.u-bordeaux.fr'
__status__ = 'TD'
# =============================================================================
import sys, copy

if sys.version_info > (3, 5):
    from typing import Tuple, Any, NewType, List, Dict, Union
    Color = NewType('Color', Any)
    Coord = Tuple[int, int]
# =============================================================================
# Constantes
BLANC = 0
NOIR = 1
VIDE = -1
COULEURS = {BLANC: "O", NOIR: "X", VIDE:"_"}
# =============================================================================
class Case(object):
    def __init__(self, position: int, contenu: 'Color'= VIDE):
        # Attributes
        self.__valeur = VIDE      # init of __valeur
        self.valeur = contenu   # then use of setter
        self.__position = position
        self.__voisinage = {}
        self.__voisins = set()

    # -------------------------------------------------------------------------
    @staticmethod
    def reverse(color: 'Color'):
        return {BLANC: NOIR, NOIR: BLANC, VIDE: VIDE}[color]

    # -------------------------------------------------------------------------
    @property
    def position(self) -> int:
        return self.__position

    # -------------------------------------------------------------------------
    @property
    def valeur(self) -> 'Color':
        return self.__valeur

    @valeur.setter
    def valeur(self, value: 'Color'):
        if value in COULEURS.keys():
            self.__valeur = value

    # -------------------------------------------------------------------------
    @property
    def voisinage(self) -> Dict['Coord','Case']:
        return dict(self.__voisinage)

    # -------------------------------------------------------------------------
    @property
    def voisins(self) -> List['Case']:
        return list(self.__voisins)

    # -------------------------------------------------------------------------
    @voisins.setter
    def voisins(self, arg: Tuple[int, 'Case']) -> None:
        if type(arg) is tuple and len(arg) == 2:
            index, cell = arg
            if type(index) is int and index >= 0 and type(cell) is Case \
                                    and index not in self.voisinage.keys():
                self.__voisins.add(cell)
                self.__voisinage[index] = cell
                cell.voisins = (index+4) % 8, self

    # -------------------------------------------------------------------------
    @property
    def estLibre(self) -> bool:
        return self.__valeur == VIDE

    # -------------------------------------------------------------------------
    @property
    def estBloquee(self) -> bool:
        return (not self.estLibre) and not (True in [voisin.estLibre
                                                   for voisin in self.voisins])

    # -------------------------------------------------------------------------
    def estAccessible(self, color: 'Color') -> bool:
        return self.estLibre and color in [voisin.valeur
                                                    for voisin in self.voisins]

    # -------------------------------------------------------------------------
    def force(self, color: 'Color') -> int:
        return 0 if not self.estAccessible(color) else sum(
            [voisin.valeur == Case.reverse(color)for voisin in self.voisins]
        )

    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        return COULEURS[self.valeur]

    def __repr__(self) -> str:
        return "Case({i},{c})".format(
            i=self.position, c={BLANC:'BLANC', NOIR:'NOIR', VIDE: 'VIDE'}[self.valeur]
        )

# =============================================================================
class Plateau(object):
    def __init__(self, x: int= 5, h: int= 5):
        h = 5 if h%2 == 0 else h
        self.__h = h
        self.__x = x
        self.__cells = []

        # Construction du plateau
        for k in range(len(self)):
            self.__cells.append(Case(k))

        for a in range(h):
            for b in range(self.length(a)):
                if a < h // 2:
                    L = [(5, (1, 0)), (3, (1, 1)), (2, (0, 1))]
                elif a == h//2 :
                    L = [(2, (0, 1))]
                else :
                    L = [(1, (-1, 1)), (2, (0, 1)), (7, (-1, 0))]
                for (k, (i, j)) in L:
                    if 0 <= a + i < h and 0 <= b + j < self.length(a+i):
                        self[a, b].voisins = k, self[a+i, b+j]

    # -------------------------------------------------------------------------
    def length(self, line_index: int) -> int:
        " Returns the length of the n'th line "
        h, x = self.hauteur, self.largeur
        return x + line_index if line_index <= h // 2 \
                                                    else x + h - 1 - line_index

    # -------------------------------------------------------------------------
    @property
    def largeur(self) -> int:
        return self.__x

    # -------------------------------------------------------------------------
    @property
    def hauteur(self) -> int:
        return self.__h

    # -------------------------------------------------------------------------
    @property
    def configuration(self) -> List['Case']:
        return [copy.copy(x) for x in self.__cells]

    # -------------------------------------------------------------------------
    @property
    def libres(self) -> List['Case']:
        return list(filter(lambda x: x.estLibre, self.configuration))

    # -------------------------------------------------------------------------
    def jouables(self, color: 'Color') -> List['Case']:
        return list(filter(lambda x: x.estAccessible(color),self.configuration))

    # -------------------------------------------------------------------------
    def jouablesTriees(self, color: 'Color') -> List['Case']:
        jouables = self.jouables(color)
        jouables.sort(key = lambda x: x.force(color), reverse=True)
        return jouables

    # -------------------------------------------------------------------------
    def evaluation(self, color: 'Color') -> int:
        return sum([x.force for x in self.jouables(color)]) - sum(
                        [x.force for x in self.jouables(Case.reverse(color))])

    # -------------------------------------------------------------------------
    def pos2coord(self, k: int) -> 'Coord':
        if type(k) is int:
            l = self.__x
            for i in range(self.__h):
                if 0 <= k < l:
                    return i, k
                k -= l
                l += 1 if i < self.__h // 2 else -1

    # -------------------------------------------------------------------------
    def coord2pos(self, i: int, j: int) -> int:
        l, x = self.__h // 2, self.__x
        return sum([x + k if k <= l else x + l - k%l for k in range(i)]) + j

    # -------------------------------------------------------------------------
    def load(self, iterable) -> 'Plateau':
        # print("Load !!!", iterable)
        if False in [hasattr(iterable, req) for req in ('__len__','__iter__')]:
            # print('False, return !')
            return
        for x in iterable:
            if x not in COULEURS.keys():
                # print('Problem: return !', x, COULEURS.keys())
                return
        for i,x in enumerate(iterable):
            self[i].valeur = x
            if i >= len(self): return

    # -------------------------------------------------------------------------
    def __getitem__(self, index: Union['Coord', int]) -> 'Case':
        if type(index) is int:
            return self.__cells[index]
        elif type(index) is tuple and len(index) == 2:
            # noinspection PyArgumentList
            return self.__cells[self.coord2pos(*index)]

    # -------------------------------------------------------------------------
    def __len__(self) -> int:
        return  self.hauteur * self.largeur + (self.hauteur//2)**2

    # -------------------------------------------------------------------------
    def __repr__(self) -> str:
        return "Plateau({h},{l})".format(h=self.hauteur, l=self.largeur)

    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        k = max(map(len, COULEURS.values()))
        s = ''
        for i in range(self.hauteur):
            s += abs(i - self.hauteur // 2) * ' '*(k+2)
            for j in range(self.length(i)):
                s += COULEURS[self[i,j].valeur].center(k, ' ') + ' '*(k+4)
            s += '\n'
        return s

if __name__ == '__main__':
    p = Plateau()
    l = [0 for x in range(len(p))]
    print(l)
    k = p.load(l)
    print([x.valeur for x in p.configuration])