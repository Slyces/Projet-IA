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
class GameBase(Game, tk.Tk):
    def __init__(self, height: int= 5, length: int= 7, width: int=64,
                 path: str='Sprites\\', local: bool=True):
        tk.Tk.__init__(self)
        Game.__init__(self, length, height)
        self.title("You lost The Game")

        # Attributes
        self.local = local
        self.width = width

        # Creating the banner
        self._ = {} # Widgets
        self._[0] = self
        self._[1] = tk.Frame(self)
        # Principal gamespace, using a custom Canvas
        self._[2] = (CanvasWithPIL if pil else CanvasWithoutPIL)(self,
                                   height, width, path=path, relief="sunken")
        self._[2].pack(fill='both', expand=True)
        self._[2]['height'] = self.width * self.hauteur * 0.82
        self._[2]['width'] = self.width * self.largeur * 1.12

        # Binding events
        self.bind('<Button-1>', self.on_click)
        self.bind('<Button-3>', self.on_click)
        self.bind('<Key>', self.replay)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # -------------------------------------------------------------------------
    def reset(self):
        Game.__init__(self, self.largeur, self.hauteur)
        self._[2].delete('all')
        for x in range(len(self)):
            i,j = self.pos2coord(x)
            self.display(i, j, self[i,j].valeur)
        self.player_token()

    # -------------------------------------------------------------------------
    def on_click(self, ev, color=None):
        color = color if color else self.color
        try: i,j = self._[2].hexagon(ev.x,ev.y)
        except: return
        self.play(i, j, color)

    # -------------------------------------------------------------------------
    def play(self, i, j, color=None, **kwargs):
        color = color if color else self.color
        for (i,j),_from in super().play(i, j, out=True, color=color):
            self.display(i, j, color, _from)
            self.token = 0 if index(color)-1 else 1
            self.player_token()
        #@TODO : Vérifier que les coordonnés sont dans la bonne base (0-0 à l'angle du canvas, et pas de la fenêtre

    # -------------------------------------------------------------------------
    def on_closing(self):
        print("\n" + "=" * 31 + " Game Ended " + "=" * 31)
        self.destroy()

    # -------------------------------------------------------------------------
    def replay(self, ev):
        if self.finished:
            self.reset()

    # -------------------------------------------------------------------------
    def player_token(self):
        # PIL dependant
        self._[2].delete('token')
        pass

    # -------------------------------------------------------------------------
    def check_state(self):
        if (not self.jouables(NOIR)) or (not self.jouables(BLANC)):
            color = BLANC if self.jouables(BLANC) else NOIR
            i,j = self.pos2coord(self.jouables(color)[0].position)
            self[i,j].valeur = color
            self.display(i, j, color, VIDE)
            if self.jouables(BLANC) or self.jouables(NOIR):
                self.after(100, self.check_state)
            else:
                self.on_game_end()

    # -------------------------------------------------------------------------
    def on_game_end(self):
        self.finished = True
        scores = [len(list(filter(lambda x: x.valeur == color,
                              self.configuration))) for color in (BLANC, NOIR)]
        return scores
        # pil dependant
        pass

    # -------------------------------------------------------------------------
    def display(self, i, j, color, _from=None):
        _from = color if _from is None else _from
        self._[2].delete("%s,%s" % (i, j))
        self._[2].display_hexagon(i, j, color)

# =============================================================================
class ThePilGame(GameBase):
    def __init__(self, height: int = 5, length: int = 7, width: int = 64,
                 path: str = 'Sprites\\', local: bool = True):
        GameBase.__init__(self, height, length, width, path, local)
        self.images = {}
        for i in range(2):
            self.images['Victory', i] = load_image(path +
                                                   "Victory %s.png" % (i + 1))
            self.images['Token', i] = load_image(path + "Token %s.png" % i,
                                                 (width * 0.8, width * 0.8))
        # Initial display
        self.reset()
        # Run
        self.mainloop()

    # -------------------------------------------------------------------------
    def player_token(self):
        super().player_token()
        self._[2].create_image(self.width / 2.2, self.width / 2,
                           image=self.images['Token', self.token], tag='token')

    def on_game_end(self):
        scores = super().on_game_end()
        winner = 0 if scores[0] > scores[1] else 1
        self._[2].create_image(self.winfo_width() * 0.5, self.winfo_height() \
                               * 0.5, image=self.images["Victory", winner])

# =============================================================================
class TheNotPilGame(GameBase):
    def __init__(self, height: int = 5, length: int = 7, width: int = 64,
                 path: str = 'Sprites\\', local: bool = True):
        GameBase.__init__(self, height, length, width, path, local)
        # Initial display
        self.reset()
        # Run
        self.mainloop()

    # -------------------------------------------------------------------------
    def player_token(self):
        super().player_token()
        self._[2].create_oval(2,2,self.width*0.65+2, self.width*0.65+2,
                          fill=self._[2].colors[self.tokenColor],tag = 'token')

    # -------------------------------------------------------------------------
    def on_game_end(self):
        scores = super().on_game_end()
        winner = 0 if scores[0] > scores[1] else 1
        w_x, w_y = self.winfo_width(), self.winfo_height()
        self._[2].create_rectangle(0.1*w_x, 0.1*w_y, 0.9*w_x, 0.9*w_y,
                                   outline="#4E4E4E", width=8, fill="#C7C7C7")
        self._[2].create_text(0.5*w_x, 0.5*w_y, font=("Times", 26, "bold"),
                              text="Bleu {} - {} Rouge".format(*scores))

    # -------------------------------------------------------------------------
    def display(self, i, j, color, _from=None):
        print("called")
        _from = color if _from is None else _from
        self._[2].delete("%s,%s" % (i, j))
        self._[2].animate(i, j, color, _from)

# =============================================================================

# =============================================================================
class TheGame(ThePilGame if pil else TheNotPilGame):
    def __init__(self, height: int= 5, length: int= 7, width: int=64,
                 path: str='Sprites\\', local: bool=True):
        (ThePilGame if pil else TheNotPilGame).__init__(self, height, length,
                                                        width, path, local)

if __name__ == '__main__':
    G = TheGame()