# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille'
__version__ = ''
__date__ = '08/02/2017'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__status__ = 'Prototype'
# =============================================================================
from Virus.Structures import *
# =============================================================================
class Game(Plateau):
    def __init__(self, length: int= 5, height: int= 5):
        Plateau.__init__(self, length, height)
        self.player, self.token = 0, 0
        self.finished = False
        self[0].valeur = NOIR
        self[len(self) - 1].valeur = NOIR
        self[0, self.largeur - 1].valeur = BLANC
        self[self.hauteur - 1, 0].valeur = BLANC

    # -------------------------------------------------------------------------
    @property
    def color(self):
        return [BLANC, NOIR][self.player]

    # -------------------------------------------------------------------------
    def initialize(self):
        self.player, self.token = 0, 0
        Plateau.__init__(self, self.largeur, self.hauteur)
        self.finished = False
        self[0].valeur = NOIR
        self[len(self)-1].valeur = NOIR
        self[0, self.largeur - 1].valeur = BLANC
        self[self.hauteur - 1, 0].valeur = BLANC

    # -------------------------------------------------------------------------
    def play(self, i, j, color= None, player=None, out= False):
        """ Plays in position <i,j> as player <color>. Output yields coords """
        color = color if color else self.color
        player = self.player if player is None else player
        if self[i,j].estAccessible(color) and player == self.token:
            if out:
                yield (i, j), self[i,j].valeur
            self[i,j].valeur = color
            for voisin in self[i,j].voisins:
                if voisin.valeur == Case.reverse(color):
                    if out:
                        yield self.pos2coord(voisin.position), voisin.valeur
                    voisin.valeur = color
            self.check_state()

    # -------------------------------------------------------------------------
    def check_state(self):
        # To be overriden
        pass