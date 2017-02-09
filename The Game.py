# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille & Antoine Loizel'
__version__ = ''
__date__ = '09/02/2017'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__email__ += ' & ' + 'antoine.loizel@etu.u-bordeaux.fr'
__status__ = 'Prototype'
# =============================================================================
from Interface.Graphic import *
from Virus.GameLogic import *


# =============================================================================
class TheGame(tk.Tk, Game):
    def __init__(self, height: int= 5, length: int= 7, width: int=64,
                 path: str='Sprites\\', local: bool=True):
        tk.Tk.__init__(self)
        Game.__init__(self, height, length)
        self.title("You lost The Game")

        # Attributes
        self.local = local

        # Creating the banner
        self._w = {} # Widgets
        self._w[0] = self
        if pil:  # Creating a banner if pil is available
            self._w[1] = tk.Frame(self)
        # Principal gamespace, using a custom Canvas
        self._w[2] = HexCanvas(self, height, width, path=path, relief="sunken")
        self._w[2].pack(fill='both', expand=True)
        self._w[2]['height'] = self.width*2*self.hauteur
        self._w[2]['width'] = self.width*2*self.largeur

        # Loading pil images
        if pil:
            self.images = {}
            for i in range(1,3):
                self.images['Victory', i] = load_image(path+"Victory %s" % i)

        # Binding events
        self.bind('<Button-1>', self.left_click)
        self.bind('<Button-2>', self.right_click)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # -------------------------------------------------------------------------
    def on_click(self, ev, color=None):
        color = color if color else self.color
        coord = self._w[2].hexagon(ev.x, ev.y) #Can be None
        #@TODO : Vérifier que les coordonnés sont dans la bonne base (0-0 à l'angle du canvas, et pas de la fenêtre
        if coord:
            a,b = coord
            for (i,j) in self.play(a, b, color=color, out=True):
                self.display(i, j)

    # -------------------------------------------------------------------------
    def right_click(self, ev):
        if self.local:
            return self.on_click(ev, color= BLEU)
        else:
            return self.on_click(ev)

    # -------------------------------------------------------------------------
    def left_click(self, ev):
        if self.local:
            return slf.on_click(ev, color=ROUGE)
        else:
            return self.on_click(ev)

    # -------------------------------------------------------------------------
    def on_closing(self):
        print("\n" + "=" * 31 + " Game Ended " + "=" * 31)
        self.destroy()

    # -------------------------------------------------------------------------
    def player_token(self):
        self.canvas.create_image(self.width / 2, self.width / 1.8, image=self.__tokens[self.token])

    # -------------------------------------------------------------------------
    def change(self, i, j, color, _from=None):
        self.canvas.delete("%s,%s" % (i,j))
