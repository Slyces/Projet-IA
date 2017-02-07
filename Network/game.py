# =============================================================================
'''
Quick description of the file
'''
# =============================================================================
__author__ = 'Simon Lassourreuille'
__version__ = ''
__date__ = '01/02/2017'
__email__ = 'simon.lassourreuille@etu.u-bordeaux.fr'
__status__ = 'Prototype'
# =============================================================================
import tkinter as tk
from PIL import Image, ImageTk

class Game(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.__w = {}
        self.image = [None for i in range(4)]
        for i in range(4):
            image = Image.open("{}.png".format(i))
            self.image[i] = ImageTk.PhotoImage(image)
        for i in range(3):
            for j in range(3):
                k = tk.Frame(self, bg='white', relief="ridge", bd=2,height=64, width=64)
                k.pack_propagate(False)
                k.grid(row=i, column=j, padx=1, pady=1)
                self[i,j] = tk.Label(k, bg='white')
                self[i,j].pack(fill='both', expand=True)
                self[i,j].pos = (i,j)
                self[i,j].bind('<Button-1>', self.callback)
                self[i,j].bind('<Button-3>', self.erase)

        self._cells = dict([((i//3,i%3),3) for i in range(9)])
        self.player = 0
        self.win = False
        self.display()
        self.mainloop()

    def __getitem__(self, item):
        return self.__w.__getitem__(item)

    def __setitem__(self, key, value):
        self.__w.__setitem__(key, value)

    def erase(self, ev):
        self._cells[ev.widget.pos] = None
        self.display()

    def callback(self, ev):
        reset = False
        if self.win:
            for i in range(3):
                for j in range(3):
                    self._cells[i,j] = 3
                    self[i,j].master['bd'] = 2
                    self[i,j].master['relief'] = 'ridge'
            self.player = 0
            self.win = False
        else :
            self.play(ev.widget.pos, self.player)
            self.player = (self.player + 1) % 2
        self.display()

    def check(self):
        for L in ([[(i,j) for i in range(3)] for j in range(3)] +\
                              [[(j,i) for i in range(3)] for j in range(3)] + [[(i,i) for i in range(3)]]\
                              + [[(i,2-i) for i in range(3)]]):
            if self._cells[L[0]] == self._cells[L[1]] == self._cells[L[2]] != 3:
                self.win = True
                for (k,l) in L:
                    self[k,l].master['bd'] = 4
                    self[k,l].master['relief'] = 'raised'

    def play(self, coords, player: int= 0):
        self._cells[coords] = player
        self.check()

    def display(self):
        for (i,j) in self._cells.keys():
            if self._cells[i,j] in (0,1, 3):
                self[i,j]['image'] = self.image[self._cells[i,j]]
                # self[i,j]['bg'] = {None:'white', 0:'blue', 1:'red', 2:'green'}[self._cells[i,j]]

if __name__ == '__main__':
    game = Game()